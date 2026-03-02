import pygame


class Scoreboard:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(None, 32)
        self.text_color = (235, 235, 235)
        self.border_color = (120, 126, 140)

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        text_surface = self.font.render("SCOREBOARD", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
