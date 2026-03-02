import math

import pygame

ANGLE_MIN = 0
ANGLE_MAX = 90
ANGLE_START = 45
DOUBLE_CLICK_MS = 350
FONT_SIZE = 24
LINE_COLOR = (230, 233, 240)
BORDER_COLOR = (120, 126, 140)
BUTTON_MIN_SIZE = 26
BUTTON_WIDTH_RATIO = 4
BUTTON_PADDING = 12
BUTTON_RADIUS = 4
BUTTON_BORDER_WIDTH = 2
LINE_WIDTH = 3
ARM_SCALE = 3
ANGLE_LABEL_OFFSET = 12
MOUSE_LEFT_BUTTON = 1


class AngleAdjustmentTile:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.border_color = BORDER_COLOR
        self.line_color = LINE_COLOR
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.angle = ANGLE_START
        self.min_angle = ANGLE_MIN
        self.max_angle = ANGLE_MAX
        self.double_click_ms = DOUBLE_CLICK_MS
        self.last_click_time = {"plus": 0, "minus": 0}
        self.button_size = max(BUTTON_MIN_SIZE, self.rect.width // BUTTON_WIDTH_RATIO)
        self.button_padding = BUTTON_PADDING

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

    def _apply_angle_delta(self, delta):
        self.angle = max(self.min_angle, min(self.max_angle, self.angle + delta))

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != MOUSE_LEFT_BUTTON:
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
        arm = min(self.rect.width, self.rect.height) // ARM_SCALE
        pygame.draw.line(
            surface, self.line_color, (mid_x, mid_y), (mid_x + arm, mid_y), LINE_WIDTH
        )
        angle_rad = math.radians(self.angle)
        end_x = mid_x + int(arm * math.cos(angle_rad))
        end_y = mid_y - int(arm * math.sin(angle_rad))
        pygame.draw.line(surface, self.line_color, (mid_x, mid_y), (end_x, end_y), LINE_WIDTH)
        minus_rect, plus_rect = self._button_rects()
        pygame.draw.rect(
            surface, self.line_color, minus_rect, BUTTON_BORDER_WIDTH, border_radius=BUTTON_RADIUS
        )
        pygame.draw.rect(
            surface, self.line_color, plus_rect, BUTTON_BORDER_WIDTH, border_radius=BUTTON_RADIUS
        )
        minus_label = self.font.render("-", True, self.line_color)
        plus_label = self.font.render("+", True, self.line_color)
        surface.blit(minus_label, minus_label.get_rect(center=minus_rect.center))
        surface.blit(plus_label, plus_label.get_rect(center=plus_rect.center))
        angle_label = self.font.render(f"{self.angle}", True, self.line_color)
        angle_rect = angle_label.get_rect(
            right=self.rect.right - self.button_padding,
            centery=minus_rect.top - ANGLE_LABEL_OFFSET,
        )
        surface.blit(angle_label, angle_rect)
