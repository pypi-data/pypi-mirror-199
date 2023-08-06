# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

import math
import time
import numpy as num
import logging
import enum

from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize

from .qt_compat import qc, qg, qw

from .marker import Marker, PhaseMarker, EventMarker  # noqa
from .marker import MarkerParseError, MarkerOneNSLCRequired  # noqa
from .marker import load_markers, save_markers  # noqa
from pyrocko import plot


try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as WebView
except ImportError:
    from PyQt5.QtWebKitWidgets import QWebView as WebView


logger = logging.getLogger('pyrocko.gui.util')


def make_QPolygonF(xdata, ydata):
    assert len(xdata) == len(ydata)
    qpoints = qg.QPolygonF(len(ydata))
    vptr = qpoints.data()
    vptr.setsize(len(ydata)*8*2)
    aa = num.ndarray(
        shape=(len(ydata), 2),
        dtype=num.float64,
        buffer=memoryview(vptr))
    aa.setflags(write=True)
    aa[:, 0] = xdata
    aa[:, 1] = ydata
    return qpoints


def get_colormap_qimage(cmap_name, vmin=None, vmax=None):
    NCOLORS = 512
    norm = Normalize()
    norm.vmin = vmin
    norm.vmax = vmax

    return qg.QImage(
        get_cmap(cmap_name)(
            norm(num.linspace(0., 1., NCOLORS)),
            alpha=None, bytes=True),
        NCOLORS, 1, qg.QImage.Format_RGBX8888)


class Label(object):
    def __init__(
            self, p, x, y, label_str,
            label_bg=None,
            anchor='BL',
            outline=False,
            font=None,
            color=None):

        text = qg.QTextDocument()
        if font:
            text.setDefaultFont(font)
        text.setDefaultStyleSheet('span { color: %s; }' % color.name())
        text.setHtml('<span>%s</span>' % label_str)
        s = text.size()
        rect = qc.QRect(0, 0, int(s.width()), int(s.height()))
        tx, ty = x, y

        if 'B' in anchor:
            ty -= rect.height()
        if 'R' in anchor:
            tx -= rect.width()
        if 'M' in anchor:
            ty -= rect.height() // 2
        if 'C' in anchor:
            tx -= rect.width() // 2

        rect.translate(int(tx), int(ty))
        self.rect = rect
        self.text = text
        self.outline = outline
        self.label_bg = label_bg
        self.color = color
        self.p = p

    def draw(self):
        p = self.p
        rect = self.rect
        tx = rect.left()
        ty = rect.top()

        if self.outline:
            oldpen = p.pen()
            oldbrush = p.brush()
            p.setBrush(self.label_bg)
            rect.adjust(-2, 0, 2, 0)
            p.drawRect(rect)
            p.setPen(oldpen)
            p.setBrush(oldbrush)

        else:
            if self.label_bg:
                p.fillRect(rect, self.label_bg)

        p.translate(int(tx), int(ty))
        self.text.drawContents(p)
        p.translate(-int(tx), -int(ty))


def draw_label(p, x, y, label_str, label_bg, anchor='BL', outline=False):
    fm = p.fontMetrics()

    label = label_str
    rect = fm.boundingRect(label)

    tx, ty = x, y
    if 'T' in anchor:
        ty += rect.height()
    if 'R' in anchor:
        tx -= rect.width()
    if 'M' in anchor:
        ty += rect.height() // 2
    if 'C' in anchor:
        tx -= rect.width() // 2

    rect.translate(int(tx), int(ty))
    if outline:
        oldpen = p.pen()
        oldbrush = p.brush()
        p.setBrush(label_bg)
        rect.adjust(-2, 0, 2, 0)
        p.drawRect(rect)
        p.setPen(oldpen)
        p.setBrush(oldbrush)

    else:
        p.fillRect(rect, label_bg)

    p.drawText(int(tx), int(ty), label)


