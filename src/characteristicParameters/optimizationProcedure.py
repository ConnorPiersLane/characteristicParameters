import math
from dataclasses import dataclass

import numpy as np
from scipy import optimize

"""
Important:
Most of these functions refer to the measurement procedure described in section 2.2 of the paper.
It is recommended to use the paper as a reference.
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


class MeasuredStokesVector:
    """
    This class refers to the measured outgoing Stokes Parameters used in section 2.2 "Measurement Procedure".
    Let the incident linearly polarized light be oriented at angle phi.
    S0, S1, S2, S3 are the measured outgoing Stokes parameters (Step 2. in section 2.2).
    The Stokes Parameters will be normalized in the constructor.
    S3 is optional
    """

    def __init__(self, phi: float, stokes_vector: list[float] | np.ndarray):
        """

        Args:
            phi: [rad] orientation angle of the incident linearly polarized light
            stokes_vector: Stokes vector [S0, S1, S2, S3] or [S0, S1, S2], not necessarily normalized
        """

        self.phi = phi

        # Not normalized Stokes parameters
        self.S0 = stokes_vector[0]
        self.S1 = stokes_vector[1]
        self.S2 = stokes_vector[2]

        if len(stokes_vector) == 4:
            self.S3 = stokes_vector[3]
        else:
            self.S3 = None

    def __str__(self):
        return (f"{self.__class__.__name__}: "
                f"Normalized: S1={self.get_S1_normalized()}, S2={self.get_S2_normalized()}")

    def get_S1_normalized(self):
        return self.S1 / self.S0

    def get_S2_normalized(self):
        return self.S2 / self.S0


class OptimizationProcedure:

    def __init__(self, measured_outgoing_stokes_parameters: list[MeasuredStokesVector]):
        """

        Args:
            measured_outgoing_stokes_parameters: list containing instances of the MeasuredOutgoingStokesVector class
        """

        self.measured_stokes: list[MeasuredStokesVector] = measured_outgoing_stokes_parameters

    def __str__(self):
        return f"{self.__class__.__name__}: {len(self.measured_stokes)} {MeasuredStokesVector.__name__}"

    @staticmethod
    def S1_in_theory(phi, delta, theta, omega) -> float:
        """
        See Eq. (8) in the paper

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

    @staticmethod
    def S2_in_theory(phi, delta, theta, omega) -> float:
        """
        See Eq. (9) in the paper

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

    @staticmethod
    def convert_theta_to_specified_range(theta: float) -> float:
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
        return theta % (math.pi / 2)

    @staticmethod
    def convert_omega_to_specified_range(omega: float) -> float:
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
        return omega % math.pi

    def residual_vector_r(self, delta: float, theta: float, omega: float) -> list[float]:
        """
        Eq. (12) in the paper
        """
        residual_vector = []

        for measurement in self.measured_stokes:
            residual_vector.append(
                measurement.get_S1_normalized() - OptimizationProcedure.S1_in_theory(phi=measurement.phi,
                                                                                     delta=delta, theta=theta,
                                                                                     omega=omega))
            residual_vector.append(
                measurement.get_S2_normalized() - OptimizationProcedure.S2_in_theory(phi=measurement.phi,
                                                                                     delta=delta, theta=theta,
                                                                                     omega=omega))

        return residual_vector

    def residual_function_R(self, delta: float, theta: float, omega: float) -> float:
        """
        Eq. (13) in the Paper
        """
        return np.linalg.norm(self.residual_vector_r(delta, theta, omega), ord=2)

    def find_characteristic_parameters(self,
                                       lb_delta: float = 0,
                                       ub_delta: float = math.pi,
                                       lb_theta: float = 0,
                                       ub_theta: float = math.pi,
                                       lb_omega: float = 0,
                                       ub_omega: float = 2 * math.pi,
                                       strategy: str = "rand1exp",
                                       ) -> MeasuredCharacteristicParameters:
        """
        Finds the characteristic parameters by finding the minimum of the residual function R using
        the scipy differential evolution.

        Args:
            lb_delta: lower boundary of delta
            ub_delta: upper boundary of delta
            lb_theta: lower boundary of theta
            ub_theta: upper boundary of theta
            lb_omega: lower boundary of omega
            ub_omega: upper boundary of omega
            strategy: differential evolution strategy

        Returns: class MeasuredCharacteristicParameters containing the characteristic parameters

        """

        def func(x) -> float:
            return self.residual_function_R(delta=x[0], theta=x[1], omega=x[2])

        result = optimize.differential_evolution(func=func,
                                                 bounds=((lb_delta, ub_delta),
                                                         (lb_theta, ub_theta),
                                                         (lb_omega, ub_omega)),
                                                 strategy=strategy)

        delta_tilde = result.x[0]
        theta_tilde = OptimizationProcedure.convert_theta_to_specified_range(result.x[1])
        omega_tilde = OptimizationProcedure.convert_omega_to_specified_range(result.x[2])

        return MeasuredCharacteristicParameters(delta=delta_tilde,
                                                theta=theta_tilde,
                                                omega=omega_tilde)
