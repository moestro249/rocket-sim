import pytest
from rocket_sim.simulation import simulate_flight


def test_flight_normal():
    result = simulate_flight(300, 1000, 500, 30000, 0.001)
    assert result["burn_time"] == pytest.approx(49.03, abs=0.01)
    assert result["apogee"] == pytest.approx(156300, rel=1e-3)
    assert result["total_time"] == pytest.approx(208.0, abs=0.2)


def test_total_time_is_sum():
    result = simulate_flight(300, 1000, 500, 30000, 0.001)
    assert result["total_time"] == pytest.approx(
        result["burn_time"] + result["coast_time"]
    )


def test_apogee_above_burnout():
    result = simulate_flight(300, 1000, 500, 30000, 0.001)
    assert result["apogee"] > result["burnout_height"]


def test_flight_error_is_passed_through():
    with pytest.raises(ValueError):
        simulate_flight(0, 1000, 500, 30000)