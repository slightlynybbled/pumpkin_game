"""Board state, water simulation, and pumpkin management."""

import random
from typing import Optional, Tuple

import pygame

from pumpkin.pumpkin import Pumpkin

DEFAULT_ROWS = 8
DEFAULT_COLS = 8
DEFAULT_TILE_SIZE = 64
WATER_MIN = 0
WATER_MAX = 10
DRY_RATE_PER_SEC = 0.1
WET_COLOR = (82, 50, 28)
DRY_COLOR = (176, 126, 82)
SPROUT_CHANCE_PER_SEC = 0.002
INITIAL_PUMPKINS = 3
WATER_CENTER_RATIO = 0.5
WATER_NEIGHBOR_RATIO = 0.2
PUMPKIN_COLOR = (232, 144, 64)
PUMPKIN_MAX_RADIUS_MARGIN = 6
PUMPKIN_MIN_RADIUS = 3
WEATHER_RAINY = "rainy"
WEATHER_CLOUDY = "cloudy"
WEATHER_SUNNY = "sunny"
SUNNY_DRY_MULTIPLIER = 2.0
NORMAL_DRY_MULTIPLIER = 1.0
RAIN_RATE_PER_SEC = 0.15


class Board:
    """Manage board tiles, water levels, and pumpkins."""

    def __init__(
        self,
        rows: int = DEFAULT_ROWS,
        cols: int = DEFAULT_COLS,
        tile_size: int = DEFAULT_TILE_SIZE,
        origin: Tuple[int, int] = (0, 0),
    ):
        """Initialize the board grid and state.

        Args:
            rows: Number of tile rows.
            cols: Number of tile columns.
            tile_size: Pixel size of each tile.
            origin: Top-left pixel position of the board.
        """
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.origin = origin
        self.max_water = WATER_MAX
        self.min_water = WATER_MIN
        self.dry_rate = DRY_RATE_PER_SEC
        self.water: list[list[float]] = [
            [float(random.randint(self.min_water, self.max_water)) for _ in range(cols)]
            for _ in range(rows)
        ]
        self.pumpkins: list[list[Optional[Pumpkin]]] = [
            [None for _ in range(cols)] for _ in range(rows)
        ]
        self.sprout_chance_per_sec = SPROUT_CHANCE_PER_SEC
        self.weather = WEATHER_CLOUDY
        self.harvested_total = 0
        self.spawned_total = 0
        self.wet_color = WET_COLOR
        self.dry_color = DRY_COLOR
        self._seed_pumpkins(INITIAL_PUMPKINS)

    def _seed_pumpkins(self, count: int) -> None:
        """Seed an initial number of pumpkins.

        Args:
            count: Number of pumpkins to place.
        """
        total_tiles = self.rows * self.cols
        count = min(count, total_tiles)
        indices = random.sample(range(total_tiles), count)
        for index in indices:
            row = index // self.cols
            col = index % self.cols
            self.pumpkins[row][col] = Pumpkin()
            self.spawned_total += 1

    def update(self, dt: float) -> None:
        """Advance board simulation.

        Args:
            dt: Delta time in seconds.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.weather == WEATHER_RAINY:
                    self.water[row][col] = min(
                        self.max_water, self.water[row][col] + RAIN_RATE_PER_SEC * dt
                    )
                else:
                    multiplier = (
                        SUNNY_DRY_MULTIPLIER if self.weather == WEATHER_SUNNY else NORMAL_DRY_MULTIPLIER
                    )
                    self.water[row][col] = max(
                        self.min_water, self.water[row][col] - self.dry_rate * multiplier * dt
                    )
                if self.pumpkins[row][col] is None:
                    if random.random() < self.sprout_chance_per_sec * dt:
                        self.pumpkins[row][col] = Pumpkin()
                        self.spawned_total += 1
                pumpkin = self.pumpkins[row][col]
                if pumpkin:
                    harvested = pumpkin.update(dt, self.water[row][col])
                    if harvested:
                        self.harvested_total += 1
                        self.pumpkins[row][col] = None
                    elif pumpkin.dead:
                        self.pumpkins[row][col] = None

    def add_water(self, row: int, col: int, quantity: int) -> None:
        """Apply water to a tile and its neighbors.

        Args:
            row: Target tile row.
            col: Target tile column.
            quantity: Water amount to distribute.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        center_amount = int(round(quantity * WATER_CENTER_RATIO))
        neighbor_amount = int(round(quantity * WATER_NEIGHBOR_RATIO))
        self._apply_water(row, col, center_amount)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                self._apply_water(row + dr, col + dc, neighbor_amount)

    def set_weather(self, weather: str) -> None:
        """Set the current weather state.

        Args:
            weather: Weather state string.
        """
        self.weather = weather

    def _apply_water(self, row: int, col: int, amount: int) -> None:
        """Apply water to a single tile.

        Args:
            row: Tile row.
            col: Tile column.
            amount: Water amount to add.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        self.water[row][col] = max(
            self.min_water,
            min(self.max_water, self.water[row][col] + amount),
        )

    def _tile_color(self, row: int, col: int) -> Tuple[int, int, int]:
        """Return a color based on tile water level.

        Args:
            row: Tile row.
            col: Tile column.
        """
        ratio = self.water[row][col] / self.max_water
        r = int(self.dry_color[0] + (self.wet_color[0] - self.dry_color[0]) * ratio)
        g = int(self.dry_color[1] + (self.wet_color[1] - self.dry_color[1]) * ratio)
        b = int(self.dry_color[2] + (self.wet_color[2] - self.dry_color[2]) * ratio)
        return (r, g, b)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the board and any pumpkins.

        Args:
            surface: Pygame surface to draw on.
        """
        ox, oy = self.origin
        for row in range(self.rows):
            for col in range(self.cols):
                color = self._tile_color(row, col)
                rect = pygame.Rect(
                    ox + col * self.tile_size,
                    oy + row * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(surface, color, rect)
                pumpkin = self.pumpkins[row][col]
                if pumpkin:
                    max_radius = self.tile_size // 2 - PUMPKIN_MAX_RADIUS_MARGIN
                    ratio = min(pumpkin.health, pumpkin.max_health) / pumpkin.max_health
                    radius = max(PUMPKIN_MIN_RADIUS, int(max_radius * ratio))
                    center = rect.center
                    pygame.draw.circle(surface, PUMPKIN_COLOR, center, radius)
