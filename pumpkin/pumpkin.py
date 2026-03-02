class Pumpkin:
    def __init__(self):
        self.health = 0
        self.max_health = 10
        self.min_water = 0
        self.max_water = 10
        self.grow_min = 3
        self.grow_max = 7
        self.perfect_water = 5
        self.harvested = False
        self.dead = False
        self.stagnant_time = 0.0
        self.stagnant_limit = 10.0

    def update(self, dt, water_level):
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

        rate = 1.0 if water == self.perfect_water else 0.5
        prev_health = self.health
        self.health = min(self.max_health, self.health + rate * dt)
        if self.health > prev_health:
            self.stagnant_time = 0.0
        if self.health >= self.max_health:
            self.harvested = True
            return True
        return False
