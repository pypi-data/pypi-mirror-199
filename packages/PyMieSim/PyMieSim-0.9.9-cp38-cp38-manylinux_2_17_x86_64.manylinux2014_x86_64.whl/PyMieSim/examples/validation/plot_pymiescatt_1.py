"""
=========================
PyMieSim vs PyMieScatt: 1
=========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.tools.directories import validation_data_path
from PyMieSim.experiment import SourceSet, SphereSet, Setup
from PyMieSim import measure


theoretical = numpy.genfromtxt(f"{validation_data_path}/PyMieScattQsca.csv", delimiter=',')

diameter = numpy.geomspace(10e-9, 6e-6, 800)

scatterer_set = SphereSet(
    diameter=diameter,
    index=1.4,
    n_medium=1.
)

source_set = SourceSet(
    wavelength=632.8e-9,
    polarization=[0],
    amplitude=1
)

experiment = Setup(
    scatterer_set=scatterer_set,
    source_set=source_set,
    detector_set=None
)

data = experiment.Get(measures=measure.Qsca)
data = data._data.squeeze()

plt.figure(figsize=(8, 4))
plt.plot(diameter, data, 'C1-', linewidth=3, label='PyMieSim')

plt.plot(diameter, theoretical, 'k--', linewidth=1, label='PyMieScatt')

plt.xlabel(r'diameter [$\mu$m]')
plt.ylabel('Scattering efficiency [Sphere]')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

assert numpy.all(numpy.isclose(data, theoretical, 1e-9)), 'Error: mismatch on PyMieScatt calculation occuring'


# -
