from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.UIGraphicsItem import UIGraphicsItem
from pyqtgraph import functions as fn
from pyqtgraph import debug as debug

from pyqtgraph.Point import Point
from pyqtgraph.graphicsItems.GraphicsObject import GraphicsObject
from pyqtgraph.graphicsItems.TextItem import TextItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
import numpy as np
import weakref

__all__ = ['FiniteLinearRegionItem']


class FiniteLinearRegionItem(UIGraphicsItem):
    """
    **Bases:** :class:`UIGraphicsItem <pyqtgraph.UIGraphicsItem>`

    Copy of LinearRegionItem from pyqtgraph, changed in a way that we can define a limits in both direction.
    Also add an option to be able to move the lines only from one integer to another.
    Another modificaiton, is the fact to remove the ability to move the lines/linearRegion in the same direction as
    their axis.

    Used for marking a horizontal or vertical region in plots.
    The region can be dragged and is bounded by lines which can be dragged individually.

    ===============================  =============================================================================
    **Signals:**
    sigRegionChangeFinished(self)    Emitted when the user has finished dragging the region (or one of its lines)
                                     and when the region is changed programatically.
    sigRegionChanged(self)           Emitted while the user is dragging the region (or one of its lines)
                                     and when the region is changed programatically.
    ===============================  =============================================================================
    """

    sigRegionChangeFinished = QtCore.Signal(object)
    sigRegionChanged = QtCore.Signal(object)
    Vertical = 0
    Horizontal = 1

    def __init__(self, time_interval, values=[0, 1], finite_values=None, orientation=None, brush=None, movable=True, bounds=None,
                 int_rounding=False, new_line_pos_callback=None, mouse_hover_callback=None):
        """Create a new LinearRegionItem.

        ==============  =====================================================================
        **Arguments:**
        values          A list of the positions of the lines in the region. These are not
                        limits; limits can be set by specifying bounds.
        time_interval   instance of TimeInterval from cicada_time_intervals.py
        finite_values     A list of the position of the lines (so there are not infinite).
                        If None, then the are will be infinite
        orientation     Options are LinearRegionItem.Vertical or LinearRegionItem.Horizontal.
                        If not specified it will be vertical.
        brush           Defines the brush that fills the region. Can be any arguments that
                        are valid for :func:`mkBrush <pyqtgraph.mkBrush>`. Default is
                        transparent blue.
        movable         If True, the region and individual lines are movable by the user; if
                        False, they are static.
        bounds          Optional [min, max] bounding values for the region
        int_rounding    if True, lines can only be moved to an integer value coordinate in
                        their orthogonal axis
        new_line_pos_callback fct to be called if the line is moved, take as argument the new pos
        mouse_hover_callback fct to be called when the mouse get (in or out) hover. The two arguments are
                        self (instance of FiniteLinearRegionItem) and hover (bool). Called only if the
                        hover state change.
        ==============  =====================================================================
        """

        UIGraphicsItem.__init__(self)
        if orientation is None:
            orientation = FiniteLinearRegionItem.Vertical
        self.orientation = orientation
        self.bounds = QtCore.QRectF()
        self.blockLineSignal = False
        self.moving = False
        self.mouseHovering = False
        self._finite_values = finite_values
        self.int_rounding = int_rounding
        self.time_interval = time_interval
        self._new_line_pos_callback = new_line_pos_callback
        self._mouse_hover_callback = mouse_hover_callback


        if orientation == FiniteLinearRegionItem.Horizontal:
            self.lines = [
                FiniteLine(pos=QtCore.QPointF(0, values[0]), angle=0, finite_values=finite_values,
                           movable=movable, bounds=bounds, int_rounding=int_rounding,
                           new_line_pos_callback=new_line_pos_callback, time_interval=time_interval,
                           first_line=True),
                FiniteLine(pos=QtCore.QPointF(0, values[1]), angle=0, finite_values=finite_values,
                           movable=movable, bounds=bounds, int_rounding=int_rounding,
                           new_line_pos_callback=new_line_pos_callback, time_interval=time_interval,
                           first_line=False)]
        elif orientation == FiniteLinearRegionItem.Vertical:
            self.lines = [
                FiniteLine(pos=QtCore.QPointF(values[1], 0), angle=90, finite_values=finite_values,
                           movable=movable, bounds=bounds, int_rounding=int_rounding,
                           new_line_pos_callback=new_line_pos_callback, time_interval=time_interval,
                           first_line=False),
                FiniteLine(pos=QtCore.QPointF(values[0], 0), angle=90, finite_values=finite_values,
                           movable=movable, bounds=bounds, int_rounding=int_rounding,
                           new_line_pos_callback=new_line_pos_callback, time_interval=time_interval,
                           first_line=True)]
        else:
            raise Exception('Orientation must be one of LinearRegionItem.Vertical or LinearRegionItem.Horizontal')

        for l in self.lines:
            l.setParentItem(self)
            l.sigPositionChangeFinished.connect(self.lineMoveFinished)
            l.sigPositionChanged.connect(self.lineMoved)

        if brush is None:
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
        self.setBrush(brush)

        self.setMovable(movable)

    def getRegion(self):
        """Return the values at the edges of the region."""
        # if self.orientation[0] == 'h':
        # r = (self.bounds.top(), self.bounds.bottom())
        # else:
        # r = (self.bounds.left(), self.bounds.right())
        r = [self.lines[0].value(), self.lines[1].value()]
        return (min(r), max(r))

    def setRegion(self, rgn):
        """Set the values for the edges of the region.

        ==============   ==============================================
        **Arguments:**
        rgn              A list or tuple of the lower and upper values.
        ==============   ==============================================
        """
        if self.lines[0].value() == rgn[0] and self.lines[1].value() == rgn[1]:
            return
        self.blockLineSignal = True
        self.lines[0].setValue(rgn[0])
        self.blockLineSignal = False
        self.lines[1].setValue(rgn[1])
        # self.blockLineSignal = False
        self.lineMoved()
        self.lineMoveFinished()

    def setBrush(self, *br, **kargs):
        """Set the brush that fills the region. Can have any arguments that are valid
        for :func:`mkBrush <pyqtgraph.mkBrush>`.
        """
        self.brush = fn.mkBrush(*br, **kargs)
        self.currentBrush = self.brush

    def setBounds(self, bounds):
        """Optional [min, max] bounding values for the region. To have no bounds on the
        region use [None, None].
        Does not affect the current position of the region unless it is outside the new bounds.
        See :func:`setRegion <pyqtgraph.LinearRegionItem.setRegion>` to set the position
        of the region."""
        for l in self.lines:
            l.setBounds(bounds)

    def setMovable(self, m):
        """Set lines to be movable by the user, or not. If lines are movable, they will
        also accept HoverEvents."""
        for l in self.lines:
            l.setMovable(m)
        self.movable = m
        self.setAcceptHoverEvents(m)

    def boundingRect(self):
        br = UIGraphicsItem.boundingRect(self)
        rng = self.getRegion()
        if self.orientation == FiniteLinearRegionItem.Vertical:
            br.setLeft(rng[0])
            br.setRight(rng[1])
            # finite rectangle
            if self._finite_values is not None:
                br.setBottom(self._finite_values[0])
                br.setTop(self._finite_values[1])
        else:  # horizontal
            br.setTop(rng[0])
            br.setBottom(rng[1])
            if self._finite_values is not None:
                br.setLeft(self._finite_values[0])
                br.setRight(self._finite_values[1])
        return br.normalized()

    def paint(self, p, *args):
        profiler = debug.Profiler()
        UIGraphicsItem.paint(self, p, *args)
        p.setBrush(self.currentBrush)
        p.setPen(fn.mkPen(None))
        p.drawRect(self.boundingRect())

    def dataBounds(self, axis, frac=1.0, orthoRange=None):
        if axis == self.orientation:
            return self.getRegion()
        else:
            return None

    def lineMoved(self):
        if self.blockLineSignal:
            return
        self.prepareGeometryChange()
        # self.emit(QtCore.SIGNAL('regionChanged'), self)
        self.sigRegionChanged.emit(self)

    def lineMoveFinished(self):
        # self.emit(QtCore.SIGNAL('regionChangeFinished'), self)
        self.sigRegionChangeFinished.emit(self)

    # def updateBounds(self):
    # vb = self.view().viewRect()
    # vals = [self.lines[0].value(), self.lines[1].value()]
    # if self.orientation[0] == 'h':
    # vb.setTop(min(vals))
    # vb.setBottom(max(vals))
    # else:
    # vb.setLeft(min(vals))
    # vb.setRight(max(vals))
    # if vb != self.bounds:
    # self.bounds = vb
    # self.rect.setRect(vb)

    # def mousePressEvent(self, ev):
    # if not self.movable:
    # ev.ignore()
    # return
    # for l in self.lines:
    # l.mousePressEvent(ev)  ## pass event to both lines so they move together
    ##if self.movable and ev.button() == QtCore.Qt.LeftButton:
    ##ev.accept()
    ##self.pressDelta = self.mapToParent(ev.pos()) - QtCore.QPointF(*self.p)
    ##else:
    ##ev.ignore()

    # def mouseReleaseEvent(self, ev):
    # for l in self.lines:
    # l.mouseReleaseEvent(ev)

    # def mouseMoveEvent(self, ev):
    ##print "move", ev.pos()
    # if not self.movable:
    # return
    # self.lines[0].blockSignals(True)  # only want to update once
    # for l in self.lines:
    # l.mouseMoveEvent(ev)
    # self.lines[0].blockSignals(False)
    ##self.setPos(self.mapToParent(ev.pos()) - self.pressDelta)
    ##self.emit(QtCore.SIGNAL('dragged'), self)

    def mouseDragEvent(self, ev):
        if not self.movable or int(ev.button() & QtCore.Qt.LeftButton) == 0:
            return
        ev.accept()

        if ev.isStart():
            bdp = ev.buttonDownPos()
            self.cursorOffsets = [l.pos() - bdp for l in self.lines]
            self.startPositions = [l.pos() for l in self.lines]
            self.moving = True

        if not self.moving:
            return

        # delta = ev.pos() - ev.lastPos()
        self.lines[0].blockSignals(True)  # only want to update once
        for i, l in enumerate(self.lines):
            # we want to forbid the line to move in its axis, it should be moving only orthogonaly
            # valid only for angle of 0 and 90
            new_pos = list(self.cursorOffsets[i] + ev.pos())
            if self.orientation == FiniteLinearRegionItem.Vertical:
                if self.int_rounding:
                    new_pos[0] = round(new_pos[0])
                l.setPos([new_pos[0], self.startPositions[i][1]])
                if self._new_line_pos_callback is not None:
                    self._new_line_pos_callback(new_pos=new_pos[0], first_value=l._first_line,
                                                time_interval=self.time_interval)
            else:  # horizontal
                if self.int_rounding:
                    new_pos[1] = round(new_pos[1])
                l.setPos([self.startPositions[i][0], new_pos[1]])
                if self._new_line_pos_callback is not None:
                    self._new_line_pos_callback(new_pos=new_pos[1], first_value=l._first_line,
                                                time_interval=self.time_interval)
            # l.setPos(l.pos()+delta)
            # l.mouseDragEvent(ev)
        self.lines[0].blockSignals(False)
        self.prepareGeometryChange()

        if ev.isFinish():
            self.moving = False
            self.sigRegionChangeFinished.emit(self)
        else:
            self.sigRegionChanged.emit(self)

    def mouseClickEvent(self, ev):
        if self.moving and ev.button() == QtCore.Qt.RightButton:
            ev.accept()
            for i, l in enumerate(self.lines):
                l.setPos(self.startPositions[i])
            self.moving = False
            self.sigRegionChanged.emit(self)
            self.sigRegionChangeFinished.emit(self)

    def hoverEvent(self, ev):
        if self.movable and (not ev.isExit()) and ev.acceptDrags(QtCore.Qt.LeftButton):
            self.setMouseHover(True)
        else:
            self.setMouseHover(False)

    def setMouseHover(self, hover):
        ## Inform the item that the mouse is(not) hovering over it
        if self.mouseHovering == hover:
            return
        self.mouseHovering = hover
        if self._mouse_hover_callback is not None:
            self._mouse_hover_callback(self, hover)
        if hover:
            c = self.brush.color()
            c.setAlpha(min(c.alpha() * 2, 255))
            self.currentBrush = fn.mkBrush(c)
        else:
            self.currentBrush = self.brush
        self.update()

    # def hoverEnterEvent(self, ev):
    # print "rgn hover enter"
    # ev.ignore()
    # self.updateHoverBrush()

    # def hoverMoveEvent(self, ev):
    # print "rgn hover move"
    # ev.ignore()
    # self.updateHoverBrush()

    # def hoverLeaveEvent(self, ev):
    # print "rgn hover leave"
    # ev.ignore()
    # self.updateHoverBrush(False)

    # def updateHoverBrush(self, hover=None):
    # if hover is None:
    # scene = self.scene()
    # hover = scene.claimEvent(self, QtCore.Qt.LeftButton, scene.Drag)

    # if hover:
    # self.currentBrush = fn.mkBrush(255, 0,0,100)
    # else:
    # self.currentBrush = self.brush
    # self.update()