def get_err_palette():
    err_palette = qg.QPalette()
    err_palette.setColor(qg.QPalette.Base, qg.QColor(255, 200, 200))
    return err_palette


class QSliderNoWheel(qw.QSlider):

    def wheelEvent(self, ev):
        ev.ignore()

    def keyPressEvent(self, ev):
        ev.ignore()


class MyValueEdit(qw.QLineEdit):

    edited = qc.pyqtSignal(float)

    def __init__(
            self,
            low_is_none=False,
            high_is_none=False,
            low_is_zero=False,
            *args, **kwargs):

        qw.QLineEdit.__init__(self, *args, **kwargs)
        self.value = 0.
        self.mi = 0.
        self.ma = 1.
        self.low_is_none = low_is_none
        self.high_is_none = high_is_none
        self.low_is_zero = low_is_zero
        self.editingFinished.connect(
            self.myEditingFinished)
        self.lock = False

    def setRange(self, mi, ma):
        self.mi = mi
        self.ma = ma

    def setValue(self, value):
        if not self.lock:
            self.value = value
            self.setPalette(qw.QApplication.palette())
            self.adjust_text()

    def myEditingFinished(self):
        try:
            t = str(self.text()).strip()
            if self.low_is_none and t in ('off', 'below'):
                value = self.mi
            elif self.high_is_none and t in ('off', 'above'):
                value = self.ma
            elif self.low_is_zero and float(t) == 0.0:
                value = self.mi
            else:
                value = float(t)

            if not (self.mi <= value <= self.ma):
                raise Exception('out of range')

            if value != self.value:
                self.value = value
                self.lock = True
                self.edited.emit(value)
                self.setPalette(qw.QApplication.palette())
        except Exception:
            self.setPalette(get_err_palette())

        self.lock = False

    def adjust_text(self):
        t = ('%8.5g' % self.value).strip()

        if self.low_is_zero and self.value == self.mi:
            t = '0'

        if self.low_is_none and self.value == self.mi:
            if self.high_is_none:
                t = 'below'
            else:
                t = 'off'

        if self.high_is_none and self.value == self.ma:
            if self.low_is_none:
                t = 'above'
            else:
                t = 'off'

        if t in ('off', 'below', 'above'):
            self.setStyleSheet('font-style: italic;')
        else:
            self.setStyleSheet(None)

        self.setText(t)


