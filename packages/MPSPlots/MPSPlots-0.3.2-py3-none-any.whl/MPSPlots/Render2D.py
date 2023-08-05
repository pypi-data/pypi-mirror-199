#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Matplotlib imports
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.offsetbox import AnchoredText
from matplotlib import colors
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.path import Path

# Other imports
import numpy
import shapely.geometry as geo
from itertools import cycle
from dataclasses import dataclass
from . import CMAP


matplotlib.style.use('ggplot')
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams["font.family"] = "serif"
plt.rcParams['axes.edgecolor'] = 'black'


linecycler = cycle(["-", "--", "-.", ":"])


@dataclass
class ColorBar:
    color: str = 'viridis'
    """ colormap for the colorbar """
    discreet: bool = False
    position: str = 'left'
    orientation: str = "vertical"
    symmetric: bool = False
    log_norm: bool = False
    numeric_format: str = '%.3f'
    n_ticks: int = None
    label_size: int = None
    show: bool = True

    def _render_(self, ax, Scalar, image) -> None:
        if self.discreet:
            unique_values = numpy.unique(Scalar)
            Norm = colors.BoundaryNorm(unique_values, unique_values.size + 1, extend='both')
            image.set_norm(Norm)
            # ticks = numpy.unique(Scalar)
            # cbar = plt.colorbar(mappable=Image, norm=Norm, boundaries=ticks, cax=cax, orientation=self.orientation, format=self.numeric_format)

        elif self.log_norm and self.symmetric:
            Norm = matplotlib.colors.SymLogNorm(linthresh=1e-10)
            Norm.autoscale(Scalar)
            image.set_norm(Norm)

        elif self.log_norm and not self.symmetric:
            Norm = matplotlib.colors.LogNorm()
            Norm.autoscale(Scalar)
            image.set_norm(Norm)

        elif not self.log_norm and self.symmetric:
            Norm = matplotlib.colors.TwoSlopeNorm(
                vcenter=0,
                vmax=numpy.abs(Scalar).max(),
                vmin=-numpy.abs(Scalar).max()
            )

            image.set_norm(Norm)

        if ax.show_colorbar:
            self.construct_ax(ax=ax, image=image)

    def construct_ax(self, ax, image) -> None:
        divider = make_axes_locatable(ax._ax)

        colorbar_ax = divider.append_axes(self.position, size="10%", pad=0.15)

        cbar = plt.colorbar(
            mappable=image,
            norm=None,
            cax=colorbar_ax,
            orientation=self.orientation,
            format=self.numeric_format
        )

        if self.n_ticks is not None:
            cbar.ax.locator_params(nbins=self.n_ticks)
        if self.n_ticks is not None:
            cbar.ax.tick_params(labelsize=self.label_size)


@dataclass
class Contour:
    x: numpy.ndarray
    y: numpy.ndarray
    scalar: numpy.ndarray
    colormap: str = CMAP.BKR
    isolines: list = None
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """

    def _render_(self, ax) -> None:
        ax.contour(
            self.x * self.x_scale_factor,
            self.y * self.y_scale_factor,
            self.scalar,
            level=self.isolines,
            colors="black",
            linewidth=.5
        )

        ax.contourf(
            self.x * self.x_scale_factor,
            self.y * self.y_scale_factor,
            self.scalar,
            level=self.isolines,
            cmap=self.colormap,
            norm=colors.LogNorm()
        )


@dataclass
class Mesh:
    scalar: numpy.ndarray
    """ 2 dimensional numpy array representing the mesh to be plotted """
    colormap: str = CMAP.BKR
    """ Colormap to be used for the plot """
    x: numpy.ndarray = None
    """ Array representing the x axis, if not defined a numpy arrange is used instead """
    y: numpy.ndarray = None
    """ Array representing the y axis, if not defined a numpy arrange is used instead """
    show_colorbar: bool = True
    """ Boolean option to show or not the colorbar of the mesh """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """

    def __post_init__(self):
        if self.x is None:
            self.x = numpy.arange(self.scalar.shape[1])

        if self.y is None:
            self.y = numpy.arange(self.scalar.shape[0])

    def _render_(self, ax):
        image = ax._ax.pcolormesh(
            self.x * self.x_scale_factor,
            self.y * self.y_scale_factor,
            self.scalar,
            cmap=self.colormap,
            shading='auto',
            zorder=1
        )

        image.set_edgecolor('face')

        if ax.colorbar is not None:
            ax.colorbar.show = ax.show_colorbar
            ax.colorbar._render_(ax=ax, Scalar=self.scalar, image=image)

        return image


