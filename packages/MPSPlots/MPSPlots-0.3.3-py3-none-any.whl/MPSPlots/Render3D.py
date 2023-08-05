#   !/usr/bin/env python
# -*- coding: utf-8 -*-

import pyvista
import numpy
import matplotlib
from MPSPlots.CMAP import BKR


class Scene3D:
    def __init__(self,
                 shape: tuple = (1, 1),
                 unit_size: tuple = (800, 800),
                 window_size: tuple = None,
                 **kwargs):

        if window_size is None:
            window_size = (unit_size[1] * shape[1], unit_size[0] * shape[0])

        self.figure = pyvista.Plotter(
            theme=pyvista.themes.DocumentTheme(),
            window_size=window_size,
            shape=shape,
            **kwargs
        )

    def add_unstructured_mesh(self,
                              coordinates: numpy.ndarray,
                              scalar: numpy.ndarray = None,
                              plot_number: tuple = (0, 0),
                              color_map: str = BKR,
                              scalar_bar_args: dict = None,
                              symmetric_map: bool = True) -> None:

        self.figure.subplot(*plot_number)
        coordinates = numpy.array(coordinates).T
        points = pyvista.wrap(coordinates)

        if symmetric_map:
            max_abs = numpy.abs(scalar).max()
            if max_abs == 0:
                color_map_limit = [-1, 1]
            else:
                color_map_limit = [-max_abs, max_abs]
        else:
            color_map_limit = None

        self.figure.add_points(
            points,
            scalars=scalar,
            point_size=20,
            render_points_as_spheres=True,
            cmap=color_map,
            clim=color_map_limit,
            scalar_bar_args=scalar_bar_args
        )

    def add_mesh(self,
                 coordinates: numpy.ndarray,
                 plot_number: tuple = (0, 0),
                 cmap: str = BKR,
                 **kwargs) -> None:

        if isinstance(cmap, str):  # works only for matplotlib 3.6.1
            cmap = matplotlib.colormaps[cmap]

        self.figure.subplot(*plot_number)
        mesh = pyvista.StructuredGrid(*coordinates)

        self.figure.add_mesh(mesh=mesh, cmap=cmap, **kwargs)

        return self.figure

    def add_theta_vector_field(self, plot_number: list, radius: float = 1.03 / 2):
        self.figure.subplot(*plot_number)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        theta_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, Radius, [1], [0], [0])], axis=1)

        spherical_vector = pyvista.grid_from_sph_coords(theta, phi, radius)

        spherical_vector.point_data["Theta"] = theta_vector * 0.1

        vectors = spherical_vector.glyph(
            orient="Theta",
            scale="Theta",
            tolerance=0.005
        )

        self.figure.add_mesh(vectors, color='k')

    def add_phi_vector_field(self, plot_number: tuple, radius: float = 1.03 / 2):
        self.figure.subplot(*plot_number)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        Phi_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, Radius, [0], [1], [0])], axis=1)

        spherical_vector = pyvista.grid_from_sph_coords(theta, phi, radius)

        spherical_vector.point_data["Phi"] = Phi_vector * 0.1

        vectors = spherical_vector.glyph(
            orient="Phi",
            scale="Phi",
            tolerance=0.005
        )

        self.figure.add_mesh(vectors, color='k')

    def add_r_vector_field(self, plot_number: tuple, R: float = [1.03 / 2]):
        self.figure.subplot(*plot_number)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        R_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, R, *[0, 0, 1])], axis=1)

        spherical_vector = pyvista.grid_from_sph_coords(theta, phi, R)

        spherical_vector.point_data["R"] = R_vector * 0.1

        vectors = spherical_vector.glyph(
            orient="R",
            scale="R",
            tolerance=0.005
        )

        self.figure.add_mesh(vectors, color='k')

    def add_unit_sphere_to_ax(self, plot_number: tuple = (0, 0), **kwargs):
        self.figure.subplot(*plot_number)
        sphere = pyvista.Sphere(radius=1)
        self.figure.add_mesh(sphere, opacity=0.3)

    def add_unit_axes_to_ax(self, plot_number: tuple = (0, 0)):
        self.figure.subplot(*plot_number)
        self.figure.add_axes_at_origin(labels_off=True)

    def add_text_to_axes(self, plot_number: tuple = (0, 0), text='', **kwargs):
        self.figure.subplot(*plot_number)
        self.figure.add_text(text, **kwargs)

    def show(self, SaveDir: str = None):
        self.figure.show(screenshot=SaveDir)

        return self

    def close(self):
        self.figure.close()