class ValControl(qw.QWidget):

    valchange = qc.pyqtSignal(object, int)

    def __init__(
            self,
            low_is_none=False,
            high_is_none=False,
            low_is_zero=False,
            type=float,
            *args):

        qc.QObject.__init__(self, *args)

        self.lname = qw.QLabel('name')
        self.lname.setSizePolicy(
            qw.QSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum))
        self.lvalue = MyValueEdit(
            low_is_none=low_is_none,
            high_is_none=high_is_none,
            low_is_zero=low_is_zero)
        self.lvalue.setFixedWidth(100)
        self.slider = QSliderNoWheel(qc.Qt.Horizontal)
        self.slider.setSizePolicy(
            qw.QSizePolicy(qw.QSizePolicy.Expanding, qw.QSizePolicy.Minimum))
        self.slider.setMaximum(10000)
        self.slider.setSingleStep(100)
        self.slider.setPageStep(1000)
        self.slider.setTickPosition(qw.QSlider.NoTicks)
        self.slider.setFocusPolicy(qc.Qt.ClickFocus)

        self.low_is_none = low_is_none
        self.high_is_none = high_is_none
        self.low_is_zero = low_is_zero

        self.slider.valueChanged.connect(
                     self.slided)
        self.lvalue.edited.connect(
                     self.edited)

        self.type = type
        self.mute = False

    def widgets(self):
        return self.lname, self.lvalue, self.slider

    def s2v(self, svalue):
        if self.ma == 0 or self.mi == 0:
            return 0

        a = math.log(self.ma/self.mi) / 10000.
        value = self.mi*math.exp(a*svalue)
        value = self.type(value)
        return value

    def v2s(self, value):
        value = self.type(value)

        if value == 0 or self.mi == 0:
            return 0

        a = math.log(self.ma/self.mi) / 10000.
        return int(round(math.log(value/self.mi) / a))

    def setup(self, name, mi, ma, cur, ind):
        self.lname.setText(name)
        self.mi = mi
        self.ma = ma
        self.ind = ind
        self.lvalue.setRange(self.s2v(0), self.s2v(10000))
        self.set_value(cur)

    def set_range(self, mi, ma):
        if self.mi == mi and self.ma == ma:
            return

        vput = None
        if self.cursl == 0:
            vput = mi
        if self.cursl == 10000:
            vput = ma

        self.mi = mi
        self.ma = ma
        self.lvalue.setRange(self.s2v(0), self.s2v(10000))

        if vput is not None:
            self.set_value(vput)
        else:
            if self.cur < mi:
                self.set_value(mi)
            if self.cur > ma:
                self.set_value(ma)

    def set_value(self, cur):
        if cur is None:
            if self.low_is_none:
                cur = self.mi
            elif self.high_is_none:
                cur = self.ma

        if cur == 0.0:
            if self.low_is_zero:
                cur = self.mi

        self.mute = True
        self.cur = cur
        self.cursl = self.v2s(cur)
        self.slider.blockSignals(True)
        self.slider.setValue(self.cursl)
        self.slider.blockSignals(False)
        self.lvalue.blockSignals(True)
        if self.cursl in (0, 10000):
            self.lvalue.setValue(self.s2v(self.cursl))
        else:
            self.lvalue.setValue(self.cur)
        self.lvalue.blockSignals(False)
        self.mute = False

    def set_tracking(self, tracking):
        self.slider.setTracking(tracking)

    def get_value(self):
        return self.cur

    def slided(self, val):
        if self.cursl != val:
            self.cursl = val
            cur = self.s2v(self.cursl)

            if cur != self.cur:
                self.cur = cur
                self.lvalue.blockSignals(True)
                self.lvalue.setValue(self.cur)
                self.lvalue.blockSignals(False)
                self.fire_valchange()

    def edited(self, val):
        if self.cur != val:
            self.cur = val
            cursl = self.v2s(val)
            if (cursl != self.cursl):
                self.slider.blockSignals(True)
                self.slider.setValue(cursl)
                self.slider.blockSignals(False)
                self.cursl = cursl

            self.fire_valchange()

    def fire_valchange(self):

        if self.mute:
            return

        cur = self.cur

        if self.cursl == 0:
            if self.low_is_none:
                cur = None

            elif self.low_is_zero:
                cur = 0.0

        if self.cursl == 10000 and self.high_is_none:
            cur = None

        self.valchange.emit(cur, int(self.ind))


class LinValControl(ValControl):

    def s2v(self, svalue):
        value = svalue/10000. * (self.ma-self.mi) + self.mi
        value = self.type(value)
        return value

    def v2s(self, value):
        value = self.type(value)
        if self.ma == self.mi:
            return 0
        return int(round((value-self.mi)/(self.ma-self.mi) * 10000.))


