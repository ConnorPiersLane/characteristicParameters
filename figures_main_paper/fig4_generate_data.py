import math
import pickle
import numpy as np
import concurrent.futures

from oem.measurement_procedure import MeasurementProcedure, MeasuredNormalizedStokesParametersS1S2
from oem.mueller_calculus import linearly_polarized_light, optical_equivalent_model

# Settings
stepsize = math.radians(30)
# x-axis
deltas = np.arange(0, 2 * math.pi + stepsize / 2, stepsize)
# y-axis
omegas = np.arange(0, math.pi + stepsize / 2, stepsize)

# Two orientations angles for the incident linearly polarized light:
phi_1 = 0
phi_2 = math.pi / 4

# Store the values here:
true_values = []  # true characteristic values
measurements: list[MeasurementProcedure] = []  # measured Stokes parameters
measured_values = []  # measured characteristic values

for delta in deltas:
    for omega in omegas:
        theta = delta / 2  # Set theta

        # Store the true values
        true_values.append((delta, theta, omega))

        # Calculate the outgoing Stokes parameters
        # Define the optical model:
        model = optical_equivalent_model(delta=delta, theta=theta, omega=omega)
        # Incident light:
        S_in_phi1 = linearly_polarized_light(phi_1)
        S_in_phi2 = linearly_polarized_light(phi_2)

        S_out_phi1 = np.matmul(model, S_in_phi1)
        S_out_phi2 = np.matmul(model, S_in_phi2)

        OutgoingStokes1 = MeasuredNormalizedStokesParametersS1S2(phi=phi_1,
                                                                 stokes_vector=S_out_phi1)
        OutgoingStokes2 = MeasuredNormalizedStokesParametersS1S2(phi=phi_2,
                                                                 stokes_vector=S_out_phi2)
        measurements.append(MeasurementProcedure([OutgoingStokes1, OutgoingStokes2]))

# Define a function that can be run parallel:
def find_parameters_parallel(measurement: MeasurementProcedure) -> (float, float, float):
    parameters = measurement.find_characteristic_parameters()
    return parameters.delta, parameters.theta, parameters.omega

# the next line of codes needs to be there so the ProcessPoolExecutor can run parallel on windows
if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        measured_values = list(executor.map(find_parameters_parallel, measurements))

    with open("data/measured_values_fig3.pickle", "wb") as handle:
        pickle.dump(measured_values, handle)

    with open("data/true_values_fig3.pickle", "wb") as handle:
        pickle.dump(true_values, handle)
