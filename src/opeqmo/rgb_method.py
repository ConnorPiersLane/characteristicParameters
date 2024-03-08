import math
import statistics
from dataclasses import dataclass
from typing import Callable
import numpy as np
from scipy import optimize

from opeqmo.triangle_wave_functions import T_pi

"""
Important:
Most of these functions refer to the RGB method described in section 2.6 of my paper.
I recommend using the paper as a reference.
"""


@dataclass()
class MeasuredRetardation:
    """
    Attributes:
        wavelength: corresponding wavelength at which the retardation has been obtained
        delta: [rad] measured retardation
               (if linearly polarized incident light is used, the measurement range is 0-pi)
    """
    wavelength: float
    delta: float


def define_reduced_birefringence_function(lambda_0, a, b) -> Callable[[float], float]:
    """
    Defines a reduced birefringence function k(lambda) (see section 1).


    Source: Equation (2) and (3) in
            "Inoue, T., Kuwada, S., Ryu, D. S., & Osaki, K. (1998).
            Effects of wavelength on strain-induced birefringence of polymers. Polymer journal, 30(11), 929-934."


    Args:
        lambda_0: reference wavlength
        a: fitting parameter a
        b: fitting parameter b

    Returns: k(lambda) = birefringence(lambda) / birefringence(lambda_0)

    """

    def k(lambda_x: float) -> float:
        numerator = 1 + a / (lambda_x ** 2) + b / (lambda_x ** 4)
        denominator = 1 + a / (lambda_0 ** 2) + b / (lambda_0 ** 4)
        return numerator / denominator

    return k


class OneLocation:

    def __init__(self,
                 measured_retardations: list[MeasuredRetardation],
                 reduced_birefringence_function: Callable[[float], float]):
        """

        Args:
            measured_retardations: list containing instances of the MeasuredRetardation class
            reduced_birefringence_function: k(lambda) = birefringence(lambda) / birefringence(lambda_0)

        """
        self.measured_deltas: list[MeasuredRetardation] = measured_retardations
        self.k_function: Callable[[float], float] = reduced_birefringence_function

        # Set the reference wavelength as the first wavelength in the input list
        # the function parameter "delta" will always refer to the reference wavelength
        self.reference_wavelength = measured_retardations[0].wavelength

    def error_vector_e(self, delta) -> list[float]:
        """
        Eq. (26) in the paper

        Args:
            delta: retardation of the light at the reference wavelength

        """
        # The reference wavelength has been set in the constructor
        wave_0 = self.reference_wavelength

        vector = []
        for measured_retardation in self.measured_deltas:
            wave = measured_retardation.wavelength
            delta_measured = measured_retardation.delta

            delta_in = (wave_0 / wave * self.k_function(wave) / self.k_function(wave_0) * delta)

            vector.append(delta_measured - T_pi(delta_in))

        return vector

    def error_function_E(self, delta):
        """
        Eq. (27) in the paper

        Args:
            delta: retardation at the reference wavelength (see self.reference_wavelength)

        """
        return np.linalg.norm(self.error_vector_e(delta), ord=2)


class MultipleNeighboringLocations:

    @staticmethod
    def _validate_init_input(neighboring_locations):
        # Set the Reference Wavelength
        wave0 = neighboring_locations[0].reference_wavelength

        # Make sure alle Neighboring Measurements refer to the same reference wavelength
        for i in range(1, len(neighboring_locations)):
            location = neighboring_locations[i]
            if not math.isclose(wave0, location.reference_wavelength, rel_tol=1e-3):
                raise ValueError(
                    f"The first location at position 0 has a reference wavelength of: {wave0}. "
                    f"But the location at position {i} has a reference wavelength of: {location.reference_wavelength}. "
                    f"All reference wavelengths must be the same.")
        return None

    def __init__(self, neighboring_locations: list[OneLocation]):

        self._validate_init_input(neighboring_locations)

        self.reference_wavelength = neighboring_locations[0].reference_wavelength
        self.locations: list[OneLocation] = neighboring_locations

    def _validate_deltas_input(self, deltas):
        if not len(deltas) == len(self.locations):
            raise ValueError(f"The input has length: {len(deltas)}."
                             f"It must be the same as the number of locations: {len(self.locations)}")
        return None

    def loss_function_L(self, deltas: list[float], k: float = 1) -> float:
        """
        Eq. (32) in the paper

        Args:
            deltas: list of retardations at the reference wavelength (see self.reference_wavelength)
            k: K-Parameter
        """
        self._validate_deltas_input(deltas)

        error_functions = [one_location.error_function_E(delta)
                           for (one_location, delta) in zip(self.locations, deltas)]

        delta_mean = statistics.fmean(deltas)
        total_sum = 0
        for (E, delta) in zip(error_functions, deltas):
            total_sum = total_sum + E + k * (delta - delta_mean) ** 2
        return total_sum

    def find_all_neighboring_retardations(self,
                                      k: float,
                                      lb_delta: float = 0,
                                      ub_delta: float = 50 * math.pi,
                                      strategy: str = "rand1exp"):
        """
        Finds the minimum of Eq. (32) in the paper

        Finds all retardations belonging to the neighboring locations with the loss function L
        All retardations are at the reference wavelength (self.reference_wavelength)

        Args:
            k: K-Parameter of the loss function (see Eq. (32) in the paper)
            lb_delta: lower boundary of the search area (default i 0)
            ub_delta: upper boundary of the search area (default is 50 pi)
            strategy: strategy of the differential evolution (see

        Returns: list of retardations

        """

        # func:
        def func(x):
            return self.loss_function_L(deltas=x, k=k)

        # define boundaries:
        bounds = []
        for _ in self.locations:
            bounds.append((lb_delta, ub_delta))

        optimization_result = optimize.differential_evolution(func=func,
                                                              bounds=bounds,
                                                              strategy=strategy)

        return optimization_result.x
