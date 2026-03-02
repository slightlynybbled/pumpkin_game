import pygame


class SquirtButton:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(None, 32)
        self.text_color = (20, 24, 32)
        self.fill_color = (78, 148, 255)
        self.border_color = (30, 70, 140)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                print("SQIRT")

    def draw(self, surface):
        pygame.draw.rect(surface, self.fill_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=6)
        text_surface = self.font.render("SQIRT", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
