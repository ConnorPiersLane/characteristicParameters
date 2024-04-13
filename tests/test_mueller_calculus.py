import math

import numpy as np
import pytest

import characteristicParameters

def test_linearly_polarized_light():
    # Arrange
    phi1 = 0
    phi2 = math.pi/4

    # Act
    stokes_1 = characteristicParameters.muellerCalculus.linearly_polarized_light(phi1)
    stokes_2 = characteristicParameters.muellerCalculus.linearly_polarized_light(phi2)

    # Assert
    for (S_is, S_should) in zip(stokes_1, [1, 1, 0, 0]):
        assert pytest.approx(S_is) == S_should
    for (S_is, S_should) in zip(stokes_2, [1, 0, 1, 0]):
        assert pytest.approx(S_is) == S_should

def test_hand_circularly_polarized_light():
    # Act:
    rh_stokes = characteristicParameters.muellerCalculus.right_hand_circularly_polarized_light()

    # Assert
    for (S_is, S_should) in zip(rh_stokes, [1, 0, 0, 1]):
        assert pytest.approx(S_is) == S_should

def test_rotator():
    # Arrange: Rotator that rotates 45°
    R = characteristicParameters.muellerCalculus.rotator(math.pi / 4)

    # Test 1
    S_in1 = [1,1,0,0]
    S_out_expected1 = [1,0,1,0]
    # Test 2
    S_in2 = [1,0,0,-1]
    S_out_expected2 = [1, 0, 0, -1]

    # Act and Assert
    assert pytest.approx(S_out_expected1) == list(np.matmul(R, S_in1))
    assert pytest.approx(S_out_expected2) == list(np.matmul(R, S_in2))

def test_linear_retarder():

    # Test 1
    # Linearly polarized light entering a quarter wave plate should lead to circulalry polarized light
    LR = characteristicParameters.muellerCalculus.linear_retarder(delta=math.pi / 2, theta=0)
    S_in_45 = [1, 0, 1, 0]
    S_out_expected = [1, 0, 0, -1]
    pytest.approx(S_out_expected) == list(np.matmul(LR, S_in_45))

    # Test 2
    # Linearly polarized light entering a half wave plate should lead to linear polarized light
    S_in_45 = [1, 0, 1, 0]
    S_out_expected = [1, 0, -1, 0]
    pytest.approx(S_out_expected) == list(np.matmul(LR, S_in_45))

def test_optical_equivalent_model():
    # Arrange: this should result in circulalry polarized light:
    S_in = characteristicParameters.muellerCalculus.linearly_polarized_light(0)
    delta = math.pi / 2
    theta = math.pi / 4 + math.pi / 16
    omega = math.pi / 16

    optical_eq_model = characteristicParameters.muellerCalculus.optical_equivalent_model(
        delta=delta, theta=theta, omega=omega
    )

    # Act
    S_out = optical_eq_model @ S_in

    # Assert
    for (S_is, S_should) in zip(S_out, [1, 0, 0, 1]):
        assert pytest.approx(S_is) == S_should

