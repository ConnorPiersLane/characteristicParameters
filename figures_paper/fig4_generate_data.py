import math
import pickle
import numpy as np
import concurrent.futures

from charpar.mueller_calculus import S_lin, XR
from charpar.linear import MeasuredStokesParameters, calc_charparas

stepsize = math.radians(30)
deltas = np.arange(0, 2 * math.pi + stepsize / 2, stepsize)  # x-axis
omegas = np.arange(0, math.pi + stepsize / 2, stepsize)  # y-axis

phi_1 = 0
phi_2 = math.pi / 4

true_values = []
measured_Stokes = []
measured_values = []

for delta in deltas:
    for omega in omegas:
        theta = delta / 2  # Set theta

        true_values.append((delta, theta, omega))

        # Measured Stokes parameters
        model = XR(delta=delta, theta=theta, omega=omega)
        S_phi1 = model.dot(S_lin(phi_1))
        S_phi2 = model.dot(S_lin(phi_2))

        measured = MeasuredStokesParameters([phi_1, phi_2],
                                            [S_phi1[1], S_phi2[1]],
                                            [S_phi1[2], S_phi2[2]])

        measured_Stokes.append(measured)

# the next line of codes needs to be there so the ProcessPoolExecutor can run parallel on windows

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        measured_values = list(executor.map(calc_charparas, measured_Stokes))

    with open("measured_values_fig3.pickle", "wb") as handle:
        pickle.dump(measured_values, handle)

    with open("true_values_fig3.pickle", "wb") as handle:
        pickle.dump(true_values, handle)