class ColorbarControl(qw.QWidget):

    AVAILABLE_CMAPS = (
        'viridis',
        'plasma',
        'magma',
        'binary',
        'Reds',
        'copper',
        'seismic',
        'RdBu',
        'YlGn',
    )

    DEFAULT_CMAP = 'viridis'

    cmap_changed = qc.pyqtSignal(str)
    show_absolute_toggled = qc.pyqtSignal(bool)
    show_integrate_toggled = qc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lname = qw.QLabel('Colormap')
        self.lname.setSizePolicy(
            qw.QSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum))

        self.cmap_options = qw.QComboBox()
        self.cmap_options.setIconSize(qc.QSize(64, 12))
        for ic, cmap in enumerate(self.AVAILABLE_CMAPS):
            pixmap = qg.QPixmap.fromImage(
                get_colormap_qimage(cmap))
            icon = qg.QIcon(pixmap.scaled(64, 12))

            self.cmap_options.addItem(icon, '', cmap)
            self.cmap_options.setItemData(ic, cmap, qc.Qt.ToolTipRole)

        # self.cmap_options.setCurrentIndex(self.cmap_name)
        self.cmap_options.currentIndexChanged.connect(self.set_cmap)
        self.cmap_options.setSizePolicy(
            qw.QSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum))

        self.colorslider = ColorbarSlider(self)
        self.colorslider.setSizePolicy(
            qw.QSizePolicy.MinimumExpanding | qw.QSizePolicy.ExpandFlag,
            qw.QSizePolicy.MinimumExpanding | qw.QSizePolicy.ExpandFlag
        )
        self.clip_changed = self.colorslider.clip_changed

        btn_size = qw.QSizePolicy(
            qw.QSizePolicy.Maximum | qw.QSizePolicy.ShrinkFlag,
            qw.QSizePolicy.Maximum | qw.QSizePolicy.ShrinkFlag)

        self.symetry_toggle = qw.QPushButton()
        self.symetry_toggle.setIcon(
            qg.QIcon.fromTheme('object-flip-horizontal'))
        self.symetry_toggle.setToolTip('Symetric clip values')
        self.symetry_toggle.setSizePolicy(btn_size)
        self.symetry_toggle.setCheckable(True)
        self.symetry_toggle.toggled.connect(self.toggle_symetry)
        self.symetry_toggle.setChecked(True)

        self.reverse_toggle = qw.QPushButton()
        self.reverse_toggle.setIcon(
            qg.QIcon.fromTheme('object-rotate-right'))
        self.reverse_toggle.setToolTip('Reverse the colormap')
        self.reverse_toggle.setSizePolicy(btn_size)
        self.reverse_toggle.setCheckable(True)
        self.reverse_toggle.toggled.connect(self.toggle_reverse_cmap)

        self.abs_toggle = qw.QPushButton()
        self.abs_toggle.setIcon(
            qg.QIcon.fromTheme('go-bottom'))
        self.abs_toggle.setToolTip('Show absolute values')
        self.abs_toggle.setSizePolicy(btn_size)
        self.abs_toggle.setCheckable(True)
        self.abs_toggle.toggled.connect(self.toggle_absolute)

        self.int_toggle = qw.QPushButton()
        self.int_toggle.setText('∫')
        self.int_toggle.setToolTip(
            u'Integrate traces (e.g. strain rate → strain)')
        self.int_toggle.setSizePolicy(btn_size)
        self.int_toggle.setCheckable(True)
        self.int_toggle.setMaximumSize(
            24,
            self.int_toggle.maximumSize().height())
        self.int_toggle.toggled.connect(self.show_integrate_toggled.emit)

        v_splitter = qw.QFrame()
        v_splitter.setFrameShape(qw.QFrame.VLine)
        v_splitter.setFrameShadow(qw.QFrame.Sunken)

        self.controls = qw.QWidget()
        layout = qw.QHBoxLayout()
        layout.addWidget(self.colorslider)
        layout.addWidget(self.symetry_toggle)
        layout.addWidget(self.reverse_toggle)
        layout.addWidget(v_splitter)
        layout.addWidget(self.abs_toggle)
        layout.addWidget(self.int_toggle)
        self.controls.setLayout(layout)

        self.set_cmap_name(self.DEFAULT_CMAP)

    def set_cmap(self, idx):
        self.set_cmap_name(self.cmap_options.itemData(idx))

    def set_cmap_name(self, cmap_name):
        self.cmap_name = cmap_name
        self.colorslider.set_cmap_name(cmap_name)
        self.cmap_changed.emit(cmap_name)

    def get_cmap(self):
        return self.cmap_name

    def toggle_symetry(self, toggled):
        self.colorslider.set_symetry(toggled)

    def toggle_reverse_cmap(self):
        cmap = self.get_cmap()
        if cmap.endswith('_r'):
            r_cmap = cmap.rstrip('_r')
        else:
            r_cmap = cmap + '_r'
        self.set_cmap_name(r_cmap)

    def toggle_absolute(self, toggled):
        self.symetry_toggle.setChecked(not toggled)
        self.show_absolute_toggled.emit(toggled)

    def widgets(self):
        return (self.lname, self.cmap_options, self.controls)


