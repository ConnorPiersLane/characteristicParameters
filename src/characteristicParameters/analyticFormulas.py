import math

import numpy as np

from characteristicParameters._helpers import CodingError
from characteristicParameters.muellerCalculus import optical_equivalent_model


def eff_diff_with_shift(measured, true, shift):
    diff1 = abs(measured - true)
    diff2 = abs(measured+shift - true)
    diff3 = abs(measured - (true+shift))
    return min(diff1, diff2, diff3)

def eff_diff_omega(omega_measured: float, omega_expected: float) -> float:
    return eff_diff_with_shift(measured=omega_measured,
                               true=omega_expected,
                               shift=math.pi)

def eff_diff_theta(theta_measured: float, theta_expected: float) -> float:
    return eff_diff_with_shift(measured=theta_measured,
                               true=theta_expected,
                               shift=math.pi/2)

def shift_omega_to_specified_range(omega: float) -> float:
    """

    Args:
        omega: [rad] in any range

    Returns: [rad] in range [0-pi]

    """
    return omega % math.pi

def shift_theta_to_specified_range(theta: float) -> float:
    """

    Args:
        theta: [rad] in any range

    Returns: [rad] in range [0-pi/2]

    """
    return theta % (math.pi/2)


def char_paras_to_stokes(
        delta: float, theta: float, omega: float, stokes_in: list | np.ndarray | tuple
    ) -> list[float, float, float, float]:
    """
    
    Args:
        delta: [rad]
        theta: [rad]
        omega: [rad]
        stokes_in: [S0, S1, S2, S3]

    Returns: [S0, S1, S2, S3]

    """
    oem = optical_equivalent_model(delta=delta, theta=theta, omega=omega)
    stokes_in = np.asarray(stokes_in)
    return list(np.matmul(oem, stokes_in))


def stokes_to_char_paras_phi_0_and_45(
        stokes_0_deg: list | np.ndarray | tuple,
        stokes_45_deg: list | np.ndarray | tuple
) -> tuple[float, float, float]:
    """
    
    Args:
        stokes_0_deg: measured at phi=0° [S0, S1, S2] or [S0, S1, S2, S3]
        stokes_45_deg: measured at phi=45° [S0, S1, S2] or [S0, S1, S2, S3]

    Returns: delta [0-pi], theta [0-pi/4], omega [0-pi]

    """
    S1_0 = stokes_0_deg[1] / stokes_0_deg[0]
    S2_0 = stokes_0_deg[2] / stokes_0_deg[0]

    S1_45 = stokes_45_deg[1] / stokes_45_deg[0]
    S2_45 = stokes_45_deg[2] / stokes_45_deg[0]

    omega = 0.5 * math.atan2(S2_0-S1_45, S1_0+S2_45)
    theta = omega / 2 - 0.25 * math.atan2(-S1_45-S2_0, S1_0-S2_45)

    # Calculate the denominators for each Equation
    den_S1_0 = math.cos(2 * omega) - math.cos(2 * omega - 4 * theta)
    den_S2_0 = math.sin(2 * omega) + math.sin(2 * omega - 4 * theta)
    den_S1_45 = math.sin(2 * omega) - math.sin(2 * omega - 4 * theta)
    den_S2_45 = math.cos(2 * omega) + math.cos(2 * omega - 4 * theta)

    # Chose the denominator which is most far from zero
    den_max = max(abs(den_S1_0), abs(den_S2_0), abs(den_S1_45), abs(den_S2_45))

    if den_max == abs(den_S1_0):
        cos_delta = ((2 * S1_0 - math.cos(2*omega) - math.cos(2 * omega - 4 * theta)) / den_S1_0)
    elif den_max == abs(den_S2_0):
        cos_delta = ((2 * S2_0 - math.sin(2*omega) + math.sin(2 * omega - 4 * theta)) / den_S2_0)
    elif den_max == abs(den_S1_45):
        cos_delta = ((- 2 * S1_45 - math.sin(2 * omega) - math.sin(2 * omega - 4 * theta)) / den_S1_45)
    elif den_max == abs(den_S2_45):
        cos_delta = ((2 * S2_45 - math.cos(2*omega) + math.cos(2 * omega - 4 * theta)) / den_S2_45)
    else:
        raise CodingError("Failed to find the maximum denominator.")

    # Measurement errors can lead to cos_delta>1 or cos_delta<-1
    if cos_delta>1: cos_delta=1
    if cos_delta<-1: cos_delta=-1

    delta = math.acos(cos_delta)

    return delta, shift_theta_to_specified_range(theta), shift_omega_to_specified_range(omega)