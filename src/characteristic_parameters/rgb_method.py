import math
import statistics
from dataclasses import dataclass
from typing import Callable
import numpy as np
from scipy import optimize

from characteristic_parameters import _helpers
from characteristic_parameters.triangle_wave_functions import T_pi

"""
Important:
Most of these functions refer to the RGB method described in section 2.6 of my paper.
I recommend using the paper as a reference.
"""


@dataclass()
class RetardationMeasurement:
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
    Defines a reduced birefringence function k(lambda) (see Eq. (4) in the paper).


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


def convert_retardation_to_different_wavelength(k_function: Callable[[float], float],
                                                wavelength_1: float,
                                                delta_1: float,
                                                wavelength_2):
    """
    See Eq. (5) in the paper

    Args:
        k_function: a reduced_birefringence_function
        wavelength_1: wavelength at which the retardation is known
        delta_1: known retardation
        wavelength_2: wavelength for which we want to know the retardation

    Returns: delta_2 (new retardation for wavelength_2)

    """
    return (wavelength_1 / wavelength_2
            * k_function(wavelength_2) / k_function(wavelength_1)
            * delta_1)


class MeasuredRetardationsAtOneLocation:

    def __init__(self,
                 measurement_at_reference_wavelength: RetardationMeasurement,
                 additional_measurements: RetardationMeasurement | list[RetardationMeasurement],
                 reduced_birefringence_function: Callable[[float], float]):
        """

        Args:
            measurement_at_reference_wavelength: Measurements at the reference wavelength
            additional_measurements: list containing instances of the MeasuredRetardation class
            reduced_birefringence_function: k(lambda) = birefringence(lambda) / birefringence(lambda_0)

        """
        # Set the reference wavelength
        # the function parameter "delta" will always refer to the reference wavelength
        # In the paper, this is delta_r
        self.measurement_at_reference_wavelength = measurement_at_reference_wavelength

        if not isinstance(additional_measurements, list):
            additional_measurements = [additional_measurements]

        self.all_measurements: list[RetardationMeasurement] = [
                    measurement_at_reference_wavelength] + additional_measurements

        self.k_function: Callable[[float], float] = reduced_birefringence_function

    def __str__(self):
        return f"Class {self.__class__.__name__} with reference wavelength {self.get_reference_wavelength()}"

    def get_reference_wavelength(self) -> float:
        return self.measurement_at_reference_wavelength.wavelength

    def error_vector_e(self, delta_r: float) -> list[float]:
        """
        Eq. (26) in the paper

        Args:
            delta_r: retardation of the light at the reference wavelength

        """

        vector = []
        for measured_lambda_delta in self.all_measurements:
            delta_in = convert_retardation_to_different_wavelength(
                k_function=self.k_function,
                wavelength_1=self.get_reference_wavelength(),
                delta_1=delta_r,
                wavelength_2=measured_lambda_delta.wavelength
            )

            vector.append(measured_lambda_delta.delta - T_pi(delta_in))

        return vector

    def error_function_E(self, delta_r: float):
        """
        Eq. (27) in the paper

        Args:
            delta_r: retardation at the reference wavelength (see self.reference_wavelength)

        """
        return np.linalg.norm(self.error_vector_e(delta_r), ord=2)


class MultipleNeighboringLocations:

    @staticmethod
    def _check_if_all_have_the_same_reference_wavelength(neighboring_locations):
        reference_wavelengths = [location.get_reference_wavelength() for location in neighboring_locations]
        return _helpers.all_equal(reference_wavelengths)

    def __init__(self, neighboring_locations: list[MeasuredRetardationsAtOneLocation]):

        self._check_if_all_have_the_same_reference_wavelength(neighboring_locations)

        self.locations: list[MeasuredRetardationsAtOneLocation] = neighboring_locations

    def __str__(self):
        return f"Class {self.__class__.__name__} with reference wavelength {self.get_reference_wavelength()}"

    def get_reference_wavelength(self) -> float:
        return self.locations[0].get_reference_wavelength()

    def _validate_length_of_input(self, delta_rs) -> None:
        if not len(delta_rs) == len(self.locations):
            raise _helpers.InvalidInputError(f"The input has length: {len(delta_rs)}."
                                             f"It must be the same as the number of locations: {len(self.locations)}")
        return None

    def collective_error_function_L(self, delta_rs: list[float], k: float = 1) -> float:
        """
        Eq. (32) in the paper

        Args:
            delta_rs: list of retardations at the reference wavelength (see self.reference_wavelength)
            k: K-Parameter
        """
        self._validate_length_of_input(delta_rs)

        error_functions = [
            one_location.error_function_E(delta_r) for (one_location, delta_r) in zip(self.locations, delta_rs)]

        delta_mean = statistics.fmean(delta_rs)
        total_sum = 0
        for (E, delta_r) in zip(error_functions, delta_rs):
            total_sum = total_sum + E + k * (delta_r - delta_mean) ** 2
        return total_sum

    def find_all_neighboring_delta_r(self,
                                     k: float,
                                     lb_delta: float = 0,
                                     ub_delta: float = 50 * math.pi,
                                     strategy: str = "rand2exp"):
        """
        Finds the minimum of Eq. (32) in the paper

        Finds all retardations belonging to the neighboring locations with the loss function L
        All retardations are at the reference wavelength (self.reference_wavelength)

        Args:
            k: K-Parameter of the loss function (see Eq. (32) in the paper)
            lb_delta: lower boundary of the search area (default i 0)
            ub_delta: upper boundary of the search area (default is 50 pi)
            strategy: strategy of the differential evolution (see scipy documentation)

        Returns: list of retardations at the reference wavelength

        """

        # func:
        def func(x):
            return self.collective_error_function_L(delta_rs=x, k=k)

        # define boundaries:
        bounds = []
        for _ in self.locations:
            bounds.append((lb_delta, ub_delta))

        optimization_result = optimize.differential_evolution(func=func,
                                                              bounds=bounds,
                                                              strategy=strategy)

        return optimization_result.x
