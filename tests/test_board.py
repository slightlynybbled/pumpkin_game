"""Unit tests for board water behavior."""

import pytest

from pumpkin.board import Board, RAIN_RATE_PER_SEC, SUNNY_DRY_MULTIPLIER, WEATHER_RAINY, WEATHER_SUNNY


def _empty_board(rows: int = 3, cols: int = 3) -> Board:
    board = Board(rows=rows, cols=cols, tile_size=1, origin=(0, 0))
    board.water = [[0.0 for _ in range(cols)] for _ in range(rows)]
    board.pumpkins = [[None for _ in range(cols)] for _ in range(rows)]
    board.sprout_chance_per_sec = 0.0
    return board


def test_add_water_distributes_to_neighbors() -> None:
    """Water should distribute to target and neighboring tiles."""
    board = _empty_board()
    board.add_water(1, 1, 10)
    assert board.water[1][1] == 5
    for row in range(3):
        for col in range(3):
            if (row, col) == (1, 1):
                continue
            assert board.water[row][col] == 2


def test_add_water_clamps_to_max() -> None:
    """Water should clamp to the board max."""
    board = _empty_board(rows=1, cols=1)
    board.max_water = 6
    board.add_water(0, 0, 10)
    assert board.water[0][0] == 5
    board.add_water(0, 0, 10)
    assert board.water[0][0] == 6


def test_update_rainy_increases_water() -> None:
    """Rain should increase water levels over time."""
    board = _empty_board(rows=1, cols=1)
    board.weather = WEATHER_RAINY
    board.update(1.0)
    assert board.water[0][0] == pytest.approx(RAIN_RATE_PER_SEC)


def test_update_sunny_dries_water() -> None:
    """Sunny weather should dry tiles faster than normal."""
    board = _empty_board(rows=1, cols=1)
    board.water[0][0] = board.max_water
    board.weather = WEATHER_SUNNY
    board.update(1.0)
    expected = board.max_water - board.dry_rate * SUNNY_DRY_MULTIPLIER
    assert board.water[0][0] == pytest.approx(expected)
