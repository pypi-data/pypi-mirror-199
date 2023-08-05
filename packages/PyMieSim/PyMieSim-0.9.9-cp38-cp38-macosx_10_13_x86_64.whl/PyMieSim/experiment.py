#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

from DataVisual import Xparameter
from DataVisual import DataV

from PyMieSim import load_lp_mode

from PyMieSim.polarization import LinearPolarization
from PyMieSim.binary.Experiment import CppExperiment

from PyMieSim.binary.Sets import (
    CppCoreShellSet,
    CppCylinderSet,
    CppSphereSet,
    CppSourceSet,
    CppDetectorSet
)


@dataclass
class CoreShellSet():
    core_diameter: list
    """ diameter of the core of the single scatterer [m]. """
    shell_diameter: list
    """ diameter of the shell of the single scatterer [m]. """
    core_index: tuple = tuple()
    """ Refractive index of the core of the scatterer. """
    shell_index: tuple = tuple()
    """ Refractive index of the shell of the scatterer. """
    core_material: tuple = tuple()
    """ Core material of which the scatterer is made of. Only if core_index is not specified.  """
    shell_material: tuple = tuple()
    """ Shell material of which the scatterer is made of. Only if shell_index is not specified.  """
    n_medium: list = 1.0
    """ Refractive index of scatterer medium. """
    name: str = 'coreshell'
    """name of the set """

    def __post_init__(self):
        self.format_inputs()

        self.bounded_core = True if len(self.core_material) != 0 else False
        self.bounded_shell = True if len(self.shell_material) != 0 else False

        self.core_diameter = Xparameter(
            values=self.core_diameter,
            name='diameter',
            format=".2e",
            unit="m",
            long_label='diameter',
            short_label='diameter'
        )

        self.shell_diameter = Xparameter(
            values=self.shell_diameter,
            name='Shell diameter',
            format=".2e",
            unit="m",
            long_label='Shell diameter',
            short_label='Shell diameter'
        )

        self.core_material = Xparameter(
            values=self.core_material,
            name='core_material',
            format="",
            unit="",
            long_label='core_material',
            short_label='core_material'
        )

        self.shell_material = Xparameter(
            values=self.shell_material,
            name='shell_material',
            format="",
            unit="",
            long_label='shell_material',
            short_label='shell_material'
        )

        self.core_index = Xparameter(
            values=self.core_index,
            name='core_index',
            format="",
            unit="1",
            long_label='core_index',
            short_label='core_index'
        )

        self.shell_index = Xparameter(
            values=self.shell_index,
            name='shell_index',
            format="",
            unit="1",
            long_label='shell_index',
            short_label='shell_index'
        )

        self.n_medium = Xparameter(
            values=self.n_medium,
            name='n_medium',
            long_label='n_medium',
            format=".2f",
            unit="1",
            short_label='n_medium'
        )

    def bind_to_experiment(self, experiment):
        """
        Bind this specific set to a Setup experiment.

        :param      experiment:  The experiment
        :type       experiment:  Setup

        :returns:   No return
        :rtype:     None
        """
        experiment.binding.set_coreshell(self.binding)

    def bind_0(self, source):
        core_material = [
            material.GetRI(source.values) for material in self.core_material
        ]

        shell_material = [
            material.GetRI(source.values) for material in self.shell_material
        ]

        core_material = numpy.asarray(core_material).astype(complex)
        shell_material = numpy.asarray(shell_material).astype(complex)

        self.binding = CppCoreShellSet(
            core_diameter=self.core_diameter.values,
            shell_diameter=self.shell_diameter.values,
            core_material=core_material,
            shell_material=shell_material,
            n_medium=self.n_medium.values
        )

    def bind_1(self, source):
        core_material = [
            material.GetRI(source.values) for material in self.core_material
        ]

        core_material = numpy.asarray(core_material).astype(complex)

        self.binding = CppCoreShellSet(
            core_diameter=self.core_diameter.values,
            shell_diameter=self.shell_diameter.values,
            core_material=core_material,
            shell_index=self.shell_index.values,
            n_medium=self.n_medium.values
        )

    def bind_2(self, source):
        shell_material = [
            material.GetRI(source.values) for material in self.shell_material
        ]

        shell_material = numpy.asarray(shell_material).astype(complex)

        self.binding = CppCoreShellSet(
            core_diameter=self.core_diameter.values,
            shell_diameter=self.shell_diameter.values,
            core_index=self.core_index.values,
            shell_material=shell_material,
            n_medium=self.n_medium.values
        )

    def bind_3(self, source):
        self.binding = CppCoreShellSet(
            core_diameter=self.core_diameter.values,
            shell_diameter=self.shell_diameter.values,
            core_index=self.core_index.values,
            shell_index=self.shell_index.values,
            n_medium=self.n_medium.values
        )

    def evaluate_index_material(self, source):
        if self.bounded_core and self.bounded_shell:
            self.bind_0(source)

        if self.bounded_core and not self.bounded_shell:
            self.bind_1(source)

        if not self.bounded_core and self.bounded_shell:
            self.bind_2(source)

        if not self.bounded_core and not self.bounded_shell:
            self.bind_3(source)

    def format_inputs(self):
        """
        Format the inputs given by the user into numpy array. Those inputs are subsequently
        sent to the cpp binding.

        :returns:   No return
        :rtype:     None
        """
        self.core_diameter = numpy.atleast_1d(self.core_diameter).astype(float)
        self.shell_diameter = numpy.atleast_1d(self.shell_diameter).astype(float)

        self.core_index = numpy.atleast_1d(self.core_index).astype(numpy.complex128)
        self.shell_index = numpy.atleast_1d(self.shell_index).astype(numpy.complex128)

        self.n_medium = numpy.atleast_1d(self.n_medium).astype(float)

        self.core_material = numpy.atleast_1d(self.core_material)
        self.shell_material = numpy.atleast_1d(self.shell_material)

    def append_to_table(self, table):
        """
        Append elements to the xTable from the DataVisual library for the plottings.

        :param      table:  The table
        :type       table:  list

        :returns:   The updated list
        :rtype:     list
        """
        if self.bounded_core and self.bounded_shell:
            return [*table, self.core_diameter, self.shell_diameter, self.core_material, self.shell_material, self.n_medium]

        if self.bounded_core and not self.bounded_shell:
            return [*table, self.core_diameter, self.shell_diameter, self.core_material, self.shell_index, self.n_medium]

        if not self.bounded_core and self.bounded_shell:
            return [*table, self.core_diameter, self.shell_diameter, self.core_index, self.shell_material, self.n_medium]

        if not self.bounded_core and not self.bounded_shell:
            return [*table, self.core_diameter, self.shell_diameter, self.core_index, self.shell_index, self.n_medium]


