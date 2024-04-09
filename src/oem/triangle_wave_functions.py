import math

def T_pi(delta: float) -> float:
    """
    Triangle wave function with Period 2pi; Amplitude pi/2; and a y-shift of pi/2.
    Starts at (0,0)
    Source: https://en.wikipedia.org/wiki/Triangle_wave

    Args:
        delta: [rad]

    Returns: [rad] [0-pi]

    """

    return abs(((delta-math.pi) % (2*math.pi))-math.pi)


def T_pi_2(delta) -> float:
    """
    Triangle wave function with Period pi; Amplitude pi/4; and a y-shift of pi/4.
    Starts at (0,0)
    Source: https://en.wikipedia.org/wiki/Triangle_wave

    Args:
        delta: [rad]

    Returns: [rad] [0-pi/2]

    """

    return abs(((delta - math.pi/2) % (math.pi)) - math.pi/2)
