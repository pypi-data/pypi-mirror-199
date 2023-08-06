import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from qtpy import QtWidgets


class MplWidget(QtWidgets.QWidget):
    """A PyQt/Pyside widget that contains a matplotlib figure"""

    #: Matplotlib figure
    figure: Figure
    #: Figure canvas
    canvas: FigureCanvas

    def __init__(self, figure: Figure = None, toolbar: bool = True, parent=None, *args, **kwargs):
        """Create a new Matplotlib widget

        Parameters
        ----------
        figure : matplotlib.figure.Figure, optional
            Figure to use, by default None
        toolbar : bool, optional
            Whether to show the toolbar, by default True
        parent : QtWidgets.QWidget, optional
            Parent widget, by default None
        args, kwargs
            Additional arguments passed to the QWidget constructor
        """
        super().__init__(parent, *args, **kwargs)

        # Figure elements
        self.figure = figure or plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self) if toolbar else None

        # Layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def draw(self):
        """Redraw the figure"""
        self.canvas.draw()