@dataclass
class SphereSet():
    diameter: list
    """ diameter of the single scatterer in unit of meter. """
    index: list = tuple()
    """ Refractive index of scatterer. """
    material: list = tuple()
    """ material of which the scatterer is made of. Only if index is not specified. """
    n_medium: list = 1.0
    """ Refractive index of scatterer medium. """
    name: str = 'sphere'
    """name of the set """

    def __post_init__(self):
        self.format_inputs()

        self.bounded_index = True if len(self.material) != 0 else False

        self.diameter = Xparameter(
            values=self.diameter,
            name='diameter',
            format=".2e",
            unit="m",
            long_label='diameter',
            short_label='diameter'
        )

        self.material = Xparameter(
            values=self.material,
            name='material',
            format="",
            unit="",
            long_label='material',
            short_label='material'
        )

        self.index = Xparameter(
            values=self.index,
            name='index',
            format="",
            unit="1",
            long_label='index',
            short_label='index'
        )

        self.n_medium = Xparameter(
            values=self.n_medium,
            name='n_medium',
            long_label='n_medium',
            format=".2f",
            unit="1",
            short_label='n_medium'
        )

    def bind_to_experiment(self, experiment):
        """
        Bind this specific set to a Setup experiment.

        :param      experiment:  The experiment
        :type       experiment:  Setup

        :returns:   No return
        :rtype:     None
        """
        experiment.binding.set_sphere(self.binding)

    def evaluate_index_material(self, Source):
        if self.bounded_index:
            material = [
                material.GetRI(Source.values) for material in self.material
            ]

            material_index = numpy.asarray(material).astype(complex)

            self.binding = CppSphereSet(
                diameter=self.diameter.values.astype(float),
                material=material_index,
                n_medium=self.n_medium.values.astype(float)
            )

        else:
            self.binding = CppSphereSet(
                diameter=self.diameter.values,
                index=self.index.values,
                n_medium=self.n_medium.values
            )

    def append_to_table(self, table):
        """
        Append elements to the xTable from the DataVisual library for the plottings.

        :param      table:  The table
        :type       table:  list

        :returns:   The updated list
        :rtype:     list
        """
        if self.bounded_index:
            return [*table, self.diameter, self.material, self.n_medium]

        else:
            return [*table, self.diameter, self.index, self.n_medium]

    def format_inputs(self):
        """
        Format the inputs given by the user into numpy array. Those inputs are subsequently
        sent to the cpp binding.

        :returns:   No return
        :rtype:     None
        """
        self.diameter = numpy.atleast_1d(self.diameter).astype(float)

        self.index = numpy.atleast_1d(self.index).astype(numpy.complex128)

        self.n_medium = numpy.atleast_1d(self.n_medium).astype(float)

        self.material = numpy.atleast_1d(self.material)


