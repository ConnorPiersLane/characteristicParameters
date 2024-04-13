import math
import numpy as np
import pytest

from characteristicParameters.measurementProcedure import MeasurementProcedure, MeasuredStokesVector
from characteristicParameters import muellerCalculus
def test_MeasuredNormalizedStokesVector():

    # Test 1:
    stokes = MeasuredStokesVector(0, [2, 4, 6, 8])
    assert pytest.approx(0) == stokes.phi
    assert pytest.approx(1) == stokes.S0
    assert pytest.approx(2) == stokes.S1
    assert pytest.approx(3) == stokes.S2
    assert pytest.approx(4) == stokes.S3

    # Test 1:
    stokes = MeasuredStokesVector(math.pi, [2, 6, 8])
    assert pytest.approx(math.pi) == stokes.phi
    assert pytest.approx(1) == stokes.S0
    assert pytest.approx(3) == stokes.S1
    assert pytest.approx(4) == stokes.S2
    assert stokes.S3 is None

def test_S1_in_theory():
    # This should give circularly polarized light and hence S1==0
    delta = math.pi/2
    omega = math.pi/4
    phi = 0
    theta = 0
    assert pytest.approx(0) == MeasurementProcedure.S1_in_theory(phi=phi, delta=delta, theta=theta, omega=omega)

def test_S2_in_theory():
    # This should give circularly polarized light and hence S2 == 0
    delta = math.pi/2
    omega = math.pi/4
    phi = 0
    theta = 0
    assert pytest.approx(0) == MeasurementProcedure.S2_in_theory(phi=phi, delta=delta, theta=theta, omega=omega)

def test_compare_with_Mueller_matrices():

    # Arrange:
    # Define parameters:
    delta = math.pi/8
    omega = math.pi/5
    phi = math.pi/7
    theta = 23*math.pi/16

    # Get the optically equivalent model
    S_in = mueller_calculus.linearly_polarized_light(phi)
    optical_equivalent_model=mueller_calculus.optical_equivalent_model(
        delta=delta, theta=theta, omega=omega
    )
    S_out_oem = optical_equivalent_model @ S_in

    # Act and Assert:
    assert pytest.approx(S_out_oem[1]) == MeasurementProcedure.S1_in_theory(phi=phi, delta=delta, theta=theta, omega=omega)
    assert pytest.approx(S_out_oem[2]) == MeasurementProcedure.S2_in_theory(phi=phi, delta=delta, theta=theta, omega=omega)


def test_convert_theta_to_specified_range():
    assert pytest.approx(0) == MeasurementProcedure.convert_theta_to_specified_range(math.pi/2)
    assert pytest.approx(math.pi / 4) == MeasurementProcedure.convert_theta_to_specified_range(3* math.pi / 4)

def test_convert_omega_to_specified_range():
    assert pytest.approx(math.pi/2) == MeasurementProcedure.convert_omega_to_specified_range(5*math.pi/2)
    assert pytest.approx(0) == MeasurementProcedure.convert_omega_to_specified_range(3* math.pi)

def test_residual_vector_r_and_residual_function_R():
    # This should be a residuel vector and norm close to zero
    # Arrange:
    # Define parameters:
    delta = math.pi/8
    omega = math.pi/5
    theta = 23*math.pi/16

    phi_1 = 0
    phi_2 = math.pi/4

    # Get the optically equivalent model
    model=mueller_calculus.optical_equivalent_model(
        delta=delta, theta=theta, omega=omega
    )

    S_in_phi1 = mueller_calculus.linearly_polarized_light(phi_1)
    S_in_phi2 = mueller_calculus.linearly_polarized_light(phi_2)

    S_out_phi1 = np.matmul(model, S_in_phi1)
    S_out_phi2 = np.matmul(model, S_in_phi2)

    OutgoingStokes1 = MeasuredStokesVector(phi=phi_1,
                                           stokes_vector=S_out_phi1)
    OutgoingStokes2 = MeasuredStokesVector(phi=phi_2,
                                           stokes_vector=S_out_phi2)

    mp = MeasurementProcedure([OutgoingStokes1, OutgoingStokes2])

    # insert the true values -> the residuals should be zero
    assert pytest.approx([0,0,0,0]) == mp.residual_vector_r(delta=delta, theta=theta, omega=omega)
    assert pytest.approx(0) == mp.residual_function_R(delta=delta, theta=theta, omega=omega)