class ColorbarSlider(qw.QWidget):
    DEFAULT_CMAP = 'viridis'
    CORNER_THRESHOLD = 10
    MIN_WIDTH = .05

    clip_changed = qc.pyqtSignal(float, float)

    class COMPONENTS(enum.Enum):
        LeftLine = 1
        RightLine = 2
        Center = 3

    def __init__(self, *args, cmap_name=None):
        super().__init__()
        self.cmap_name = cmap_name or self.DEFAULT_CMAP
        self.clip_min = 0.
        self.clip_max = 1.

        self._sym_locked = True
        self._mouse_inside = False
        self._window = None
        self._old_pos = None
        self._component_grabbed = None

        self.setMouseTracking(True)

    def set_cmap_name(self, cmap_name):
        self.cmap_name = cmap_name
        self.repaint()

    def get_cmap_name(self):
        return self.cmap_name

    def set_symetry(self, symetry):
        self._sym_locked = symetry
        if self._sym_locked:
            clip_max = 1. - min(self.clip_min, 1.-self.clip_max)
            clip_min = 1. - clip_max
            self.set_clip(clip_min, clip_max)

    def _set_window(self, window):
        self._window = window

    def _get_left_line(self):
        rect = self._get_active_rect()
        if not rect:
            return
        return qc.QLineF(rect.left(), 0, rect.left(), rect.height())

    def _get_right_line(self):
        rect = self._get_active_rect()
        if not rect:
            return
        return qc.QLineF(rect.right(), 0, rect.right(), rect.height())

    def _get_active_rect(self):
        if not self._window:
            return
        rect = qc.QRect(self._window)
        width = rect.width()
        rect.setLeft(width * self.clip_min)
        rect.setRight(width * self.clip_max)
        return rect

    def set_clip(self, clip_min, clip_max):
        if clip_min < 0. or clip_max > 1.:
            return
        if clip_max - clip_min < self.MIN_WIDTH:
            return

        self.clip_min = clip_min
        self.clip_max = clip_max
        self.repaint()
        self.clip_changed.emit(self.clip_min, self.clip_max)

    def mousePressEvent(self, event):
        act_rect = self._get_active_rect()
        if event.buttons() != qc.Qt.MouseButton.LeftButton:
            self._component_grabbed = None
            return

        dist_left = abs(event.pos().x() - act_rect.left())
        dist_right = abs(event.pos().x() - act_rect.right())

        if 0 < dist_left < self.CORNER_THRESHOLD:
            self._component_grabbed = self.COMPONENTS.LeftLine
            self.setCursor(qg.QCursor(qc.Qt.CursorShape.SizeHorCursor))
        elif 0 < dist_right < self.CORNER_THRESHOLD:
            self._component_grabbed = self.COMPONENTS.RightLine
            self.setCursor(qg.QCursor(qc.Qt.CursorShape.SizeHorCursor))
        else:
            self.setCursor(qg.QCursor())

    def mouseReleaseEvent(self, event):
        self._component_grabbed = None
        self.repaint()

    def mouseDoubleClickEvent(self, event):
        self.set_clip(0., 1.)

    def wheelEvent(self, event):
        event.accept()
        if not self._sym_locked:
            return

        delta = event.angleDelta().y()
        delta = -delta / 5e3
        clip_min_new = max(self.clip_min + delta, 0.)
        clip_max_new = min(self.clip_max - delta, 1.)
        self._mouse_inside = True
        self.set_clip(clip_min_new, clip_max_new)

    def mouseMoveEvent(self, event):
        act_rect = self._get_active_rect()

        if not self._component_grabbed:
            dist_left = abs(event.pos().x() - act_rect.left())
            dist_right = abs(event.pos().x() - act_rect.right())

            if 0 <= dist_left < self.CORNER_THRESHOLD or \
                    0 <= dist_right < self.CORNER_THRESHOLD:
                self.setCursor(qg.QCursor(qc.Qt.CursorShape.SizeHorCursor))
            else:
                self.setCursor(qg.QCursor())

        if self._old_pos and self._component_grabbed:
            shift = (event.pos() - self._old_pos).x() / self._window.width()

            if self._component_grabbed is self.COMPONENTS.LeftLine:
                clip_min_new = max(self.clip_min + shift, 0.)
                clip_max_new = \
                    min(self.clip_max - shift, 1.) \
                    if self._sym_locked else self.clip_max

            elif self._component_grabbed is self.COMPONENTS.RightLine:
                clip_max_new = min(self.clip_max + shift, 1.)
                clip_min_new = \
                    max(self.clip_min - shift, 0.) \
                    if self._sym_locked else self.clip_min

            self.set_clip(clip_min_new, clip_max_new)

        self._old_pos = event.pos()

    def enterEvent(self, e):
        self._mouse_inside = True
        self.repaint()

    def leaveEvent(self, e):
        self._mouse_inside = False
        self.repaint()

    def paintEvent(self, e):
        p = qg.QPainter(self)
        self._set_window(p.window())

        p.drawImage(
            p.window(),
            get_colormap_qimage(self.cmap_name, self.clip_min, self.clip_max))

        left_line = self._get_left_line()
        right_line = self._get_right_line()

        pen = qg.QPen()
        pen.setWidth(2)
        pen.setStyle(qc.Qt.DotLine)
        pen.setBrush(qc.Qt.white)
        p.setPen(pen)
        p.setCompositionMode(
            qg.QPainter.CompositionMode.CompositionMode_Difference)

        p.drawLine(left_line)
        p.drawLine(right_line)

        label_rect = self._get_active_rect()
        label_rect.setLeft(label_rect.left() + 5)
        label_rect.setRight(label_rect.right() - 5)
        label_left_rect = qc.QRectF(label_rect)
        label_right_rect = qc.QRectF(label_rect)
        label_left_align = qc.Qt.AlignLeft
        label_right_align = qc.Qt.AlignRight

        if label_rect.left() > 50:
            label_left_rect.setRight(label_rect.left() - 10)
            label_left_rect.setLeft(0)
            label_left_align = qc.Qt.AlignRight

        if self._window.right() - label_rect.right() > 50:
            label_right_rect.setLeft(label_rect.right() + 10)
            label_right_rect.setRight(self._window.right())
            label_right_align = qc.Qt.AlignLeft

        if self._mouse_inside or self._component_grabbed:
            p.drawText(
                label_left_rect,
                label_left_align | qc.Qt.AlignVCenter,
                '%d%%' % round(self.clip_min * 100))
            p.drawText(
                label_right_rect,
                label_right_align | qc.Qt.AlignVCenter,
                '%d%%' % round(self.clip_max * 100))


