import math
import pytest

from rocket_sim.models.rocket import Rocket


@pytest.fixture
def rocket():
    return Rocket(
        dry_mass=500,
        fuel_mass=1500,
        diameter=1.2,
        drag_coefficient=0.4,
    )


def test_rocket_creation(rocket):
    assert rocket.dry_mass == 500
    assert rocket.fuel_mass == 1500
    assert rocket.diameter == 1.2
    assert rocket.drag_coefficient == 0.4


def test_total_mass(rocket):
    assert rocket.total_mass == 2000


def test_cross_section_area(rocket):
    assert rocket.cross_section_area == pytest.approx(math.pi * 1.2**2 / 4)


def test_zero_fuel_is_allowed():
    rocket = Rocket(500, 0, 1.2, 0.4)
    assert rocket.total_mass == 500


@pytest.mark.parametrize(
    "parameters",
    [
        (-500, 1500, 1.2, 0.4),
        (500, -1500, 1.2, 0.4),
        (500, 1500, 0, 0.4),
        (500, 1500, 1.2, -0.4),
        (float("inf"), 1500, 1.2, 0.4),
        (500, float("nan"), 1.2, 0.4),
    ],
)
def test_invalid_parameters(parameters):
    with pytest.raises(ValueError):
        Rocket(*parameters)
