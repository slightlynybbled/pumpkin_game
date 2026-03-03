"""Pumpkin growth logic."""

HEALTH_START = 0
HEALTH_MAX = 10
WATER_MIN = 0
WATER_MAX = 10
GROW_MIN = 3
GROW_MAX = 7
PERFECT_WATER = 5
GROW_RATE_NORMAL = 0.5
GROW_RATE_PERFECT = 1.0
STAGNANT_LIMIT = 10.0


class Pumpkin:
    """Track pumpkin health and growth state."""

    def __init__(self):
        """Initialize a new pumpkin."""
        self.health = HEALTH_START
        self.max_health = HEALTH_MAX
        self.min_water = WATER_MIN
        self.max_water = WATER_MAX
        self.grow_min = GROW_MIN
        self.grow_max = GROW_MAX
        self.perfect_water = PERFECT_WATER
        self.harvested = False
        self.dead = False
        self.stagnant_time = 0.0
        self.stagnant_limit = STAGNANT_LIMIT

    def update(self, dt: float, water_level: float) -> bool:
        """Advance pumpkin growth state.

        Args:
            dt: Delta time in seconds.
            water_level: Current water level from the hosting tile.
        """
        if self.harvested:
            return False
        if self.dead:
            return False
        water = max(self.min_water, min(self.max_water, water_level))
        if not (self.grow_min <= water <= self.grow_max):
            self.stagnant_time += dt
            if self.stagnant_time >= self.stagnant_limit:
                self.dead = True
            return False

        rate = GROW_RATE_PERFECT if water == self.perfect_water else GROW_RATE_NORMAL
        prev_health = self.health
        self.health = min(self.max_health, self.health + rate * dt)
        if self.health > prev_health:
            self.stagnant_time = 0.0
        if self.health >= self.max_health:
            self.harvested = True
            return True
        return False