class Progressbar(object):
    def __init__(self, parent, name, can_abort=True):
        self.parent = parent
        self.name = name
        self.label = qw.QLabel(name, parent)
        self.pbar = qw.QProgressBar(parent)
        self.aborted = False
        self.time_last_update = 0.
        if can_abort:
            self.abort_button = qw.QPushButton('Abort', parent)
            self.abort_button.clicked.connect(
                self.abort)
        else:
            self.abort_button = None

    def widgets(self):
        widgets = [self.label, self.bar()]
        if self.abort_button:
            widgets.append(self.abort_button)
        return widgets

    def bar(self):
        return self.pbar

    def abort(self):
        self.aborted = True


class Progressbars(qw.QFrame):
    def __init__(self, parent):
        qw.QFrame.__init__(self, parent)
        self.layout = qw.QGridLayout()
        self.setLayout(self.layout)
        self.bars = {}
        self.start_times = {}
        self.hide()

    def set_status(self, name, value, can_abort=True):
        value = int(round(value))
        now = time.time()
        if name not in self.start_times:
            self.start_times[name] = now
            return False
        else:
            if now < self.start_times[name] + 1.0:
                if value == 100:
                    del self.start_times[name]
                return False

        self.start_times.get(name, 0.0)
        if name not in self.bars:
            if value == 100:
                return False
            self.bars[name] = Progressbar(self, name, can_abort=can_abort)
            self.make_layout()

        bar = self.bars[name]
        if bar.time_last_update < now - 0.1 or value == 100:
            bar.bar().setValue(value)
            bar.time_last_update = now

        if value == 100:
            del self.bars[name]
            del self.start_times[name]
            self.make_layout()
            for w in bar.widgets():
                w.setParent(None)

        return bar.aborted

    def make_layout(self):
        while True:
            c = self.layout.takeAt(0)
            if c is None:
                break

        for ibar, bar in enumerate(self.bars.values()):
            for iw, w in enumerate(bar.widgets()):
                self.layout.addWidget(w, ibar, iw)

        if not self.bars:
            self.hide()
        else:
            self.show()