__all__ = ['FiniteLine', 'fLineLabel']


class FiniteLine(GraphicsObject):
    """
    **Bases:** :class:`GraphicsObject <pyqtgraph.GraphicsObject>`

    Displays a line of infinite length.
    This line may be dragged to indicate a position in data coordinates.

    =============================== ===================================================
    **Signals:**
    sigDragged(self)
    sigPositionChangeFinished(self)
    sigPositionChanged(self)
    =============================== ===================================================
    """

    sigDragged = QtCore.Signal(object)
    sigPositionChangeFinished = QtCore.Signal(object)
    sigPositionChanged = QtCore.Signal(object)

    def __init__(self, time_interval, first_line, pos=None, angle=90, finite_values=None, pen=None, movable=False, bounds=None,
                 hoverPen=None, label=None, labelOpts=None, name=None, int_rounding=False,
                 new_line_pos_callback=None):
        """
        =============== ==================================================================
        **Arguments:**
        first_line      Indicate if it is the first line in the case of LinearRegion usage
        pos             Position of the line. This can be a QPointF or a single value for
                        vertical/horizontal lines.
        angle           Angle of line in degrees. 0 is horizontal, 90 is vertical.
        pen             Pen to use when drawing line. Can be any arguments that are valid
                        for :func:`mkPen <pyqtgraph.mkPen>`. Default pen is transparent
                        yellow.
        finite_values   List of the values representing the start and end of the line. If None the line
                        is Infinite covering all the viewBox
        movable         If True, the line can be dragged to a new position by the user.
        hoverPen        Pen to use when drawing line when hovering over it. Can be any
                        arguments that are valid for :func:`mkPen <pyqtgraph.mkPen>`.
                        Default pen is red.
        bounds          Optional [min, max] bounding values. Bounds are only valid if the
                        line is vertical or horizontal.
        label           Text to be displayed in a label attached to the line, or
                        None to show no label (default is None). May optionally
                        include formatting strings to display the line value.
        labelOpts       A dict of keyword arguments to use when constructing the
                        text label. See :class:`InfLineLabel`.
        name            Name of the item
        int_rounding    if True, lines can only be moved to an integer value coordinate in
                        their orthogonal axis (valid only for angle 0 or 90
        =============== ==================================================================
        """
        self._boundingRect = None
        self._line = None

        self._name = name

        self._finite_values = finite_values

        self.int_rounding = int_rounding

        self._new_line_pos_callback = new_line_pos_callback

        self.time_interval = time_interval

        self._first_line = first_line

        GraphicsObject.__init__(self)

        if bounds is None:  ## allowed value boundaries for orthogonal lines
            self.maxRange = [None, None]
        else:
            self.maxRange = bounds
        self.moving = False
        self.setMovable(movable)
        self.mouseHovering = False
        self.p = [0, 0]
        self.setAngle(angle)

        if pos is None:
            pos = Point(0, 0)
        self.setPos(pos)

        if pen is None:
            pen = (200, 200, 100)
        self.setPen(pen)
        if hoverPen is None:
            self.setHoverPen(color=(255, 0, 0), width=self.pen.width())
        else:
            self.setHoverPen(hoverPen)
        self.currentPen = self.pen

        if label is not None:
            labelOpts = {} if labelOpts is None else labelOpts
            self.label = fLineLabel(self, text=label, **labelOpts)

    def setMovable(self, m):
        """Set whether the line is movable by the user."""
        self.movable = m
        self.setAcceptHoverEvents(m)

    def setBounds(self, bounds):
        """Set the (minimum, maximum) allowable values when dragging."""
        self.maxRange = bounds
        self.setValue(self.value())

    def setPen(self, *args, **kwargs):
        """Set the pen for drawing the line. Allowable arguments are any that are valid
        for :func:`mkPen <pyqtgraph.mkPen>`."""
        self.pen = fn.mkPen(*args, **kwargs)
        if not self.mouseHovering:
            self.currentPen = self.pen
            self.update()

    def setHoverPen(self, *args, **kwargs):
        """Set the pen for drawing the line while the mouse hovers over it.
        Allowable arguments are any that are valid
        for :func:`mkPen <pyqtgraph.mkPen>`.

        If the line is not movable, then hovering is also disabled.

        Added in version 0.9.9."""
        self.hoverPen = fn.mkPen(*args, **kwargs)
        if self.mouseHovering:
            self.currentPen = self.hoverPen
            self.update()

    def setAngle(self, angle):
        """
        Takes angle argument in degrees.
        0 is horizontal; 90 is vertical.

        Note that the use of value() and setValue() changes if the line is
        not vertical or horizontal.
        """
        self.angle = ((angle + 45) % 180) - 45  ##  -45 <= angle < 135
        self.resetTransform()
        self.rotate(self.angle)
        self.update()

    def setPos(self, pos):

        if type(pos) in [list, tuple]:
            newPos = pos
        elif isinstance(pos, QtCore.QPointF):
            newPos = [pos.x(), pos.y()]
        else:
            if self.angle == 90:
                newPos = [pos, 0]
            elif self.angle == 0:
                newPos = [0, pos]
            else:
                raise Exception("Must specify 2D coordinate for non-orthogonal lines.")

        ## check bounds (only works for orthogonal lines)
        if self.angle == 90:
            if self.maxRange[0] is not None:
                newPos[0] = max(newPos[0], self.maxRange[0])
            if self.maxRange[1] is not None:
                newPos[0] = min(newPos[0], self.maxRange[1])
        elif self.angle == 0:
            if self.maxRange[0] is not None:
                newPos[1] = max(newPos[1], self.maxRange[0])
            if self.maxRange[1] is not None:
                newPos[1] = min(newPos[1], self.maxRange[1])

        if self.p != newPos:
            # print(f"setPos newPos {newPos}")
            self.p = newPos
            self._invalidateCache()
            GraphicsObject.setPos(self, Point(self.p))
            self.sigPositionChanged.emit(self)

    def getXPos(self):
        return self.p[0]

    def getYPos(self):
        return self.p[1]

    def getPos(self):
        return self.p

    def value(self):
        """Return the value of the line. Will be a single number for horizontal and
        vertical lines, and a list of [x,y] values for diagonal lines."""
        if self.angle % 180 == 0:
            return self.getYPos()
        elif self.angle % 180 == 90:
            return self.getXPos()
        else:
            return self.getPos()

    def setValue(self, v):
        """Set the position of the line. If line is horizontal or vertical, v can be
        a single value. Otherwise, a 2D coordinate must be specified (list, tuple and
        QPointF are all acceptable)."""
        self.setPos(v)

    ## broken in 4.7
    # def itemChange(self, change, val):
    # if change in [self.ItemScenePositionHasChanged, self.ItemSceneHasChanged]:
    # self.updateLine()
    # print "update", change
    # print self.getBoundingParents()
    # else:
    # print "ignore", change
    # return GraphicsObject.itemChange(self, change, val)

    def _invalidateCache(self):
        self._line = None
        self._boundingRect = None

    def boundingRect(self):
        if self._boundingRect is None:
            # br = UIGraphicsItem.boundingRect(self)
            br = self.viewRect()
            if br is None:
                return QtCore.QRectF()

            # We want to change the right and left value if a finite value has been given
            if (self._finite_values is not None) and (self.angle in [0, 90]):
                if br.right() > self._finite_values[1]:
                    br.setRight(self._finite_values[1])
                if br.left() < self._finite_values[0]:
                    br.setLeft(self._finite_values[0])


            ## add a 4-pixel radius around the line for mouse interaction.
            px = self.pixelLength(direction=Point(1, 0), ortho=True)  ## get pixel length orthogonal to the line
            if px is None:
                px = 0
            w = (max(4, self.pen.width() / 2, self.hoverPen.width() / 2) + 1) * px

            br.setBottom(-w)
            br.setTop(w)

            br = br.normalized()
            self._boundingRect = br
            self._line = QtCore.QLineF(br.right(), 0.0, br.left(), 0.0)
        return self._boundingRect

    def paint(self, p, *args):
        p.setPen(self.currentPen)
        # print(f"paint {self._line} self.p {self.p} self.pos() {self.pos()}")
        p.drawLine(self._line)

    def dataBounds(self, axis, frac=1.0, orthoRange=None):
        if axis == 0:
            return None  ## x axis should never be auto-scaled
        else:
            return (0, 0)

    def mouseDragEvent(self, ev):
        if self.movable and ev.button() == QtCore.Qt.LeftButton:
            if ev.isStart():
                self.moving = True
                self.cursorOffset = self.pos() - self.mapToParent(ev.buttonDownPos())
                self.startPosition = self.pos()
            ev.accept()

            if not self.moving:
                return
            # we want to forbid the line to move in its axis, it should be moving only orthogonaly
            # valid only for angle of 0 and 90
            new_pos = list(self.cursorOffset + self.mapToParent(ev.pos()))
            if self.angle == 90:
                if self.int_rounding:
                    new_pos[0] = round(new_pos[0])
                self.setPos([new_pos[0], self.p[1]])
                if self._new_line_pos_callback is not None:
                    self._new_line_pos_callback(new_pos=new_pos[0], first_value=self._first_line,
                                                time_interval=self.time_interval)
            elif self.angle == 0:
                if self.int_rounding:
                    new_pos[1] = round(new_pos[1])
                self.setPos([self.p[0], new_pos[1]])
                if self._new_line_pos_callback is not None:
                    self._new_line_pos_callback(new_pos=new_pos[1], first_value=self._first_line,
                                                time_interval=self.time_interval)
            else:
                self.setPos(new_pos)
            self.sigDragged.emit(self)
            if ev.isFinish():
                self.moving = False
                self.sigPositionChangeFinished.emit(self)

    def mouseClickEvent(self, ev):
        if self.moving and ev.button() == QtCore.Qt.RightButton:
            ev.accept()
            self.setPos(self.startPosition)
            self.moving = False
            self.sigDragged.emit(self)
            self.sigPositionChangeFinished.emit(self)

    def hoverEvent(self, ev):
        if (not ev.isExit()) and self.movable and ev.acceptDrags(QtCore.Qt.LeftButton):
            self.setMouseHover(True)
        else:
            self.setMouseHover(False)

    def setMouseHover(self, hover):
        ## Inform the item that the mouse is (not) hovering over it
        if self.mouseHovering == hover:
            return
        self.mouseHovering = hover
        if hover:
            self.currentPen = self.hoverPen
        else:
            self.currentPen = self.pen
        self.update()

    def viewTransformChanged(self):
        """
        Called whenever the transformation matrix of the view has changed.
        (eg, the view range has changed or the view was resized)
        """
        self._invalidateCache()

    def setName(self, name):
        self._name = name

    def name(self):
        return self._name


