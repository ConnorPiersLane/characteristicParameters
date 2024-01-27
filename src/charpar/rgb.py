from dataclasses import dataclass
from typing import Callable

from charpar.circular import R_pi_2
from charpar.linear import R_pi


def generate_dispersion_function_k(lambda_0, a, b) -> Callable[[float], float]:
    def k(lambda_x: float) -> float:
        numerator = 1 + a / (lambda_x ** 2) + b / (lambda_x ** 4)
        denominator = 1 + a / (lambda_0 ** 2) + b / (lambda_0 ** 4)
        return numerator / denominator
    return k



@dataclass(frozen=True)
class OneRelativeMeasurement:
    """
    Attributes:
        wavelength: [m] wavelength of the corresponding measurement
        measured_relative_phase_difference: [rad] 0-pi (linearly polarized incident light) or 0-pi/2 (circularly ...)
        dispersion_k: [] dispersion of birefringence in the reduced form with
                        k(lambda) = Delta n(lambda) / Delta n(lambda_ref)
        type_of_incident_polarized_light: "linear" or "circular"
    """
    wavelength: float
    measured_relative_phase_difference: float
    dispersion_k: float




def _get_relative_function(type) -> Callable[[float], float]:
    if type == "linear":
        return R_pi
    elif type == "circular":
        return R_pi_2
    else:
        raise NotImplementedError(
            f"This method is only implemented for type==linear and type==circular. Buty type={type}")


def _generate_residual_vector_norm(measurements: list[OneRelativeMeasurement],
                                relative_function: Callable[[float], float]) -> Callable[[float], float]:

    def residual_vector_norm(x) -> float:
        # First entry will be the reference
        lambda_r = measurements[0].wavelength


        vector = []
        pass

def calc_absolute_phase_differences(measurements: list[OneRelativeMeasurement], type="linear") -> list[float]:
    """

    Args:
        measurements (list[OneRelativeMeasurement]):
        type (str): "linear" or "circular" depending on which polarized incident light was used

    Returns:

    """
    R = _get_relative_function(type)

    residual_vector = []