def tohex(c):
    return '%02x%02x%02x' % c


def to01(c):
    return c[0]/255., c[1]/255., c[2]/255.


def beautify_axes(axes):
    try:
        from cycler import cycler
        axes.set_prop_cycle(
            cycler('color', [to01(x) for x in plot.graph_colors]))

    except (ImportError, KeyError):
        axes.set_color_cycle(list(map(to01, plot.graph_colors)))

    xa = axes.get_xaxis()
    ya = axes.get_yaxis()
    for attr in ('labelpad', 'LABELPAD'):
        if hasattr(xa, attr):
            setattr(xa, attr, xa.get_label().get_fontsize())
            setattr(ya, attr, ya.get_label().get_fontsize())
            break


class FigureFrame(qw.QFrame):

    def __init__(self, parent=None, figure_cls=None):
        qw.QFrame.__init__(self, parent)
        fgcolor = plot.tango_colors['aluminium5']
        dpi = 0.5*(self.logicalDpiX() + self.logicalDpiY())

        font = qg.QFont()
        font.setBold(True)
        fontsize = font.pointSize()

        import matplotlib
        matplotlib.rcdefaults()
        matplotlib.rcParams['backend'] = 'Qt5Agg'

        matplotlib.rc('xtick', direction='out', labelsize=fontsize)
        matplotlib.rc('ytick', direction='out', labelsize=fontsize)
        matplotlib.rc('xtick.major', size=8, width=1)
        matplotlib.rc('xtick.minor', size=4, width=1)
        matplotlib.rc('ytick.major', size=8, width=1)
        matplotlib.rc('ytick.minor', size=4, width=1)
        matplotlib.rc('figure', facecolor='white', edgecolor=tohex(fgcolor))

        matplotlib.rc(
            'font',
            family='sans-serif',
            weight='bold',
            size=fontsize,
            **{'sans-serif': [
                font.family(),
                'DejaVu Sans', 'Bitstream Vera Sans', 'Lucida Grande',
                'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica']})

        matplotlib.rc('legend', fontsize=fontsize)

        matplotlib.rc('text', color=tohex(fgcolor))
        matplotlib.rc('xtick', color=tohex(fgcolor))
        matplotlib.rc('ytick', color=tohex(fgcolor))
        matplotlib.rc('figure.subplot', bottom=0.15)

        matplotlib.rc('axes', linewidth=1.0, unicode_minus=False)
        matplotlib.rc(
            'axes',
            facecolor='white',
            edgecolor=tohex(fgcolor),
            labelcolor=tohex(fgcolor))

        try:
            from cycler import cycler
            matplotlib.rc(
                'axes', prop_cycle=cycler(
                    'color', [to01(x) for x in plot.graph_colors]))

        except (ImportError, KeyError):
            try:
                matplotlib.rc('axes', color_cycle=[
                    to01(x) for x in plot.graph_colors])

            except KeyError:
                pass

        try:
            matplotlib.rc('axes', labelsize=fontsize)
        except KeyError:
            pass

        try:
            matplotlib.rc('axes', labelweight='bold')
        except KeyError:
            pass

        if figure_cls is None:
            from matplotlib.figure import Figure
            figure_cls = Figure

        from matplotlib.backends.backend_qt5agg import \
            NavigationToolbar2QT as NavigationToolbar

        from matplotlib.backends.backend_qt5agg \
            import FigureCanvasQTAgg as FigureCanvas

        layout = qw.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
        self.figure = figure_cls(dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setSizePolicy(
            qw.QSizePolicy(
                qw.QSizePolicy.Expanding,
                qw.QSizePolicy.Expanding))
        toolbar_frame = qw.QFrame()
        toolbar_frame.setFrameShape(qw.QFrame.StyledPanel)
        toolbar_frame_layout = qw.QHBoxLayout()
        toolbar_frame_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_frame.setLayout(toolbar_frame_layout)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.canvas, 0, 0)
        toolbar_frame_layout.addWidget(self.toolbar)
        layout.addWidget(toolbar_frame, 1, 0)
        self.closed = False

    def gca(self):
        axes = self.figure.gca()
        beautify_axes(axes)
        return axes

    def gcf(self):
        return self.figure

    def draw(self):
        '''
        Draw with AGG, then queue for Qt update.
        '''
        self.canvas.draw()

    def closeEvent(self, ev):
        self.closed = True


