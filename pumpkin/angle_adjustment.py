import math

import pygame


class AngleAdjustmentTile:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.border_color = (120, 126, 140)
        self.line_color = (230, 233, 240)
        self.font = pygame.font.Font(None, 24)
        self.angle = 45
        self.min_angle = 0
        self.max_angle = 90
        self.double_click_ms = 350
        self.last_click_time = {"plus": 0, "minus": 0}
        self.button_size = max(26, self.rect.width // 4)
        self.button_padding = 12

    def _button_rects(self):
        minus_rect = pygame.Rect(0, 0, self.button_size, self.button_size)
        plus_rect = pygame.Rect(0, 0, self.button_size, self.button_size)
        plus_rect.topleft = (
            self.rect.left + self.button_padding,
            self.rect.bottom - self.button_padding - self.button_size,
        )
        minus_rect.topright = (
            self.rect.right - self.button_padding,
            self.rect.bottom - self.button_padding - self.button_size,
        )
        return minus_rect, plus_rect

    def _apply_angle_delta(self, delta):
        self.angle = max(self.min_angle, min(self.max_angle, self.angle + delta))

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        minus_rect, plus_rect = self._button_rects()
        if not self.rect.collidepoint(event.pos):
            return

        now = pygame.time.get_ticks()
        if plus_rect.collidepoint(event.pos):
            step = 10 if now - self.last_click_time["plus"] <= self.double_click_ms else 1
            self._apply_angle_delta(step)
            self.last_click_time["plus"] = now
        elif minus_rect.collidepoint(event.pos):
            step = 10 if now - self.last_click_time["minus"] <= self.double_click_ms else 1
            self._apply_angle_delta(-step)
            self.last_click_time["minus"] = now

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        mid_x = self.rect.left + self.button_padding
        mid_y = self.rect.top + self.rect.height // 2 - self.button_size // 2
        arm = min(self.rect.width, self.rect.height) // 3
        pygame.draw.line(surface, self.line_color, (mid_x, mid_y), (mid_x + arm, mid_y), 3)
        angle_rad = math.radians(self.angle)
        end_x = mid_x + int(arm * math.cos(angle_rad))
        end_y = mid_y - int(arm * math.sin(angle_rad))
        pygame.draw.line(surface, self.line_color, (mid_x, mid_y), (end_x, end_y), 3)
        minus_rect, plus_rect = self._button_rects()
        pygame.draw.rect(surface, self.line_color, minus_rect, 2, border_radius=4)
        pygame.draw.rect(surface, self.line_color, plus_rect, 2, border_radius=4)
        minus_label = self.font.render("-", True, self.line_color)
        plus_label = self.font.render("+", True, self.line_color)
        surface.blit(minus_label, minus_label.get_rect(center=minus_rect.center))
        surface.blit(plus_label, plus_label.get_rect(center=plus_rect.center))
        angle_label = self.font.render(f"{self.angle}", True, self.line_color)
        angle_rect = angle_label.get_rect(
            right=self.rect.right - self.button_padding,
            centery=minus_rect.top - 12,
        )
        surface.blit(angle_label, angle_rect)