@dataclass
class Polygon:
    instance: object
    """ Shapely geo instance representing the polygone to be plotted """
    name: str = ''
    """ Name to be added to the plot next to the polygon """
    alpha: float = 0.4
    """ Opacity of the polygon to be plotted """
    facecolor: str = 'lightblue'
    """ Color for the interior of the polygon """
    edgecolor: str = 'black'
    """ Color for the border of the polygon """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """

    def _render_(self, ax):

        if isinstance(self.instance, geo.MultiPolygon):
            for polygon in self.instance.geoms:
                self.add_polygon_to_ax(polygon, ax)

        else:
            self.add_polygon_to_ax(self.instance, ax)

    def add_polygon_to_ax(self, polygon, ax, add_name: str = None):
        collection = self.get_polygon_path(polygon)
        ax._ax.add_collection(collection, autolim=True)
        ax._ax.autoscale_view()

        if add_name:
            ax._ax.scatter(polygon.centroid.x, polygon.centroid.y)
            ax._ax.text(polygon.centroid.x, polygon.centroid.y, self.name)

    def get_polygon_path(self, polygon):
        exterior_coordinate = numpy.asarray(polygon.exterior.coords)

        exterior_coordinate[:, 0] *= self.x_scale_factor
        exterior_coordinate[:, 1] *= self.y_scale_factor

        path_exterior = Path(exterior_coordinate)

        path_interior = []
        for ring in polygon.interiors:
            interior_coordinate = numpy.asarray(ring.coords)
            path_interior.append(Path(interior_coordinate))

        path = Path.make_compound_path(
            path_exterior,
            *path_interior
        )

        patch = PathPatch(path)

        collection = PatchCollection(
            [patch],
            alpha=self.alpha,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor
        )

        return collection


@dataclass
class FillLine:
    x: numpy.ndarray
    """ Array representing the x axis """
    y0: numpy.ndarray
    """ Array representing the inferior y axis to be filled with color """
    y1: numpy.ndarray
    """ Array representing the superior y axis to be filled with color """
    label: str = ""
    color: str = None
    """ Color for the fill """
    line_style: str = None
    """ Line style for the unique line default is next in cycle """
    show_outline: bool = True
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """

    def _render_(self, ax) -> None:
        if self.line_style is None:
            self.line_style = next(linecycler)

        ax._ax.fill_between(
            self.x * self.x_scale_factor,
            self.y0 * self.y_scale_factor,
            self.y1 * self.y_scale_factor,
            color=self.color,
            linestyle=self.line_style,
            alpha=0.7,
            label=self.label
        )

        if self.show_outline:
            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y1 * self.y_scale_factor,
                color='k',
                linestyle='-',
                linewidth=1
            )

            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y0 * self.y_scale_factor,
                color='k',
                linestyle='-',
                linewidth=1
            )


