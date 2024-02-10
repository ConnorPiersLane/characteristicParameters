import math
import statistics
from typing import Callable

import numpy as np
from scipy import optimize

from charpar.linear import R_pi


def generate_dispersion_function_k(lambda_0, a, b) -> Callable[[float], float]:
    def k(lambda_x: float) -> float:
        numerator = 1 + a / (lambda_x ** 2) + b / (lambda_x ** 4)
        denominator = 1 + a / (lambda_0 ** 2) + b / (lambda_0 ** 4)
        return numerator / denominator

    return k


def generate_error_function_E(
        measured_relative_phases: list[float],
        wavelengths: list[float],
        reduced_dispersion_function: Callable[[float], float]) -> Callable[[float], float]:

    if not len(measured_relative_phases) == len(wavelengths):
        raise ValueError("For each measured relative phase, you need to provide the corresponding wavelength")

    wave_0 = wavelengths[0]  # The first wavelength will be taken as the reference wavelength

    def error_function_E(delta):
        vector = []
        for (delta_r, wave) in zip(measured_relative_phases, wavelengths):
            delta_in = wave_0 / wave * reduced_dispersion_function(wave) / reduced_dispersion_function(wave_0) * delta
            vector.append(delta_r - R_pi(delta_in))
        return np.linalg.norm(vector, ord=2)
    return error_function_E


def generate_rgb_optimizer(n_parameters: int,
                           lb_delta: float = 0,
                           ub_delta: float = 50 * math.pi,
                           strategy: str = "rand1exp") -> Callable[
    [Callable], optimize.OptimizeResult]:

    bounds = []
    for _ in range(n_parameters):
        bounds.append((lb_delta, ub_delta))

    def de_optimizer(func: Callable) -> optimize.OptimizeResult:
        return optimize.differential_evolution(func=func,
                                               bounds=bounds,
                                               strategy=strategy)
    return de_optimizer


def generate_cost_function_L(error_functions: list[Callable], K: float = 0.1) -> Callable[[list[float]], float]:
    """

    Args:
        error_functions:
        K:

    Returns:

    """
    def cost_function_L(x: list[float]) -> float:
        delta_mean = statistics.fmean(x)
        L = 0
        for (E, delta) in zip(error_functions, x):
            L = L + E(delta) + K*(delta-delta_mean)**2
        return L

    return cost_function_L


def calc_absolute_phase_differences(measured_relative_phases: list[float],
                                    wavelengths: list[float],
                                    reduced_dispersion_function: Callable[[float], float],
                                    ):
    residual_vector_norm = generate_error_function_E(measured_relative_phases=measured_relative_phases,
                                                     wavelengths=wavelengths,
                                                     reduced_dispersion_function=reduced_dispersion_function)
