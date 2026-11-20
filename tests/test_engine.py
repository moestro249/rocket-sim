
import math
import pytest

from rocket_sim.models.engine import Engine


def test_engine_creation():
    engine = Engine(
        thrust=30000,
        isp=300,
        burn_time=49.03,
        fuel_mass=500,
    )

    assert engine.thrust == 30000
    assert engine.isp == 300
    assert engine.burn_time == 49.03
    assert engine.fuel_mass == 500


def test_mass_flow_rate():
    engine = Engine(
        thrust=30000,
        isp=300,
        burn_time=49.03,
        fuel_mass=500,
    )

    expected = 30000 / (300 * 9.80665)

    assert engine.mass_flow_rate == pytest.approx(expected)


def test_total_impulse():
    engine = Engine(
        thrust=30000,
        isp=300,
        burn_time=49.03,
        fuel_mass=500,
    )

    expected = 30000 * 49.03

    assert engine.total_impulse == pytest.approx(expected)


def test_calculated_fuel_mass():
    engine = Engine(
        thrust=30000,
        isp=300,
        burn_time=49.03,
        fuel_mass=500,
    )

    expected = (
        30000 / (300 * 9.80665)
    ) * 49.03

    assert engine.calculated_fuel_mass == pytest.approx(expected)


@pytest.mark.parametrize(
    "parameter, value",
    [
        ("thrust", 0),
        ("thrust", -100),
        ("isp", 0),
        ("isp", -10),
        ("burn_time", 0),
        ("burn_time", -5),
        ("fuel_mass", 0),
        ("fuel_mass", -100),
    ],
)
def test_invalid_positive_parameters(parameter, value):
    params = {
        "thrust": 30000,
        "isp": 300,
        "burn_time": 49.03,
        "fuel_mass": 500,
    }

    params[parameter] = value

    with pytest.raises(ValueError):
        Engine(**params)


@pytest.mark.parametrize(
    "parameter, value",
    [
        ("thrust", float("inf")),
        ("isp", float("-inf")),
        ("burn_time", float("nan")),
        ("fuel_mass", float("inf")),
    ],
)
def test_non_finite_parameters(parameter, value):
    params = {
        "thrust": 30000,
        "isp": 300,
        "burn_time": 49.03,
        "fuel_mass": 500,
    }

    params[parameter] = value

    with pytest.raises(ValueError):
        Engine(**params)