@dataclass
class CylinderSet():
    diameter: list
    """ diameter of the single scatterer in unit of meter. """
    index: tuple = tuple()
    """ Refractive index of scatterer. """
    material: tuple = tuple()
    """ Refractive index of scatterer medium. """
    n_medium: list = 1.0
    """ material of which the scatterer is made of. Only if index is not specified. """
    name: str = 'cylinder'
    """name of the set """

    def __post_init__(self):
        self.format_inputs()

        self.bounded_index = True if len(self.material) != 0 else False

        self.diameter = Xparameter(
            values=self.diameter,
            name='diameter',
            format=".2e",
            unit="m",
            long_label='diameter',
            short_label='diameter'
        )

        self.material = Xparameter(
            values=self.material,
            name='material',
            format="",
            unit="",
            long_label='material',
            short_label='material'
        )

        self.index = Xparameter(
            values=self.index,
            name='index',
            format="",
            unit="1",
            long_label='index',
            short_label='index'
        )

        self.n_medium = Xparameter(
            values=self.n_medium,
            name='n_medium',
            long_label='n_medium',
            format=".2f",
            unit="1",
            short_label='n_medium'
        )

    def bind_to_experiment(self, experiment):
        """
        Bind this specific set to a Setup experiment.

        :param      experiment:  The experiment
        :type       experiment:  Setup

        :returns:   No return
        :rtype:     None
        """
        experiment.binding.set_cylinder(self.binding)

    def evaluate_index_material(self, Source):
        if self.bounded_index:
            material = numpy.asarray([material.GetRI(Source.values) for material in self.material])

            self.binding = CppCylinderSet(
                diameter=self.diameter.values.astype(float),
                material=material.astype(complex),
                n_medium=self.n_medium.values.astype(float)
            )

        else:
            self.binding = CppCylinderSet(
                diameter=self.diameter.values,
                index=self.index.values,
                n_medium=self.n_medium.values
            )

    def append_to_table(self, table):
        """
        Append elements to the xTable from the DataVisual library for the plottings.

        :param      table:  The table
        :type       table:  list

        :returns:   The updated list
        :rtype:     list
        """
        if self.bounded_index:
            return [*table, self.diameter, self.material, self.n_medium]

        else:
            return [*table, self.diameter, self.index, self.n_medium]

    def format_inputs(self):
        """
        Format the inputs given by the user into numpy array. Those inputs are subsequently
        sent to the cpp binding.

        :returns:   No return
        :rtype:     None
        """
        self.diameter = numpy.atleast_1d(self.diameter).astype(float)

        self.index = numpy.atleast_1d(self.index).astype(numpy.complex128)

        self.n_medium = numpy.atleast_1d(self.n_medium).astype(float)

        self.material = numpy.atleast_1d(self.material)


