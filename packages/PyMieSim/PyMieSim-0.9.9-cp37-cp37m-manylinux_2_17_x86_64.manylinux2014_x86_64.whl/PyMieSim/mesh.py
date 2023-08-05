#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

from PyMieSim.binary.Fibonacci import FIBONACCI
from MPSPlots.Render3D import Scene3D
from MPSPlots.Math import Angle


@dataclass
class FibonacciMesh():
    """
    Class wich represent an angular mesh. The distribution of points inside
    the mesh is similar to a Fibonacci sphere where each point cover an
    equivalent solid angle.
    """
    max_angle: float = 1.5
    """ Angle in radian defined by the numerical aperture of the imaging system. """
    sampling: int = 1000
    """Number of point distrubuted inside the Solid angle defined by the numerical aperture. """
    phi_offset: float = 0.
    """ Angle offset in the parallel direction of the polarization of incindent light. """
    gamma_offset: float = 0.
    """ Angle offset in the perpendicular direction of the polarization of incindent light. """

    def __post_init__(self):
        self.structured = False

        self._para = None
        self._perp = None

        self._parallel_vector_in_plan = None
        self._perpendicular_vector_in_plan = None

        self._vertical_to_perpendicular_vector = None
        self._horizontal_to_perpendicular_vector = None
        self._vertical_to_parallel_vector = None
        self._horizontal_to_parallel_vector = None

        self._phi = None
        self._theta = None

        self._plan = None

        self.vertical_vector = numpy.array([1, 0, 0])
        self.horizontal_vector = numpy.array([0, 1, 0])
        self.generate_ledeved_mesh()

    @property
    def plan(self):
        if self._plan is None:
            self.cpp_binding.Computeplan()
            self._plan = numpy.asarray([self.cpp_binding.Xplan, self.cpp_binding.Yplan, self.cpp_binding.Zplan])

        return self._plan

    @property
    def perpendicular_vector(self):
        if self._perp is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.perpVector

    @property
    def parallel_vector(self):
        if self._para is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.paraVector

    @property
    def horizontal_to_perpendicular(self):
        if self._horizontal_to_perpendicular_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.horizontal_to_perpendicular_vector

    @property
    def horizontal_to_parallel(self):
        if self._horizontal_to_parallel_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.horizontal_to_parallel_vector

    @property
    def vertical_to_perpendicular(self):
        if self._vertical_to_perpendicular_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.perpVector

    @property
    def vertical_to_parallel(self):
        if self._vertical_to_parallel_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.paraVector

    @property
    def parallel_plan(self):
        if self._parallel_vector_in_plan is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.paraVectorZplanar

    @property
    def perpendicular_plan(self):
        if self._perpendicular_vector_in_plan is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.perpVectorZplanar

    @property
    def phi(self):
        if not self._phi:
            self._phi = Angle(self.cpp_binding.phi, Unit='Radian')
            return self._phi
        else:
            return self._phi

    @property
    def theta(self):
        if not self._theta:
            self._theta = Angle(self.cpp_binding.theta, Unit='Radian')
            return self._theta
        else:
            return self._theta

    @property
    def X(self):
        return self.cpp_binding.x

    @property
    def Y(self):
        return self.cpp_binding.y

    @property
    def Z(self):
        return self.cpp_binding.z

    def _make_properties_(self):

        self.CartMesh = numpy.asarray([self.cpp_binding.x, self.cpp_binding.y, self.cpp_binding.z])

        self.d_omega = Angle(0, Unit='Radian')
        self.d_omega.Radian = self.cpp_binding.d_omega
        self.d_omega.Degree = self.cpp_binding.d_omega * (180 / numpy.pi)**2

        self.omega = Angle(0, Unit='Radian')
        self.omega.Radian = self.cpp_binding.omega
        self.omega.Degree = self.cpp_binding.omega * (180 / numpy.pi)**2

    def projection_HV_vector(self) -> tuple:
        parallel_projection = [
            self.projection_on_base_vector(
                Vector=self.vertical_to_parallel_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        perpendicular_projection = [
            self.projection_on_base_vector(
                Vector=self.vertical_to_perpendicular_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        return numpy.array(parallel_projection), numpy.array(perpendicular_projection)

    def projection_HV_scalar(self) -> tuple:
        parallel_projection = [
            self.projection_on_base_scalar(
                Vector=self.vertical_to_perpendicular_in_z_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        perpendicular_projection = [
            self.projection_on_base_scalar(
                Vector=self.vertical_to_perpendicular_in_z_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        return numpy.array(parallel_projection), numpy.array(perpendicular_projection)

    def projection_on_base_scalar(self, vector: numpy.ndarray, base_vector: numpy.ndarray) -> numpy.ndarray:
        return vector.dot(base_vector)

    def projection_on_base_vector(self, vector: numpy.ndarray, base_vector: numpy.ndarray) -> numpy.ndarray:
        projection = self.projection_on_base_scalar(vector, base_vector)

        base_projection = numpy.outer(projection, base_vector)

        return base_projection

    def plot(self) -> None:
        figure = Scene3D(shape=(1, 1))
        self._add_mesh_to_ax_(figure=figure, plot_number=(0, 0))

        return figure

    def _add_mesh_to_ax_(self, figure, plot_number: tuple) -> None:
        Coordinate = numpy.array([self.X, self.Y, self.Z])

        figure.Add_Unstructured(Plot=plot_number,
                                Coordinate=Coordinate,
                                color="k")

        figure.__add_unit_sphere__(Plot=plot_number)
        figure.__add_axes__(Plot=plot_number)
        figure.__add__text__(Plot=plot_number, Text='Mesh grid')

    def generate_ledeved_mesh(self) -> None:
        self.cpp_binding = FIBONACCI(
            self.sampling,
            self.max_angle,
            numpy.deg2rad(self.phi_offset),
            numpy.deg2rad(self.gamma_offset)
        )

        self._make_properties_()


# -