class fLineLabel(TextItem):
    """
    A TextItem that attaches itself to an InfiniteLine.

    This class extends TextItem with the following features:

    * Automatically positions adjacent to the line at a fixed position along
      the line and within the view box.
    * Automatically reformats text when the line value has changed.
    * Can optionally be dragged to change its location along the line.
    * Optionally aligns to its parent line.

    =============== ==================================================================
    **Arguments:**
    line            The InfiniteLine to which this label will be attached.
    text            String to display in the label. May contain a {value} formatting
                    string to display the current value of the line.
    movable         Bool; if True, then the label can be dragged along the line.
    position        Relative position (0.0-1.0) within the view to position the label
                    along the line.
    anchors         List of (x,y) pairs giving the text anchor positions that should
                    be used when the line is moved to one side of the view or the
                    other. This allows text to switch to the opposite side of the line
                    as it approaches the edge of the view. These are automatically
                    selected for some common cases, but may be specified if the
                    default values give unexpected results.
    =============== ==================================================================

    All extra keyword arguments are passed to TextItem. A particularly useful
    option here is to use `rotateAxis=(1, 0)`, which will cause the text to
    be automatically rotated parallel to the line.
    """

    def __init__(self, line, text="", movable=False, position=0.5, anchors=None, **kwds):
        self.line = line
        self.movable = movable
        self.moving = False
        self.orthoPos = position  # text will always be placed on the line at a position relative to view bounds
        self.format = text
        self.line.sigPositionChanged.connect(self.valueChanged)
        self._endpoints = (None, None)
        if anchors is None:
            # automatically pick sensible anchors
            rax = kwds.get('rotateAxis', None)
            if rax is not None:
                if tuple(rax) == (1, 0):
                    anchors = [(0.5, 0), (0.5, 1)]
                else:
                    anchors = [(0, 0.5), (1, 0.5)]
            else:
                if line.angle % 180 == 0:
                    anchors = [(0.5, 0), (0.5, 1)]
                else:
                    anchors = [(0, 0.5), (1, 0.5)]

        self.anchors = anchors
        TextItem.__init__(self, **kwds)
        self.setParentItem(line)
        self.valueChanged()

    def valueChanged(self):
        if not self.isVisible():
            return
        value = self.line.value()
        self.setText(self.format.format(value=value))
        self.updatePosition()

    def getEndpoints(self):
        # calculate points where line intersects view box
        # (in line coordinates)
        if self._endpoints[0] is None:
            lr = self.line.boundingRect()
            pt1 = Point(lr.left(), 0)
            pt2 = Point(lr.right(), 0)

            if self.line.angle % 90 != 0:
                # more expensive to find text position for oblique lines.
                view = self.getViewBox()
                if not self.isVisible() or not isinstance(view, ViewBox):
                    # not in a viewbox, skip update
                    return (None, None)
                p = QtGui.QPainterPath()
                p.moveTo(pt1)
                p.lineTo(pt2)
                p = self.line.itemTransform(view)[0].map(p)
                vr = QtGui.QPainterPath()
                vr.addRect(view.boundingRect())
                paths = vr.intersected(p).toSubpathPolygons(QtGui.QTransform())
                if len(paths) > 0:
                    l = list(paths[0])
                    pt1 = self.line.mapFromItem(view, l[0])
                    pt2 = self.line.mapFromItem(view, l[1])
            self._endpoints = (pt1, pt2)
        return self._endpoints

    def updatePosition(self):
        # update text position to relative view location along line
        self._endpoints = (None, None)
        pt1, pt2 = self.getEndpoints()
        if pt1 is None:
            return
        pt = pt2 * self.orthoPos + pt1 * (1 - self.orthoPos)
        self.setPos(pt)

        # update anchor to keep text visible as it nears the view box edge
        vr = self.line.viewRect()
        if vr is not None:
            self.setAnchor(self.anchors[0 if vr.center().y() < 0 else 1])

    def setVisible(self, v):
        TextItem.setVisible(self, v)
        if v:
            self.updateText()
            self.updatePosition()

    def setMovable(self, m):
        """Set whether this label is movable by dragging along the line.
        """
        self.movable = m
        self.setAcceptHoverEvents(m)

    def setPosition(self, p):
        """Set the relative position (0.0-1.0) of this label within the view box
        and along the line.

        For horizontal (angle=0) and vertical (angle=90) lines, a value of 0.0
        places the text at the bottom or left of the view, respectively.
        """
        self.orthoPos = p
        self.updatePosition()

    def setFormat(self, text):
        """Set the text format string for this label.

        May optionally contain "{value}" to include the lines current value
        (the text will be reformatted whenever the line is moved).
        """
        self.format = text
        self.valueChanged()

    def mouseDragEvent(self, ev):
        if self.movable and ev.button() == QtCore.Qt.LeftButton:
            if ev.isStart():
                self._moving = True
                self._cursorOffset = self._posToRel(ev.buttonDownPos())
                self._startPosition = self.orthoPos
            ev.accept()

            if not self._moving:
                return

            rel = self._posToRel(ev.pos())
            self.orthoPos = np.clip(self._startPosition + rel - self._cursorOffset, 0, 1)
            self.updatePosition()
            if ev.isFinish():
                self._moving = False

    def mouseClickEvent(self, ev):
        if self.moving and ev.button() == QtCore.Qt.RightButton:
            ev.accept()
            self.orthoPos = self._startPosition
            self.moving = False

    def hoverEvent(self, ev):
        if not ev.isExit() and self.movable:
            ev.acceptDrags(QtCore.Qt.LeftButton)

    def viewTransformChanged(self):
        self.updatePosition()
        TextItem.viewTransformChanged(self)

    def _posToRel(self, pos):
        # convert local position to relative position along line between view bounds
        pt1, pt2 = self.getEndpoints()
        if pt1 is None:
            return 0
        view = self.getViewBox()
        pos = self.mapToParent(pos)
        return (pos.x() - pt1.x()) / (pt2.x() - pt1.x())
