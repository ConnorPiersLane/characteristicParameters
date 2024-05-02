import math

import pytest
from characteristicParameters.triangle_wave_functions import T_pi, T_pi_2


def test_T_pi():
    assert pytest.approx(T_pi(math.pi / 2)) == math.pi / 2
    assert pytest.approx(T_pi(3 * math.pi / 2)) == math.pi / 2
    assert pytest.approx(T_pi(5 * math.pi / 2)) == math.pi / 2

    assert pytest.approx(T_pi(math.pi)) == math.pi
    assert pytest.approx(T_pi(5 * math.pi)) == math.pi


def test_T_pi_2():
    assert pytest.approx(T_pi_2(math.pi / 2)) == math.pi / 2
    assert pytest.approx(T_pi_2(3 * math.pi / 2)) == math.pi / 2
    assert pytest.approx(T_pi_2(5 * math.pi / 2)) == math.pi / 2

    assert pytest.approx(T_pi_2(math.pi)) == 0
    assert pytest.approx(T_pi_2(5 * math.pi)) == 0