class SmartplotFrame(FigureFrame):
    def __init__(
            self, parent=None, plot_args=[], plot_kwargs={}, plot_cls=None):

        from pyrocko.plot import smartplot

        FigureFrame.__init__(
            self,
            parent=parent,
            figure_cls=smartplot.SmartplotFigure)

        if plot_cls is None:
            plot_cls = smartplot.Plot

        self.plot = plot_cls(
            *plot_args,
            fig=self.figure,
            call_mpl_init=False,
            **plot_kwargs)


class WebKitFrame(qw.QFrame):

    def __init__(self, url=None, parent=None):
        qw.QFrame.__init__(self, parent)
        layout = qw.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.web_widget = WebView()
        layout.addWidget(self.web_widget, 0, 0)
        if url:
            self.web_widget.load(qc.QUrl(url))


class VTKFrame(qw.QFrame):

    def __init__(self, actors=None, parent=None):
        import vtk
        from vtk.qt.QVTKRenderWindowInteractor import \
            QVTKRenderWindowInteractor

        qw.QFrame.__init__(self, parent)
        layout = qw.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        layout.addWidget(self.vtk_widget, 0, 0)

        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()

        if actors:
            for a in actors:
                self.renderer.AddActor(a)

    def init(self):
        self.iren.Initialize()

    def add_actor(self, actor):
        self.renderer.AddActor(actor)


class PixmapFrame(qw.QLabel):

    def __init__(self, filename=None, parent=None):

        qw.QLabel.__init__(self, parent)
        self.setAlignment(qc.Qt.AlignCenter)
        self.setContentsMargins(0, 0, 0, 0)
        self.menu = qw.QMenu(self)
        action = qw.QAction('Save as', self.menu)
        action.triggered.connect(self.save_pixmap)
        self.menu.addAction(action)

        if filename:
            self.load_pixmap(filename)

    def contextMenuEvent(self, event):
        self.menu.popup(qg.QCursor.pos())

    def load_pixmap(self, filename):
        self.pixmap = qg.QPixmap(filename)
        self.setPixmap(self.pixmap)

    def save_pixmap(self, filename=None):
        if not filename:
            filename, _ = qw.QFileDialog.getSaveFileName(
                self.parent(), caption='save as')
        self.pixmap.save(filename)
