import math
from dataclasses import dataclass
from typing import Callable
import numpy as np
from scipy import optimize

"""
Important:
Most of these functions refer to the measurement procedure described in section 2.2 of my paper.
I recommend using the paper as a reference.
"""


@dataclass
class MeasuredCharacteristicParameters:
    """
    Class that stores the measured characteristic parameters
    (in the paper the values are labelled with a tilde)
    If the approach described in section 2.2 is used,
    the ranges are (see section 2.3 "Measurement ranges"):
        delta: [rad] 0-pi
        theta: [rad] 0-pi/4 (but cannot distinguish between fast and slow axis)
        omega: [rad] 0-pi/2

    Attributes:
        delta: [rad]
        theta: [rad]
        omega: [rad]

    """
    delta: float
    theta: float
    omega: float


class MeasuredNormalizedStokesParameters:
    """
    This class refers to the measured normalized Stokes Parameters used in section 2.2 "Measurement Procedure".
    Let the incident linearly polarized light be oriented at angle phi.
    S0, S1, S2, S3 are the resulting and measured Stokes parameters (Step 2. in section 2.2).
    The Stokes Parameters will be normalized in the constructor.
    """

    def __init__(self, phi: float, S0: float, S1: float, S2: float, S3: float | None = None):
        """

        Args:
            phi: orientation angle of the incident linearly polarized light
            S0: Measured total Intensity (will become =1 after initialization)
            S1: Measured S1 Stokes parameter
            S2: Measured S2 Stokes parameter
            S3: (if available), measured S3 Stkes parameter
        """

        self.phi = phi
        self.S0 = 1
        self.S1 = S1 / S0
        self.S2 = S2 / S0
        if S3:
            self.S3 = S3 / S0
        else:
            self.S3 = None


def get_theta_within_the_specified_measurement_range(theta: float) -> float:
    """
    In section 2.3 the measurement range for theta was specified as [0, pi/2).
    Because theta can be periodically continued, it is possible to use the boundaries [0, pi]
    when searching for the minimum of the residual function R. This improved the optimization procedure.
    However, we would like theta to be within our specified range again.
    See the explanation in the supplemental document, Equations (S7)-(S9).

    Args:
        theta: measured theta value

    Returns: measured value in the range [0, pi/2)

    """
    if math.isclose(theta, math.pi / 2):
        return 0
    else:
        return theta % (math.pi / 2)


def get_omega_within_the_specified_measurement_range(omega: float) -> float:
    """
    In section 2.3 the measurement range for omega was specified as [0, pi).
    Because omega can be periodically continued, it is possible to use the boundaries [0, 2pi]
    when searching for the minimum of the residual function R. This improved the optimization procedure.
    However, we would like omega to be within our specified range again.
    See the explanation in the supplemental document, Equations (S7)-(S9).

    Args:
        omega: measured omega value

    Returns: measured value in the range [0, pi/2)

    """
    if math.isclose(omega, math.pi):
        return 0
    else:
        return omega % math.pi


def define_function_that_finds_minimum_of_R_function(
        lb_delta: float = 0, ub_delta: float = math.pi,
        lb_theta: float = 0, ub_theta: float = math.pi,
        lb_omega: float = 0, ub_omega: float = 2 * math.pi,
        strategy: str = "rand1exp") -> Callable[[Callable], optimize.OptimizeResult]:
    """
    This function returns a function, that finds the minimum (using differential evolution) of the
    residual function R(x) wit x=[delta, theta, omega]

    Args:
        lb_delta: lower boundary of delta (0 is default)
        ub_delta: upper boundary of delta (pi is default)
        lb_theta: lower boundary of theta (0 is default)
        ub_theta: upper boundary of theta (pi is default -
                  Attention, this is twice the measurement range but improves the optimization procedure)
        lb_omega: lower boundary of omega (0 is default)
        ub_omega: upper boundary of omega (2pi is default -
                  Attention, this is twice the measurement range but improves the optimization procedure)
        strategy: see scipy.optimize.differential_evolution Manual

    Returns: function that finds the minimum of R(x) wit x=[delta, theta, omega]

    """

    def find_minimum_of_R_function(residual_func_R: Callable) -> optimize.OptimizeResult:
        """
        This function finds the minimum of the residual function R(x) with x=[delta, theta, omega]

        Args:
            residual_func_R: R(x) with x=[delta, theta, omega]

        Returns: OptimizeResults

        """
        return optimize.differential_evolution(func=residual_func_R,
                                               bounds=((lb_delta, ub_delta),
                                                       (lb_theta, ub_theta),
                                                       (lb_omega, ub_omega)),
                                               strategy=strategy)

    return find_minimum_of_R_function


def outgoing_S1(phi, delta, theta, omega) -> float:
    """
    See section 2.1 "Governing equations" S1(phi, delta, theta, omega)

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


def outgoing_S2(phi, delta, theta, omega) -> float:
    """
    See section 2.1 "Governing equations" S2(phi, delta, theta, omega)

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


def define_residual_function_R(
        list_of_measured_stokes_parameters: list[MeasuredNormalizedStokesParameters]
) -> Callable[[list[float, float, float]], float]:
    """
    Following the procedure outlined in section 2.2:
        - For each angle phi, the corresponding Stokes Parameters are measured.
          The results are Stored in the class "MeasuredNormalizedStokesParameters".
        - This is repeated for several angles phis.
        - All the results are passed as a list to this function.
        - This function then generates the Residual function R(x) with x=[delta, theta, omega].

    Args:
        list_of_measured_stokes_parameters: list of measurement results

    Returns: Residual function R(x) with x=[delta, theta, omega]

    """

    def residual_function_R(x) -> float:
        """
        Defines the residual function R (see section 2.2)

        Args:

            x: list with [delta, theta, omega], all in [rad]

        Returns: the Euclidean Norm of the residual vector (see section 2.2)

        """
        delta = x[0]
        theta = x[1]
        omega = x[2]

        residual_vector = []

        for measurement in list_of_measured_stokes_parameters:
            residual_vector.append(measurement.S1 - outgoing_S1(phi=measurement.phi,
                                                                delta=delta, theta=theta, omega=omega))
            residual_vector.append(measurement.S2 - outgoing_S2(phi=measurement.phi,
                                                                delta=delta, theta=theta, omega=omega))

        return np.linalg.norm(residual_vector, ord=2)

    return residual_function_R


def calculate_characteristic_parameters(
        list_of_measured_stokes_parameters: list[MeasuredNormalizedStokesParameters],
        function_that_finds_minimum_of_R_function=define_function_that_finds_minimum_of_R_function(),
) -> MeasuredCharacteristicParameters:
    """

    Args:
        list_of_measured_stokes_parameters: list of measurement results
        function_that_finds_minimum_of_R_function: function that finds the minimum of R(x) with x=[delta, theta, omega]

    Returns: MeasuredCharacteristicParameters class

    """

    residual_function_R = define_residual_function_R(list_of_measured_stokes_parameters)

    optimization_result = function_that_finds_minimum_of_R_function(residual_function_R)

    delta_tilde = optimization_result.x[0]
    theta_tilde = get_theta_within_the_specified_measurement_range(optimization_result.x[1])
    omega_tilde = get_omega_within_the_specified_measurement_range(optimization_result.x[2])

    return MeasuredCharacteristicParameters(delta=delta_tilde,
                                            theta=theta_tilde,
                                            omega=omega_tilde)
