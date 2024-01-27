import math
import pickle

import numpy as np
import concurrent.futures

from charpar.mueller_calculus import S_lin, XR
from charpar.linear import MeasuredStokesParameters, calc_charparas, make_de_optimization

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
        model = XR(delta=delta, theta=theta, omega=omega)
        S_phi1 = model.dot(S_lin(phi_1))
        S_phi2 = model.dot(S_lin(phi_2))

        measured = MeasuredStokesParameters([phi_1, phi_2],
                                            [S_phi1[1], S_phi2[1]],
                                            [S_phi1[2], S_phi2[2]])

        measured_Stokes.append(measured)

        optimization_1 = make_de_optimization(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi / 2,
            lb_omega=0, ub_omega=math.pi,
            strategy="best1bin"
        )

        optimization_2 = make_de_optimization(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi,
            lb_omega=0, ub_omega=2 * math.pi,
            strategy="best1bin"
        )

        optimization_3 = make_de_optimization(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi / 2,
            lb_omega=0, ub_omega=math.pi,
            strategy="rand1exp"
        )

        optimization_4 = make_de_optimization(
            lb_delta=0, ub_delta=math.pi,
            lb_theta=0, ub_theta=math.pi,
            lb_omega=0, ub_omega=2 * math.pi,
            strategy="rand1exp"
        )

    #
    # def f1(stokes):
    #     return calc_charparas(measured_stokes_parameters=stokes, optimization=optimization_1)
    # def f2(stokes):
    #     return calc_charparas(measured_stokes_parameters=stokes, optimization=optimization_2)
    # def f3(stokes):
    #     return calc_charparas(measured_stokes_parameters=stokes, optimization=optimization_3)
    # def f4(stokes):
    #     return calc_charparas(measured_stokes_parameters=stokes, optimization=optimization_4)
#
# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
#         # 1
#         measured_values = list(executor.map(f1, measured_Stokes))
#         results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
#         with open("S_fig1_measured_values_1_L1norm.pickle", "wb") as handle:
#             pickle.dump(results, handle)
#
#
#         # 2
#         measured_values = list(executor.map(f2, measured_Stokes))
#         results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
#         with open("S_fig1_measured_values_2_L1norm.pickle", "wb") as handle:
#             pickle.dump(results, handle)
#
#         # 3
#         measured_values = list(executor.map(f3, measured_Stokes))
#         results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
#         with open("S_fig1_measured_values_3_L1norm.pickle", "wb") as handle:
#             pickle.dump(results, handle)
#
#         # 4
#         measured_values = list(executor.map(f4, measured_Stokes))
#         results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]
#         with open("S_fig1_measured_values_4_L1norm.pickle", "wb") as handle:
#             pickle.dump(results, handle)

    with open("S_fig1_true_values.pickle", "wb") as handle:
        pickle.dump(true_values, handle)
