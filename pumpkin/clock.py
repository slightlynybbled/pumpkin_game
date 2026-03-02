import pygame


class ClockTile:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.border_color = (120, 126, 140)
        self.face_color = (230, 233, 240)
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        center = self.rect.center
        radius = min(self.rect.width, self.rect.height) // 3
        if radius > 0:
            pygame.draw.circle(surface, self.face_color, center, radius, 2)
            pygame.draw.line(
                surface,
                self.face_color,
                center,
                (center[0], center[1] - radius + 4),
                2,
            )
            pygame.draw.line(
                surface,
                self.face_color,
                center,
                (center[0] + radius - 6, center[1]),
                2,
            )
        title = self.font.render("CLOCK", True, self.face_color)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + 14))
        surface.blit(title, title_rect)
