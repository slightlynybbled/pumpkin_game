import pygame


class QuantityAdjustmentTile:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.border_color = (120, 126, 140)
        self.track_color = (150, 160, 175)
        self.knob_color = (230, 233, 240)
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        track_y = self.rect.centery
        left = self.rect.left + 16
        right = self.rect.right - 16
        pygame.draw.line(surface, self.track_color, (left, track_y), (right, track_y), 4)
        knob_x = (left + right) // 2
        pygame.draw.circle(surface, self.knob_color, (knob_x, track_y), 6)
        left_label = self.font.render("0", True, self.knob_color)
        right_label = self.font.render("10", True, self.knob_color)
        surface.blit(left_label, (left - 4, track_y + 6))
        surface.blit(right_label, (right - 10, track_y + 6))
        title = self.font.render("QTY", True, self.knob_color)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + 14))
        surface.blit(title, title_rect)