@dataclass
class SourceSet(object):
    wavelength: float = 1.0
    """ Wavelenght of the light field. """
    polarization: float = None
    """ polarization of the light field in degree. """
    amplitude: float = None
    """ Maximal value of the electric field at focus point. """
    name: str = 'PlaneWave'
    """ name of the set """

    def __post_init__(self):
        self.format_inputs()

        self.wavelength = Xparameter(
            values=self.wavelength,
            name='wavelength',
            long_label='wavelength',
            format=".1e",
            unit="m",
            short_label='wavelength'
        )

        self.polarization = Xparameter(
            values=self.jones_vector,
            representation=self.polarization.angle_list,
            name='polarization',
            long_label='polarization',
            format=".1f",
            unit="Deg",
            short_label='polarization'
        )

        self.amplitude = Xparameter(
            values=self.amplitude,
            name='amplitude',
            long_label='amplitude',
            format=".1e",
            unit="w.m⁻¹",
            short_label='amplitude'
        )

        self.binding = CppSourceSet(
            wavelength=self.wavelength.values,
            jones_vector=self.jones_vector,
            amplitude=self.amplitude.values
        )

    def format_inputs(self):
        """
        Format the inputs given by the user into numpy array. Those inputs are subsequently
        sent to the cpp binding.

        :returns:   No return
        :rtype:     None
        """
        if numpy.iterable(self.polarization):
            self.polarization = LinearPolarization(*self.polarization)
        else:
            self.polarization = LinearPolarization(self.polarization)

        self.wavelength = numpy.atleast_1d(self.wavelength).astype(float)

        self.amplitude = numpy.atleast_1d(self.amplitude).astype(float)

        self.jones_vector = numpy.atleast_1d(self.polarization.jones_vector).astype(numpy.complex128).T

    def bind_to_experiment(self, experiment):
        """
        Bind this specific set to a Setup experiment.

        :param      experiment:  The experiment
        :type       experiment:  Setup

        :returns:   No return
        :rtype:     None
        """
        experiment.binding.set_source(self.binding)

    def append_to_table(self, table):
        """
        Append elements to the xTable from the DataVisual library for the plottings.

        :param      table:  The table
        :type       table:  list

        :returns:   The updated list
        :rtype:     list
        """
        return [*table, self.wavelength, self.polarization, self.amplitude]


