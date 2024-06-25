import math
import pickle

import numpy as np

from characteristicParameters.analyticFormulas import char_paras_to_stokes, stokes_to_char_paras_phi_0_and_45, \
    eff_diff_theta, eff_diff_omega
from characteristicParameters.muellerCalculus import linearly_polarized_light
from characteristicParameters.triangle_wave_functions import T_pi

# Help functions to calculate the difference between guessed and true



""" Settings """
# Chose a fixed theta
theta = math.radians(125)
theta_expected = theta % (math.pi/2)

# Error analyis
# N times the corresponding characteristic parameters are calculated
N = 1000
error_std = 1e-3  # mean and standard deviation

# Settings
stepsize = math.radians(1)

# y-axis
omegas = np.arange(0, math.pi + stepsize / 2, stepsize)
# x-axis
deltas = np.arange(0, 4 * math.pi + stepsize / 2, stepsize)

# The variances of the guessed results are stored here
std_delta = [[None] * len(deltas)] * len(omegas)
std_theta = [[None] * len(deltas)] * len(omegas)
std_omega = [[None] * len(deltas)] * len(omegas)

for o in range(len(omegas)):
    print(f"{o}/{len(omegas)-1}")
    for d in range(len(deltas)):
        omega = omegas[o]
        delta = deltas[d]

        S_0 = char_paras_to_stokes(delta=delta, theta=theta, omega=omega, stokes_in=linearly_polarized_light(0))
        S_45 = char_paras_to_stokes(delta=delta, theta=theta, omega=omega, stokes_in=linearly_polarized_light(math.pi/4))

        # Calculate measured Stokes Parameters and add an error
        S1_0_Ns = [S_0[1] + err for err in np.random.normal(0, error_std, N)]
        S2_0_Ns = [S_0[2] + err for err in np.random.normal(0, error_std, N)]
        S1_45_Ns = [S_45[1] + err for err in np.random.normal(0, error_std, N)]
        S2_45_Ns = [S_45[2] + err for err in np.random.normal(0, error_std, N)]

        char_pars_guessed = [stokes_to_char_paras_phi_0_and_45(
            stokes_0_deg=[1, S1_0, S2_0], stokes_45_deg=[1, S1_45, S2_45])
            for (S1_0, S2_0, S1_45, S2_45) in zip(S1_0_Ns, S2_0_Ns, S1_45_Ns, S2_45_Ns)
         ]


        delta_guesses = [char_pars[0] for char_pars in char_pars_guessed]
        theta_guesses = [char_pars[1] for char_pars in char_pars_guessed]
        omega_guesses = [char_pars[2] for char_pars in char_pars_guessed]

        delta_errors = [guess - T_pi(delta) for guess in delta_guesses]
        theta_errors = [eff_diff_theta(theta_measured=guess, theta_expected=theta_expected) for guess in theta_guesses]
        omega_errors = [eff_diff_omega(omega_measured=guess, omega_expected=omega) for guess in omega_guesses]

        std_delta[o][d] = np.std(delta_errors)
        std_theta[o][d] = np.std(theta_errors)
        std_omega[o][d] = np.std(omega_errors)

std_errors = (std_delta, std_theta, std_omega)
with open(r"fig4_std_errors.pickle", "wb") as handle:
    pickle.dump(std_errors, handle)







