import numpy as np


def S_lin(phi: float) -> np.ndarray:
    """

    Args:
        phi: [rad] 0-pi orientation angle of the linearly polarized Stokes vector

    Returns: 4x1 Stokes vector of linearly polarized light oriented at angle phi

    """
    return np.array([1, np.cos(2 * phi), np.sin(2 * phi), 0])


def S_circ_rh() -> np.ndarray:
    """

    Returns: 4x1 Stokes vector of right-hand circularly polarized light

    """
    return np.array([1, 0, 0, 1])

def XR(delta: float, theta: float, omega: float) -> np.ndarray:
    """
    Models the optically equivalent model composed of two Mueller matrices:
    a rotator R(omega), and a linear retarder X(delta, theta) -> X*R

    Args:
        delta: [rad] absolut phase difference induced by the linear retarder
        theta: [rad] (-pi/2, pi/2] position of the fast axis of the linear retarder
        omega: [rad] (-pi/2, pi/2] angle of the rotation matrix

    Returns: 4x4 Mueller matrix X(delta, theta) * R(omega)

    """
    R = np.array([[1, 0, 0, 0, ],
                  [0, np.cos(2 * omega), - np.sin(2 * omega), 0],
                  [0, np.sin(2 * omega), np.cos(2 * omega), 0],
                  [0, 0, 0, 1]])
    X = np.array([[1, 0, 0, 0],
                  [0,
                   np.cos(2 * theta) ** 2 + np.sin(2 * theta) ** 2 * np.cos(delta),
                   np.sin(2 * theta) * np.cos(2 * theta) * (1 - np.cos(delta)),
                   -np.sin(delta) * np.sin(2 * theta)],
                  [0,
                   (1 - np.cos(delta)) * np.sin(2 * theta) * np.cos(2 * theta),
                   np.sin(2 * theta) ** 2 + np.cos(2 * theta) ** 2 * np.cos(delta), np.sin(delta) * np.cos(2 * theta)],
                  [0, np.sin(delta) * np.sin(2 * theta), -np.sin(delta) * np.cos(2 * theta), np.cos(delta)]])
    return X.dot(R)