@dataclass
class STDLine:
    x: numpy.ndarray
    """ Array representing the x axis """
    y_mean: numpy.ndarray
    """ Array representing the mean value of y axis """
    y_std: numpy.ndarray
    """ Array representing the standard deviation value of y axis """
    label: str = ""
    """ Label to be added to the plot """
    color: str = None
    """ Color for the artist to be ploted """
    line_style: str = None
    """ Line style for the y_mean line default is straight lines '-' """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """

    def _render_(self, ax):
        if self.line_style is None:
            self.line_style = '-'

        y0 = self.y_mean - self.y_std / 2
        y1 = self.y_mean + self.y_std / 2

        line = ax._ax.plot(
            self.x * self.x_scale_factor,
            self.y_mean * self.y_scale_factor,
            color=self.color,
            linestyle=self.line_style
        )

        ax._ax.fill_between(
            self.x * self.x_scale_factor,
            y0 * self.y_scale_factor,
            y1 * self.y_scale_factor,
            color=line[-1].get_color(),
            linestyle='-',
            alpha=0.3,
            label=self.label
        )


@dataclass
class Line:
    y: numpy.ndarray
    """ Array representing the y axis """
    x: numpy.ndarray = None
    """ Array representing the x axis, if not defined a numpy arrange is used instead """
    label: str = None
    """ Label to be added to the plot """
    color: str = None
    """ Color for the artist to be ploted """
    line_style: str = None
    """ Line style for the unique line default is next in cycle """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """

    def __post_init__(self):
        if self.x is None:
            self.x = numpy.arange(self.y.size)

    def _render_(self, ax):
        if self.line_style is None:
            self.line_style = next(linecycler)

        if numpy.iscomplexobj(self.y):
            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y.real * self.y_scale_factor,
                label=self.label + "[real]",
                color=self.color,
                linestyle=self.line_style
            )

            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y.imag * self.y_scale_factor,
                label=self.label + "[imag]",
                color=self.color,
                linestyle=self.line_style
            )

        else:
            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y * self.y_scale_factor,
                label=self.label,
                color=self.color,
                linestyle=self.line_style
            )


@dataclass
class Text:
    position: tuple = (0.9, 0.9)
    font_size: int = 8
    text: str = ''

    def _render_(self, ax):
        art = AnchoredText(self.text,
                           loc='lower left',
                           prop=dict(size=self.font_size),
                           frameon=True,
                           bbox_to_anchor=(0.05, 1.0),
                           bbox_transform=ax._ax.transAxes)

        ax._ax.get_figure().add_artist(art)


