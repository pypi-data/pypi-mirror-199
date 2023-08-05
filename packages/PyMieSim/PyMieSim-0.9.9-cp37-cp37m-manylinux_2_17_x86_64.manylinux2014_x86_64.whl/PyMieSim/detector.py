#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import logging
from dataclasses import dataclass

from PyMieSim.representations import Footprint
from PyMieSim.mesh import FibonacciMesh
from PyMieSim.binary.DetectorInterface import BindedDetector
from PyMieSim import load_lp_mode

from MPSPlots.Render3D import Scene3D
from MPSPlots.Math import NA_to_angle


@dataclass
class GenericDetector():
    r"""
    .. note::
        Detector type class representing a photodiode, light coupling is
        thus independant of the phase of the latter.
    """
    scalar_field: numpy.ndarray
    """ Array representing the detection field distribution. """
    NA: float
    """ Numerical aperture of imaging system. """
    gamma_offset: float
    """ Angle [Degree] offset of detector in the direction perpendicular to polarization. """
    phi_offset: float
    """ Angle [Degree] offset of detector in the direction parallel to polarization. """
    filter: float
    """ Angle [Degree] of polarization filter in front of detector. """
    coupling_mode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    coherent: bool = False
    """ Describe the detection scheme coherent or uncoherent. """

    def __post_init__(self):
        self.sampling = self.scalar_field.size
        self.max_angle = NA_to_angle(self.NA)

        self.Mesh = FibonacciMesh(
            max_angle=self.max_angle,
            sampling=self.sampling,
            phi_offset=self.phi_offset,
            gamma_offset=self.gamma_offset
        )

    def _get_binding_(self):
        self.cpp_binding = BindedDetector(
            scalar_field=self.scalar_field,
            NA=self.NA,
            phi_offset=numpy.deg2rad(self.phi_offset),
            gamma_offset=numpy.deg2rad(self.gamma_offset),
            filter=numpy.nan if self.filter is None else numpy.deg2rad(self.filter),
            coherent=self.coherent,
            point_coupling=True if self.coupling_mode == 'point_coupling' else False
        )

    def get_structured_scalarfield(self):
        return numpy.ones([self.sampling, self.sampling])

    def Coupling(self, scatterer):
        r"""
        .. note::
            Return the value of the scattererd light coupling as computed as:

            .. math::
                |\iint_{\Omega}  \Phi_{det} \,\, \Psi_{scat}^* \,  d \Omega|^2

            | Where:
            |   :math:`\Phi_{det}` is the capturing field of the detector and
            |   :math:`\Psi_{scat}` is the scattered field.

        Parameters
        ----------
        Scatterer : :class:`Scatterer`
            Scatterer instance (sphere, cylinder, ...).

        Returns
        -------
        :class:`float`
            Value of the coupling.

        """

        return getattr(self.cpp_binding, "Coupling" + type(scatterer).__name__)(scatterer.Bind)

    def get_footprint(self, scatterer):
        r"""
        .. note::
            Return the footprint of the scattererd light coupling with the
            detector as computed as:

            .. math::
                \big| \mathscr{F}^{-1} \big\{ \tilde{ \psi } (\xi, \nu),\
                       \tilde{ \phi}_{l,m}(\xi, \nu)  \big\}
                       (\delta_x, \delta_y) \big|^2

            | Where:
            |   :math:`\Phi_{det}` is the capturing field of the detector and
            |   :math:`\Psi_{scat}` is the scattered field.

        Parameters
        ----------
        Scatterer : :class:`Scatterer`.
            Scatterer instance (sphere, cylinder, ...).

        Returns
        -------
        :class:`Footprint`.
            Dictionnary subclass with all pertienent information.

        """
        return Footprint(scatterer=scatterer, detector=self)

    def plot(self):
        r"""
        .. note::
            Method that plot the real part of the scattered field
            (:math:`E_{\theta}` and :math:`E_{\phi}`).

        """
        Coordinate = numpy.array([self.Mesh.X, self.Mesh.Y, self.Mesh.Z])

        figure = Scene3D(shape=(1, 2), window_size=[1800, 1000])

        for plot_number, scalar, name in zip([(0, 0), (0, 1)],
                                      [self.scalar_field.real, self.scalar_field.imag],
                                      ['Real', 'Imaginary']):

            figure.add_unstructured_mesh(
                plot_number=plot_number,
                coordinates=Coordinate,
                scalar=scalar,
                color="tan",
                scalar_bar_args={'title': f'{name} field'}
            )

            figure.__add_unit_sphere__(plot_number=plot_number)
            figure.__add_axes__(plot_number=plot_number)

        return figure


class Photodiode(GenericDetector):
    Description = "[Photodiode]"

    def __init__(self, NA, sampling, gamma_offset, phi_offset, filter=None):

        super().__init__(
            scalar_field=numpy.ones(sampling).astype(complex),
            NA=NA,
            phi_offset=phi_offset,
            gamma_offset=gamma_offset,
            filter=filter,
            coherent=False,
            coupling_mode='Point'
        )

        self._get_binding_()


class IntegratingSphere(GenericDetector):
    Description = "[Integration sphere]"

    def __init__(self, sampling, filter=None):

        super().__init__(
            scalar_field=numpy.ones(sampling).astype(complex),
            NA=2,
            phi_offset=0,
            gamma_offset=0,
            filter=filter,
            coherent=False,
            coupling_mode='Point'
        )

        self._get_binding_()


class LPmode(GenericDetector):
    Description = "[LP mode detector]"

    def __init__(self,
                 mode_number: str,
                 NA: float,
                 gamma_offset: float,
                 phi_offset: float,
                 sampling: int = 200,
                 rotation: float = 0,
                 filter: float = None,
                 coupling_mode: str = 'Point'):

        if NA > 0.3 or NA < 0:
            logging.warning("High values of NA do not comply with paraxial approximation. Value under 0.3 are prefered.")

        self.mode_number = mode_number

        mode_field = load_lp_mode(
            mode_number=self.mode_number,
            type='unstructured',
            sampling=sampling
        )

        super().__init__(
            scalar_field=mode_field.astype(complex),
            NA=NA,
            phi_offset=phi_offset,
            gamma_offset=gamma_offset,
            filter=filter,
            coherent=True,
            coupling_mode=coupling_mode
        )

        self._get_binding_()

    def get_structured_scalarfield(self):
        return load_lp_mode(self.mode_number, type='structured'),


# -
