import pygame


class Mammoth:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.color = (139, 94, 60)

    def draw(self, surface):
        center = self.rect.center
        radius = min(self.rect.width, self.rect.height) // 2 - 6
        if radius > 0:
            pygame.draw.circle(surface, self.color, center, radius)
