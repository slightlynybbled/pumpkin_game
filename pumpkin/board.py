import random

import pygame

from pumpkin.pumpkin import Pumpkin


class Board:
    def __init__(self, rows=8, cols=8, tile_size=64, origin=(0, 0)):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.origin = origin
        self.max_water = 10
        self.min_water = 0
        self.dry_rate = 0.1
        self.water = [
            [random.randint(self.min_water, self.max_water) for _ in range(cols)]
            for _ in range(rows)
        ]
        self.pumpkins = [[None for _ in range(cols)] for _ in range(rows)]
        self.sprout_chance_per_sec = 0.002
        self.harvested_total = 0
        self.spawned_total = 0
        self.wet_color = (82, 50, 28)
        self.dry_color = (176, 126, 82)
        self._seed_pumpkins(3)

    def _seed_pumpkins(self, count):
        total_tiles = self.rows * self.cols
        count = min(count, total_tiles)
        indices = random.sample(range(total_tiles), count)
        for index in indices:
            row = index // self.cols
            col = index % self.cols
            self.pumpkins[row][col] = Pumpkin()
            self.spawned_total += 1

    def update(self, dt):
        for row in range(self.rows):
            for col in range(self.cols):
                self.water[row][col] = max(
                    self.min_water, self.water[row][col] - self.dry_rate * dt
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

    def add_water(self, row, col, quantity):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        center_amount = int(round(quantity * 0.5))
        neighbor_amount = int(round(quantity * 0.2))
        self._apply_water(row, col, center_amount)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                self._apply_water(row + dr, col + dc, neighbor_amount)

    def _apply_water(self, row, col, amount):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        self.water[row][col] = max(
            self.min_water,
            min(self.max_water, self.water[row][col] + amount),
        )

    def _tile_color(self, row, col):
        ratio = self.water[row][col] / self.max_water
        r = int(self.dry_color[0] + (self.wet_color[0] - self.dry_color[0]) * ratio)
        g = int(self.dry_color[1] + (self.wet_color[1] - self.dry_color[1]) * ratio)
        b = int(self.dry_color[2] + (self.wet_color[2] - self.dry_color[2]) * ratio)
        return (r, g, b)

    def draw(self, surface):
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
                    max_radius = self.tile_size // 2 - 6
                    ratio = min(pumpkin.health, pumpkin.max_health) / pumpkin.max_health
                    radius = max(3, int(max_radius * ratio))
                    center = rect.center
                    pygame.draw.circle(surface, (232, 144, 64), center, radius)
