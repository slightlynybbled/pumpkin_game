"""Unit tests for pumpkin growth behavior."""

from pumpkin import pumpkin as pumpkin_module
from pumpkin.pumpkin import Pumpkin


def test_pumpkin_grows_and_harvests() -> None:
    """Pumpkin should harvest at max health under perfect water."""
    plant = Pumpkin()
    harvested = False
    for _ in range(int(pumpkin_module.HEALTH_MAX)):
        harvested = plant.update(1.0, pumpkin_module.PERFECT_WATER)
    assert harvested is True
    assert plant.harvested is True
    assert plant.dead is False


def test_pumpkin_dies_after_stagnation() -> None:
    """Pumpkin should die after extended poor watering."""
    plant = Pumpkin()
    plant.update(pumpkin_module.STAGNANT_LIMIT / 2, pumpkin_module.WATER_MIN)
    harvested = plant.update(pumpkin_module.STAGNANT_LIMIT / 2, pumpkin_module.WATER_MIN)
    assert harvested is False
    assert plant.dead is True
    assert plant.harvested is False