@dataclass
class PhotodiodeSet():
    NA: list
    """ Numerical aperture of imaging system. """
    gamma_offset: list
    """ Angle [degree] offset of detector in the direction perpendicular to polarization. """
    phi_offset: list
    """ Angle [degree] offset of detector in the direction parallel to polarization. """
    polarization_filter: list
    """ Angle [degree] of polarization filter in front of detector. """
    coupling_mode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    coherent: bool = False
    """ Describe the detection scheme coherent or uncoherent. """
    sampling: int = 200
    """ Sampling number for the field evaluation. """
    name = "Photodiode"
    """ name of the set """

    def __post_init__(self):
        self.format_inputs()
        self.scalarfield = numpy.ones([1, self.sampling])

        self.scalarfield = Xparameter(
            values=self.scalarfield,
            representation=numpy.asarray(['Photodiode']),
            name='Field',
            long_label='Coupling field',
            format="",
            unit="",
            short_label='C.F'
        )

        self.NA = Xparameter(
            values=self.NA,
            name='NA',
            long_label='Numerical aperture',
            format=".3f",
            unit="rad",
            short_label='NA'
        )

        self.phi_offset = Xparameter(
            values=self.phi_offset,
            name='phi_offset',
            long_label='Phi offset',
            format="03.1f",
            unit="deg",
            short_label='Phi offset'
        )

        self.gamma_offset = Xparameter(
            values=self.gamma_offset,
            name='gamma_offset',
            long_label='Gamma offset',
            format="03.1f",
            unit="deg",
            short_label='Gamma offset'
        )

        self.polarization_filter = Xparameter(
            values=self.polarization_filter,
            name='polarization_filter',
            long_label=r'filter$_{pol}$',
            format="03.1f",
            unit="deg",
            short_label=r'filter$_{pol}$',
        )

        self.initialize_binding()

    def initialize_binding(self):
        point_coupling = True if self.coupling_mode == 'Point' else False
        phi_offset_rad = numpy.deg2rad(self.phi_offset.values)
        gamma_offset_rad = numpy.deg2rad(self.gamma_offset.values)

        self.binding = CppDetectorSet(
            scalarfield=self.scalarfield.values,
            NA=self.NA.values,
            phi_offset=phi_offset_rad,
            gamma_offset=gamma_offset_rad,
            filter=self.polarization_filter.values,
            point_coupling=point_coupling,
            coherent=self.coherent
        )

    def bind_to_experiment(self, experiment):
        """
        Bind this specific set to a Setup experiment.

        :param      experiment:  The experiment
        :type       experiment:  Setup

        :returns:   No return
        :rtype:     None
        """
        experiment.binding.set_detector(self.binding)

    def append_to_table(self, table):
        """
        Append elements to the xTable from the DataVisual library for the plottings.

        :param      table:  The table
        :type       table:  list

        :returns:   The updated list
        :rtype:     list
        """
        return [*table, self.scalarfield, self.NA, self.phi_offset, self.gamma_offset, self.polarization_filter]

    def format_inputs(self):
        """
        Format the inputs given by the user into numpy array. Those inputs are subsequently
        sent to the cpp binding.

        :returns:   No return
        :rtype:     None
        """
        self.NA = numpy.atleast_1d(self.NA).astype(float)

        self.phi_offset = numpy.atleast_1d(self.phi_offset).astype(float)

        self.gamma_offset = numpy.atleast_1d(self.gamma_offset).astype(float)

        self.polarization_filter = numpy.atleast_1d(self.polarization_filter).astype(float)


