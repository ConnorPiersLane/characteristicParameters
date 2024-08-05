import math

import numpy as np

from characteristicParameters._helpers import CodingError
from characteristicParameters.muellerCalculus import optical_equivalent_model


def eff_diff_with_shift(measured, true, shift):
    diff1 = true - measured
    diff2 = true - (measured+shift)
    diff3 = (true+shift) - measured

    if abs(diff1) == min(abs(diff1), abs(diff2), abs(diff3)):
        return diff1
    elif abs(diff2) == min(abs(diff1), abs(diff2), abs(diff3)):
        return diff2
    elif abs(diff3) == min(abs(diff1), abs(diff2), abs(diff3)):
        return diff3
    else:
        raise CodingError("Failed to find the minimum deviation.")

def eff_diff_omega(omega_measured: float, omega_expected: float) -> float:
    return eff_diff_with_shift(measured=omega_measured,
                               true=omega_expected,
                               shift=math.pi)

def eff_diff_theta(theta_measured: float, theta_expected: float) -> float:
    return eff_diff_with_shift(measured=theta_measured,
                               true=theta_expected,
                               shift=math.pi/2)

def shift_omega_to_0_pi(omega: float) -> float:
    """

    Args:
        omega: [rad] in any range

    Returns: [rad] in range [0-pi]

    """
    return omega % math.pi

def shift_theta_to_0_pi_2(theta: float) -> float:
    """

    Args:
        theta: [rad] in any range

    Returns: [rad] in range [0-pi/2]

    """
    return theta % (math.pi/2)


def char_paras_to_stokes(
        delta: float, theta: float, omega: float, stokes_in
    ):
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

    Sigma_1 = S1_0 + S2_45
    Sigma_2 = -S1_45 + S2_0
    Sigma_3 = S1_0 - S2_45
    Sigma_4 = -S1_45 - S2_0

    # Calculate delta
    cos_delta = 0.25*(Sigma_1**2 + Sigma_2**2 - Sigma_3**2 - Sigma_4**2)

    # Measurement errors can lead to cos_delta>1 or cos_delta<-1
    if cos_delta>1: cos_delta=1
    if cos_delta<-1: cos_delta=-1

    delta = math.acos(cos_delta)

    # Calculate omega
    omega = 0.5 * math.atan2(Sigma_2, Sigma_1)

    # Calculate theta
    theta = 0.25 * math.atan2(Sigma_2*Sigma_3-Sigma_1*Sigma_4, Sigma_1*Sigma_3+Sigma_2*Sigma_4)


    return delta, theta, omega