import pygame


class Board:
    def __init__(self, rows=8, cols=8, tile_size=64, origin=(0, 0)):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.origin = origin
        self.colors = ((230, 233, 240), (180, 188, 204))

    def draw(self, surface):
        ox, oy = self.origin
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.colors[(row + col) % 2]
                rect = pygame.Rect(
                    ox + col * self.tile_size,
                    oy + row * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(surface, color, rect)
