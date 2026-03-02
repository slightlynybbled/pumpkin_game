import pygame


class ForceAdjustmentTile:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.border_color = (120, 126, 140)
        self.track_color = (150, 160, 175)
        self.knob_color = (230, 233, 240)
        self.font = pygame.font.Font(None, 24)
        self.force = 5
        self.min_force = 0
        self.max_force = 10
        self.button_size = max(26, self.rect.width // 4)
        self.button_padding = 10

    def _button_rects(self):
        minus_rect = pygame.Rect(0, 0, self.button_size, self.button_size)
        plus_rect = pygame.Rect(0, 0, self.button_size, self.button_size)
        minus_rect.topleft = (
            self.rect.left + self.button_padding,
            self.rect.bottom - self.button_padding - self.button_size,
        )
        plus_rect.topright = (
            self.rect.right - self.button_padding,
            self.rect.bottom - self.button_padding - self.button_size,
        )
        return minus_rect, plus_rect

    def _apply_force_delta(self, delta):
        self.force = max(self.min_force, min(self.max_force, self.force + delta))

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        minus_rect, plus_rect = self._button_rects()
        if plus_rect.collidepoint(event.pos):
            self._apply_force_delta(1)
        elif minus_rect.collidepoint(event.pos):
            self._apply_force_delta(-1)

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        track_y = self.rect.centery
        left = self.rect.left + 16
        right = self.rect.right - 16
        pygame.draw.line(surface, self.track_color, (left, track_y), (right, track_y), 4)
        knob_x = int(left + (right - left) * (self.force / self.max_force))
        pygame.draw.circle(surface, self.knob_color, (knob_x, track_y), 6)
        left_label = self.font.render("0", True, self.knob_color)
        right_label = self.font.render("10", True, self.knob_color)
        surface.blit(left_label, (left - 4, track_y - 22))
        surface.blit(right_label, (right - 12, track_y - 22))
        title = self.font.render("FORCE", True, self.knob_color)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + 14))
        surface.blit(title, title_rect)
        minus_rect, plus_rect = self._button_rects()
        pygame.draw.rect(surface, self.knob_color, minus_rect, 2, border_radius=4)
        pygame.draw.rect(surface, self.knob_color, plus_rect, 2, border_radius=4)
        minus_label = self.font.render("-", True, self.knob_color)
        plus_label = self.font.render("+", True, self.knob_color)
        surface.blit(minus_label, minus_label.get_rect(center=minus_rect.center))
        surface.blit(plus_label, plus_label.get_rect(center=plus_rect.center))
