import math
import pickle

import numpy as np
import concurrent.futures

from charpar.mueller_calculus import S_lin, XR
from charpar.linear import MeasuredStokesParameters, calc_charparas



stepsize = math.radians(1)
omegas = np.arange(0, math.pi + stepsize / 2, stepsize)
deltas = np.arange(0, 6*
                   math.pi+stepsize/2, stepsize)

phi_1 = 0
phi_2 = math.radians(45)

true_values = []
measured_Stokes = []
measured_values = []

for delta in deltas:
    for omega in omegas:

        theta = delta/6

        true_values.append((delta, theta, omega))

        # Measured Stokes parameters
        model = XR(delta=delta, theta=theta, omega=omega)
        S_phi1 = model.dot(S_lin(phi_1))
        S_phi2 = model.dot(S_lin(phi_2))

        measured = MeasuredStokesParameters([phi_1, phi_2],
                                            [S_phi1[1], S_phi2[1]],
                                            [S_phi1[2], S_phi2[2]])

        measured_Stokes.append(measured)

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        measured_values = list(executor.map(calc_charparas, measured_Stokes))



    results = [(charpar.delta_tilde, charpar.theta_tilde, charpar.omega_tilde) for charpar in measured_values]

    with open("S_fig2_measured_values.pickle", "wb") as handle:
        pickle.dump(results, handle)

    with open("S_fig2_true_values.pickle", "wb") as handle:
        pickle.dump(true_values, handle)