@dataclass
class Scene2D:
    unit_size: tuple = (10, 3)
    tight_layout: bool = True
    title: str = ""

    def __post_init__(self):
        self.axis_generated = False
        self._axis = []
        self.nCols = None
        self.nRows = None

    def set_axis_row(self, value) -> None:
        for ax in self._axis:
            ax.row = value

    def set_axis_col(self, value) -> None:
        for ax in self._axis:
            ax.col = value

    def set_style(self, **style_dict):
        for ax in self:
            ax.set_style(**style_dict)

        return self

    @property
    def axis_matrix(self):
        ax_matrix = numpy.full(shape=(self.max_row + 1, self.max_col + 1), fill_value=None)
        for ax in self._axis:
            ax_matrix[ax.row, ax.col] = ax

        return ax_matrix

    @property
    def max_row(self) -> int:
        max_row = 0
        for ax in self._axis:
            max_row = ax.row if ax.row > max_row else max_row

        return max_row

    @property
    def max_col(self) -> int:
        max_col = 0
        for ax in self._axis:
            max_col = ax.col if ax.col > max_col else max_col

        return max_col

    def __getitem__(self, idx: int):
        return self._axis[idx]

    def __setitem__(self, idx: int, value) -> None:
        assert isinstance(value, Axis), f"Cannot assign type: {value.__class__} to Scene2D axis"
        self._axis[idx] = value

    def __add__(self, other):
        assert isinstance(other, Scene2D), f"Cannot add two different classes {self.__class__} and {other.__class__}"
        for ax in other._axis:
            self.append_axis(ax)

        return self

    def append_axis(self, ax):
        ax.row = self.max_row + 1 if self.max_row != 0 else 0
        ax.col = self.max_col + 1 if self.max_col != 0 else 0
        self._axis.append(ax)

    def ax_inherit(function):
        def wrapper(self, value):
            for ax in self:
                setattr(ax, function.__name__, value)

        return wrapper

    @ax_inherit
    def x_scale_factor(self, value: int):
        pass

    @ax_inherit
    def y_scale_factor(self, value: int):
        pass

    @ax_inherit
    def font_size(self, value: int):
        pass

    @ax_inherit
    def legend_font_size(self, value: int):
        pass

    @ax_inherit
    def tick_size(self, value: int):
        pass

    @ax_inherit
    def x_limits(self, value: list):
        pass

    @ax_inherit
    def y_limits(self, value: list):
        pass

    @ax_inherit
    def x_label(self, value: list):
        pass

    @ax_inherit
    def y_label(self, value: list):
        pass

    @ax_inherit
    def water_mark(self, value: str):
        pass

    @ax_inherit
    def equal(self, value: bool):
        pass

    @ax_inherit
    def equal_limits(self, value: bool):
        pass

    @ax_inherit
    def show_legend(self, value: bool):
        pass

    @ax_inherit
    def show_grid(self, value: bool):
        pass

    @ax_inherit
    def show_ticks(self, value: bool):
        pass

    @ax_inherit
    def show_colorbar(self, value: int):
        pass

    def colorbar_n_ticks(self, value: int):
        for ax in self:
            ax.colorbar.n_ticks = value

    def colorbar_label_size(self, value: int):
        for ax in self:
            ax.colorbar.label_size = value

    font_size = property(None, font_size)
    legend_font_size = property(None, legend_font_size)
    tick_size = property(None, tick_size)
    x_limits = property(None, x_limits)
    y_limits = property(None, y_limits)
    x_scale_factor = property(None, x_scale_factor)
    y_scale_factor = property(None, y_scale_factor)
    x_label = property(None, x_label)
    y_label = property(None, y_label)
    water_mark = property(None, water_mark)
    equal = property(None, equal)
    equal_limits = property(None, equal_limits)
    show_legend = property(None, show_legend)
    show_grid = property(None, show_grid)
    show_ticks = property(None, show_ticks)
    show_colorbar = property(None, show_colorbar)
    colorbar_n_ticks = property(None, colorbar_n_ticks)
    colorbar_label_size = property(None, colorbar_label_size)

    def add_axes(self, *axis):
        for ax in axis:
            self._axis.append(ax)

        return self

    def _generate_axis_(self):
        figure_size = [self.unit_size[0] * (self.max_col + 1), self.unit_size[1] * (self.max_row + 1)]
        self._mpl_figure = plt.figure(figsize=figure_size)
        self._mpl_figure.suptitle(self.title)

        grid = gridspec.GridSpec(ncols=self.max_col + 1, nrows=self.max_row + 1, figure=self._mpl_figure)

        ax_matrix = numpy.full(shape=(self.max_row + 1, self.max_col + 1), fill_value=None)

        for axis in self._axis:
            subplot = self._mpl_figure.add_subplot(grid[axis.row, axis.col], projection=axis.projection)
            ax_matrix[axis.row, axis.col] = subplot
            axis._ax = subplot

        self.axis_generated = True

        return self

    def auto_arrange_axis(self, type='row') -> None:
        if type == 'row':
            for n, ax in enumerate(self._axis):
                ax.row = n
                ax.col = 0
        else:
            for n, ax in enumerate(self._axis):
                ax.row = 0
                ax.col = n

    def _render_(self):
        if not self.axis_generated:
            self._generate_axis_()

        for ax in self._axis:
            ax._render_()

        if self.tight_layout:
            plt.tight_layout()

        return self

    def close(self) -> None:
        plt.close(self._mpl_figure)

    def show(self, save_directory: str = None, **kwargs):
        self._render_()
        if save_directory is not None:
            plt.savefig(fname=save_directory, **kwargs)

        plt.show()

        return self


