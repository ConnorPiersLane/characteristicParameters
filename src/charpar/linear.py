import math
from dataclasses import dataclass
from typing import Callable
import numpy as np
from scipy import optimize


@dataclass()
class Charparas_tilde:
    """
    Relative values of the Characteristic Parameters
    Index R indicates that these are "relative" values
    Attributes:
        delta_tilde: [rad]
        theta_tilde: [rad]
        omega_tilde: [rad]
    """
    delta_tilde: float
    theta_tilde: float
    omega_tilde: float


def R_pi(delta: float) -> float:
    """
    Describes the relation between actual, absolute phase difference and measurable, relative, phase difference
    when using linearly polarized incident light

    Args:
        delta: [rad] absolute phase difference of a linear retarder

    Returns: [rad] 0-pi relative phase difference

    """
    if delta % (2 * math.pi) < math.pi:
        return delta % math.pi
    else:
        return math.pi - (delta % math.pi)


class MeasuredStokesParameters:
    def __init__(self, phis: list[float], S_1s: list[float], S_2s: list[float]):
        """

        Args:
            phis:
            S_1s:
            S_2s:
        """
        if not len(phis) == len(S_1s) == len(S_2s):
            raise ValueError("All Input parameters must have the same length")
        self.phis = phis
        self.S_1s = S_1s
        self.S_2s = S_2s


def make_de_optimization(lb_delta: float = 0, ub_delta: float = math.pi,
                    lb_theta: float = 0, ub_theta: float = math.pi,
                    lb_omega: float = 0, ub_omega: float = 2 * math.pi,
                    strategy: str = "rand1exp") -> Callable[[Callable], optimize.OptimizeResult]:
    def de_optimization(func: Callable) -> optimize.OptimizeResult:
        return optimize.differential_evolution(func=func,
                                               bounds=((lb_delta, ub_delta),
                                                       (lb_theta, ub_theta),
                                                       (lb_omega, ub_omega)),
                                               strategy=strategy)

    return de_optimization


def calc_charparas(measured_stokes_parameters: MeasuredStokesParameters,
                   optimization: Callable[[Callable], optimize.OptimizeResult] = make_de_optimization(),
                   ) -> Charparas_tilde:

    residual_norm = generate_residual_vector_norm(
        phis=measured_stokes_parameters.phis,
        S_1s=measured_stokes_parameters.S_1s,
        S_2s=measured_stokes_parameters.S_2s)

    result = optimization(residual_norm)

    return Charparas_tilde(delta_tilde=result.x[0],
                           theta_tilde=result.x[1],
                           omega_tilde=result.x[2])


def S1(phi, delta, theta, omega) -> float:
    """

    Args:
        phi: [rad]
        delta: [rad]
        theta: [rad]
        omega: [rad]

    Returns: S1 parameter in the range 0-1

    """
    A = 2 * (phi + omega)
    B = A - 4 * theta
    return 0.5 * (math.cos(A) * (1 + math.cos(delta)) +
                  math.cos(B) * (1 - math.cos(delta)))


def S2(phi, delta, theta, omega) -> float:
    """

    Args:
        phi: [rad]
        delta: [rad]
        theta: [rad]
        omega: [rad]

    Returns: S2 parameter in the range 0-1

    """
    A = 2 * (phi + omega)
    B = A - 4 * theta
    return 0.5 * (math.sin(A) * (1 + math.cos(delta)) -
                  math.sin(B) * (1 - math.cos(delta)))


def generate_residual_vector_norm(phis: list[float],
                                  S_1s: list[float],
                                  S_2s: list[float]
                                  ) -> Callable[[list], float]:
    """

    Args:
        phis: [rad] list of orientation angles of the incident linearly polarized light
        S_1s: [rad] list of measured Stokes parameters S1 associated with the corresponding orientation angle
        S_2s: [rad] list of measured Stokes parameters S2 associated with the corresponding orientation angle

    Returns: Residual vector norm as a function of (delta, theta, omega)

    """

    def residual_vector_norm(x) -> float:
        """

        Args:

            x: list with [delta, theta, omega], all in [rad]

        Returns: residual vector norm

        """
        delta = x[0]
        theta = x[1]
        omega = x[2]

        vector = []

        for (phi, S_1, S_2) in zip(phis, S_1s, S_2s):
            vector.append(S_1 - S1(phi=phi, delta=delta, theta=theta, omega=omega))
            vector.append(S_2 - S2(phi=phi, delta=delta, theta=theta, omega=omega))

        return np.linalg.norm(vector, ord=1)

    return residual_vector_norm
