import math

import pytest

import oem

def test_linearly_polarized_light():
    # Arrange
    phi1 = 0
    phi2 = math.pi/4

    # Act
    stokes_1 = oem.mueller_calculus.linearly_polarized_light(phi1)
    stokes_2 = oem.mueller_calculus.linearly_polarized_light(phi2)

    # Assert
    for (S_is, S_should) in zip(stokes_1, [1, 1, 0, 0]):
        assert pytest.approx(S_is) == S_should
    for (S_is, S_should) in zip(stokes_2, [1, 0, 1, 0]):
        assert pytest.approx(S_is) == S_should

def test_hand_circularly_polarized_light():
    # Act:
    rh_stokes = oem.mueller_calculus.right_hand_circularly_polarized_light()

    # Assert
    for (S_is, S_should) in zip(rh_stokes, [1, 0, 0, 1]):
        assert pytest.approx(S_is) == S_should

def test_oem():
    # Arrange: this should result in circulalry polarized light:
    S_in = oem.mueller_calculus.linearly_polarized_light(0)
    rotator = oem.mueller_calculus.rotator(math.pi/16)
    retarder = oem.mueller_calculus.linear_retarder(delta=math.pi/2, theta=math.pi/4+math.pi/16)

    # Act
    S_out = retarder @ rotator @ S_in

    # Assert
    for (S_is, S_should) in zip(S_out, [1, 0, 0, 1]):
        assert pytest.approx(S_is) == S_should