@dataclass
class Axis:
    row: int
    col: int
    x_label: str = None
    y_label: str = None
    title: str = ''
    show_grid: bool = True
    show_legend: bool = False
    x_scale: str = 'linear'
    y_scale: str = 'linear'
    x_limits: list = None
    y_limits: list = None
    equal_limits: bool = False
    equal: bool = False
    colorbar: ColorBar = None
    water_mark: str = ''
    Figure: Scene2D = None
    projection: str = None
    font_size: int = 10
    tick_size: int = 10
    show_ticks: bool = True
    show_colorbar: bool = True
    legend_font_size: bool = 12
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """

    def __post_init__(self):
        self._ax = None
        self.Artist = []

    def __add__(self, other):
        self.Artist += other.Artist
        return self

    @property
    def style(self):
        return {'x_label': self.x_label,
                'y_label': self.y_label,
                'title': self.title,
                'show_grid': self.show_grid,
                'show_legend': self.show_legend,
                'x_scale': self.x_scale,
                'y_scale': self.y_scale,
                'x_limits': self.x_limits,
                'y_limits': self.y_limits,
                'equal_limits': self.equal_limits,
                'equal': self.equal,
                'colorbar': self.colorbar,
                'water_mark': self.water_mark,
                'projection': self.projection,
                'font_size': self.font_size,
                'legend_font_size': self.legend_font_size,
                'tick_size': self.tick_size}

    def copy_style(self, other):
        assert isinstance(other, self), f"Cannot copy style from other class {other.__class__}"
        for element, value in other.style.items():
            setattr(self, element, value)

    def add_artist(self, *Artist):
        for art in Artist:
            self.Artist.append(art)

    def set_style(self, **style_dict):
        for element, value in style_dict.items():
            setattr(self, element, value)

        return self

    def _render_(self):
        for artist in self.Artist:
            artist.x_scale_factor = self.x_scale_factor
            artist.y_scale_factor = self.y_scale_factor

            artist.show_colorbar = self.show_colorbar
            artist._render_(self)

        if self.x_limits is not None:
            self._ax.set_xlim(self.x_limits)

        if self.y_limits is not None:
            self._ax.set_ylim(self.y_limits)

        if self.equal_limits:
            self.set_equal_limits()

        self._decorate_ax_()

    def set_equal_limits(self) -> None:
        min_limit = numpy.min([*self._ax.get_xlim(), *self._ax.get_ylim()])
        max_limit = numpy.max([*self._ax.get_xlim(), *self._ax.get_ylim()])

        self._ax.set_xlim([min_limit, max_limit])
        self._ax.set_ylim([min_limit, max_limit])

    def _decorate_ax_(self):
        if self.show_legend:
            self._ax.legend(fancybox=True, facecolor='white', edgecolor='k', fontsize=self.legend_font_size - 4)

        if self.x_label is not None:
            self._ax.set_xlabel(self.x_label, fontsize=self.font_size)

        if self.y_label is not None:
            self._ax.set_ylabel(self.y_label, fontsize=self.font_size)

        if self.title is not None:
            self._ax.set_title(self.title, fontsize=self.font_size)

        if self.x_scale is not None:
            self._ax.set_xscale(self.x_scale)

        if self.y_scale is not None:
            self._ax.set_yscale(self.y_scale)

        if self.tick_size is not None:
            self._ax.tick_params(labelsize=self.tick_size)

        if self.equal:
            self._ax.set_aspect("equal")

        if self.show_grid:
            self._ax.grid(self.show_grid)

        self._ax.axes.get_xaxis().set_visible(self.show_ticks)
        self._ax.axes.get_yaxis().set_visible(self.show_ticks)

        if self.water_mark is not None:
            self._ax.text(0.5, 0.1, self.water_mark, transform=self._ax.transAxes,
                    fontsize=30, color='white', alpha=0.2,
                    ha='center', va='baseline')


def Multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)

    for fig in figs:
        fig._mpl_figure.savefig(pp, format='pdf')

    pp.close()


# -
