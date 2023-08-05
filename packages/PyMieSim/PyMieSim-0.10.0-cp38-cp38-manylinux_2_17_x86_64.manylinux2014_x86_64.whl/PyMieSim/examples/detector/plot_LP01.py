"""

LP01 Mode detector
==================

"""

from PyMieSim.detector import LPmode

detector = LPmode(
    mode_number="0-1",
    rotation=0.,
    sampling=300,
    NA=0.3,
    gamma_offset=0,
    phi_offset=40,
    coupling_mode='Point'
)

figure = detector.plot()

figure.show()

# -
