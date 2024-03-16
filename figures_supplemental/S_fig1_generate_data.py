import math
import pickle

import numpy as np
import concurrent.futures

from oem.mueller_calculus import linearly_polarized_light, optical_equivalent_model
from oem.measurement_procedure import MeasuredStokesParameters, calculate_characteristic_parameters, define_function_that_finds_minimum_of_R_function

stepsize = math.radians(1)
omegas = np.arange(0, math.pi + stepsize / 2, stepsize)
deltas = np.arange(0, math.pi + stepsize / 2, stepsize)

phi_1 = 0
phi_2 = math.radians(45)

true_values = []
measured_Stokes = []
measured_values = []

for delta in deltas:
    for omega in omegas:
        theta = delta / 6

        true_values.append((delta, theta, omega))

        # Measured Stokes parameters
        model = optical_equivalent_model(delta=delta, theta=theta, omega=omega)
        S_phi1 = model.dot(linearly_polarized_light(phi_1))
        S_phi2 = model.dot(linearly_polarized_light(phi_2))

        measured = MeasuredStokesParameters([phi_1, phi_2],
                                            [S_phi1[1], S_phi2[1]],
                                            [S_phi1[2], S_phi2[2]])

        measured_Stokes.append(measured)

        optimization_1 = define_function_that_finds_minimum_of_R_function(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi / 2,
            lb_omega=0, ub_omega=math.pi,
            strategy="best1bin"
        )

        optimization_2 = define_function_that_finds_minimum_of_R_function(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi,
            lb_omega=0, ub_omega=2 * math.pi,
            strategy="best1bin"
        )

        optimization_3 = define_function_that_finds_minimum_of_R_function(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi / 2,
            lb_omega=0, ub_omega=math.pi,
            strategy="rand1exp"
        )

        optimization_4 = define_function_that_finds_minimum_of_R_function(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi,
            lb_omega=0, ub_omega=2 * math.pi,
            strategy="rand1exp"
        )


    def f1(stokes):
        return calculate_characteristic_parameters(measured_stokes_parameters=stokes, optimizer=optimization_1)
    def f2(stokes):
        return calculate_characteristic_parameters(measured_stokes_parameters=stokes, optimizer=optimization_2)
    def f3(stokes):
        return calculate_characteristic_parameters(measured_stokes_parameters=stokes, optimizer=optimization_3)
    def f4(stokes):
        return calculate_characteristic_parameters(measured_stokes_parameters=stokes, optimizer=optimization_4)

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        # 1
        measured_values = list(executor.map(f1, measured_Stokes))
        results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
        with open("S_fig1_measured_values_1_L1norm.pickle", "wb") as handle:
            pickle.dump(results, handle)


        # 2
        measured_values = list(executor.map(f2, measured_Stokes))
        results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
        with open("S_fig1_measured_values_2_L1norm.pickle", "wb") as handle:
            pickle.dump(results, handle)

        # 3
        measured_values = list(executor.map(f3, measured_Stokes))
        results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
        with open("S_fig1_measured_values_3_L1norm.pickle", "wb") as handle:
            pickle.dump(results, handle)

        # 4
        measured_values = list(executor.map(f4, measured_Stokes))
        results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
        with open("S_fig1_measured_values_4_L1norm.pickle", "wb") as handle:
            pickle.dump(results, handle)

    with open("S_fig1_true_values.pickle", "wb") as handle:
        pickle.dump(true_values, handle)
