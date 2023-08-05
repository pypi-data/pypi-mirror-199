"""

LP11 Mode detector
==================

"""


def run():
    from PyMieSim.detector import LPmode

    Detector = LPmode(Mode="1-1",
                      rotation=0.,
                      sampling=300,
                      NA=0.3,
                      gamma_offset=0,
                      phi_offset=40,
                      coupling_mode='Point')

    Detector.plot().show()


if __name__ == '__main__':
    run()
