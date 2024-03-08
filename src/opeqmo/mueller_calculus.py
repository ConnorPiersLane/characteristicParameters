import numpy as np


def linearly_polarized_light(phi: float) -> np.ndarray:
    """

    Args:
        phi: [rad] 0-pi orientation angle of the linearly polarized Stokes vector

    Returns: 4x1 Stokes vector of linearly polarized light oriented at angle phi

    """
    return np.array([1, np.cos(2 * phi), np.sin(2 * phi), 0])


def right_hand_circularly_polarized_light() -> np.ndarray:
    """

    Returns: 4x1 Stokes vector of right-hand circularly polarized light

    """
    return np.array([1, 0, 0, 1])



def rotator(omega: float) -> np.ndarray:
    """
    Generates a Mueller Rotation Matrix with:
        [1, 0, 0, 0;
        0 cos(2*omega) -sin(2*omega), 0;
        0 sin(2*omega) cos(2*omega), 0;
        0, 0, 0, 1]

    Source: see page 72 and 166 in
            "Chipman, R., Lam, W. S. T., & Young, G. (2018). Polarized light and optical systems. CRC press."

    Args:
        omega: [rad] rotation relative to the coordinate axes

    Returns: 4x4 numpy matrix of the Mueller matrix rotator model

    """
    return np.array([[1, 0, 0, 0, ],
                     [0, np.cos(2 * omega), - np.sin(2 * omega), 0],
                     [0, np.sin(2 * omega), np.cos(2 * omega), 0],
                     [0, 0, 0, 1]])


def linear_retarder(delta: float, theta: float) -> np.ndarray:
    """
    Definition can be found in:
    page 169 in "Chipman, R., Lam, W. S. T., & Young, G. (2018). Polarized light and optical systems. CRC press."

    Args:
        delta: [rad] retardance
        theta: [rad] orientation of the fast axis

    Returns: 4x4 numpy matrix of the Muller matrix linear retarder model

    """
    return np.array([[1, 0, 0, 0],
                     [0,
                      np.cos(2 * theta) ** 2 + np.sin(2 * theta) ** 2 * np.cos(delta),
                      np.sin(2 * theta) * np.cos(2 * theta) * (1 - np.cos(delta)),
                      -np.sin(delta) * np.sin(2 * theta)],
                     [0,
                      (1 - np.cos(delta)) * np.sin(2 * theta) * np.cos(2 * theta),
                      np.sin(2 * theta) ** 2 + np.cos(2 * theta) ** 2 * np.cos(delta),
                      np.sin(delta) * np.cos(2 * theta)],
                     [0, np.sin(delta) * np.sin(2 * theta), -np.sin(delta) * np.cos(2 * theta), np.cos(delta)]])


def optical_equivalent_model(delta: float, theta: float, omega: float) -> np.ndarray:
    """
    Models the optically equivalent model composed of two Mueller matrices:
    linear_retarder(delta, theta) * rotator(omega)

    Args:
        delta: [rad] retardance of the linear retarder
        theta: [rad] position of the fast axis of the linear retarder
        omega: [rad] rotation of the rotation matrix

    Returns: 4x4 Mueller matrix X(delta, theta) * R(omega)

    """
    R = rotator(omega)
    X = linear_retarder(delta=delta, theta=theta)
    return np.matmul(X, R)