@dataclass
class LPModeSet():
    mode_number: list
    """ List of mode to be used. """
    NA: list
    """ Numerical aperture of imaging system. """
    gamma_offset: list
    """ Angle [degree] offset of detector in the direction perpendicular to polarization. """
    phi_offset: list
    """ Angle [degree] offset of detector in the direction parallel to polarization. """
    polarization_filter: list
    """ Angle [degree] of polarization filter in front of detector. """
    coupling_mode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    coherent: bool = True
    """ Describe the detection scheme coherent or uncoherent. """
    sampling: int = 200
    """ Sampling number for the field evaluation. """
    name = "LPMode"
    """ name of the set """

    def __post_init__(self):

        self.format_inputs()

        representation = [f"LP$_{{{mode.replace('-','')}}}$" for mode in self.mode_number]
        self.scalarfield = Xparameter(
            values=self.get_fields_array(),
            representation=representation,
            name='Field',
            long_label='Coupling field',
            format="",
            unit="",
            short_label='C.F'
        )

        self.NA = Xparameter(
            values=self.NA,
            name='NA',
            long_label='Numerical aperture',
            format=".3f",
            unit="Rad",
            short_label='NA'
        )

        self.phi_offset = Xparameter(
            values=self.phi_offset,
            name='phi_offset',
            long_label='Phi offset',
            format="03.1f",
            unit="Deg",
            short_label='Phi offset'
        )

        self.gamma_offset = Xparameter(
            values=self.gamma_offset,
            name='gamma_offset',
            long_label='Gamma offset',
            format="03.1f",
            unit="Deg",
            short_label='Gamma offset'
        )

        self.polarization_filter = Xparameter(
            values=self.polarization_filter,
            name='polarization_filter',
            long_label='polarization_filter',
            format="03.1f",
            unit="Deg",
            short_label='polarization_filter angle'
        )

        self.initialize_binding()

    def get_fields_array(self) -> numpy.ndarray:
        """
        Gets the field arrays for the detection schemes the first dimension is the different fields.
        Second dimension are the individual mode fields.

        :returns:   The fields array.
        :rtype:     numpy.ndarray
        """
        fields_array = [
            load_lp_mode(
                mode_number=mode,
                sampling=self.sampling,
                type='unstructured'
            ) for mode in self.mode_number
        ]

        return numpy.asarray(fields_array).astype(numpy.complex128)

    def initialize_binding(self) -> None:
        """
        Initializes the cpp binding of the LPmode detector set.

        :returns:   No return
        :rtype:     None
        """
        point_coupling = True if self.coupling_mode == 'Point' else False
        phi_offset_rad = numpy.deg2rad(self.phi_offset.values)
        gamma_offset_rad = numpy.deg2rad(self.gamma_offset.values)

        self.binding = CppDetectorSet(
            scalarfield=self.scalarfield.values,
            NA=self.NA.values,
            phi_offset=phi_offset_rad,
            gamma_offset=gamma_offset_rad,
            filter=self.polarization_filter.values,
            point_coupling=point_coupling,
            coherent=self.coherent
        )

    def bind_to_experiment(self, experiment) -> None:
        """
        Bind this specific set to a Setup experiment.

        :param      experiment:  The experiment
        :type       experiment:  Setup

        :returns:   No return
        :rtype:     None
        """
        experiment.binding.set_detector(self.binding)

    def append_to_table(self, table: list) -> list:
        """
        Append elements to the xTable from the DataVisual library for the plottings.

        :param      table:  The table
        :type       table:  list

        :returns:   The updated list
        :rtype:     list
        """
        return [*table, self.scalarfield, self.NA, self.phi_offset, self.gamma_offset, self.polarization_filter]

    def format_inputs(self) -> None:
        """
        Format the inputs given by the user into numpy array. Those inputs are subsequently
        sent to the cpp binding.

        :returns:   No return
        :rtype:     None
        """
        self.mode_number = numpy.atleast_1d(self.mode_number).astype(str)

        self.NA = numpy.atleast_1d(self.NA).astype(float)

        self.phi_offset = numpy.atleast_1d(self.phi_offset).astype(float)

        self.gamma_offset = numpy.atleast_1d(self.gamma_offset).astype(float)

        self.polarization_filter = numpy.atleast_1d(self.polarization_filter).astype(float)


class Setup(object):
    def __init__(self, scatterer_set, source_set, detector_set=None):

        self.source_set = source_set

        self.detector_set = detector_set

        self.scatterer_set = scatterer_set

        self.scatterer_set.evaluate_index_material(self.source_set.wavelength)

        self.binding = CppExperiment()

        self.bind_sets_to_experiment()

        self.x_table = self.source_set.append_to_table(table=[])
        self.x_table = self.scatterer_set.append_to_table(table=self.x_table)

        if self.detector_set is not None:
            self.x_table = self.detector_set.append_to_table(table=self.x_table)

    def bind_sets_to_experiment(self):
        self.source_set.bind_to_experiment(self)
        self.scatterer_set.bind_to_experiment(self)

        if self.detector_set:
            self.detector_set.bind_to_experiment(self)

    def Get(self, measures: list) -> DataV:
        """
        Compute the measure provided and return a DataV structured array.

        :param      measures:  The measures
        :type       measures:  list

        :returns:   The data structure.
        :rtype:     DataV
        """
        measures = numpy.atleast_1d(measures)

        self.y_table = measures

        array = []
        for measure in measures:
            measure.values = numpy.array([])

            measure = 'get' + "_" + self.scatterer_set.name + "_" + measure.name

            sub_array = getattr(self.binding, measure)()

            array.append(sub_array)

        array = numpy.asarray(array)

        for n, e in enumerate(self.x_table):
            e.position = n + 1

        return DataV(array, x_table=self.x_table, y_table=self.y_table)


# -
