"""

LP02 Mode detector
==================

"""


def run():
    from PyMieSim.detector import LPmode

    Detector = LPmode(Mode="0-2",
                      rotation=0.,
                      sampling=300,
                      NA=0.3,
                      gamma_offset=30,
                      phi_offset=0,
                      coupling_mode='Point')

    Detector.plot().show()


if __name__ == '__main__':
    run()
