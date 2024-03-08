import math


def R_pi_2(delta) -> float:
    """
    Describes the relation between actual, absolute phase difference and measurable, relative, phase difference
    when using circularly polarized incident light

    Args:
        delta: [rad] absolute phase difference of a linear retarder

    Returns: [rad] 0-pi/2 relative phase difference

    """

    return abs(((delta - math.pi/2) % (math.pi)) - math.pi/2)

    ## Alternative 1
    # if delta % math.pi < math.pi/2:
    #     return delta % (math.pi / 2)
    # else:
    #     return math.pi/2 - (delta % (math.pi / 2))

    ## Alternative 2
    # return math.pi / 4 + 0.5*math.asin(math.sin(2*delta - math.pi/2))