"""Mammoth tile rendering and rotation control."""

import pygame
from typing import Optional, Tuple

MAMMOTH_COLOR = (139, 94, 60)
ANGLE_MIN = -90
ANGLE_MAX = 90
BUTTON_MIN_SIZE = 26
BUTTON_WIDTH_RATIO = 4
BUTTON_PADDING = 10
DOUBLE_CLICK_MS = 350
BODY_WIDTH_RATIO = 0.32
BODY_HEIGHT_RATIO = 0.5
HEAD_RADIUS_RATIO = 0.35
TRUNK_LENGTH_RATIO = 0.3
TRUNK_THICKNESS = 4
BUTTON_BORDER_WIDTH = 2
BUTTON_RADIUS = 4
FONT_SIZE = 24
MOUSE_LEFT_BUTTON = 1


class Mammoth:
    """Render a mammoth placeholder and handle rotation input."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int]):
        """Initialize the mammoth tile.

        Args:
            rect: Tile rectangle (pygame.Rect or rect-like tuple).
        """
        self.rect = pygame.Rect(rect)
        self.color = MAMMOTH_COLOR
        self.angle = 0
        self.min_angle = ANGLE_MIN
        self.max_angle = ANGLE_MAX
        self.button_size = max(BUTTON_MIN_SIZE, self.rect.width // BUTTON_WIDTH_RATIO)
        self.button_padding = BUTTON_PADDING
        self.double_click_ms = DOUBLE_CLICK_MS
        self.last_click_time = {"plus": 0, "minus": 0}
        self.pivot: Optional[tuple[int, int]] = None

    def set_pivot(self, pivot: tuple[int, int]) -> None:
        """Set the rotation pivot point.

        Args:
            pivot: (x, y) position used as rotation center.
        """
        self.pivot = pivot

    def _button_rects(self) -> Tuple[pygame.Rect, pygame.Rect]:
        """Return rectangles for the minus and plus buttons."""
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

    def _apply_angle_delta(self, delta: int) -> None:
        """Adjust the mammoth angle within bounds.

        Args:
            delta: Signed change in degrees.
        """
        self.angle = max(self.min_angle, min(self.max_angle, self.angle + delta))

    def adjust_angle(self, delta: int) -> None:
        """Adjust the mammoth angle by a signed delta.

        Args:
            delta: Signed change in degrees.
        """
        self._apply_angle_delta(delta)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse click events.

        Args:
            event: Pygame event to process.
        """
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != MOUSE_LEFT_BUTTON:
            return
        minus_rect, plus_rect = self._button_rects()
        now = pygame.time.get_ticks()
        if plus_rect.collidepoint(event.pos):
            step = 10 if now - self.last_click_time["plus"] <= self.double_click_ms else 1
            self._apply_angle_delta(step)
            self.last_click_time["plus"] = now
        elif minus_rect.collidepoint(event.pos):
            step = 10 if now - self.last_click_time["minus"] <= self.double_click_ms else 1
            self._apply_angle_delta(-step)
            self.last_click_time["minus"] = now

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the mammoth and controls.

        Args:
            surface: Pygame surface to draw on.
        """
        body_width = int(self.rect.width * BODY_WIDTH_RATIO)
        body_height = int(self.rect.height * BODY_HEIGHT_RATIO)
        head_radius = int(body_width * HEAD_RADIUS_RATIO)
        trunk_length = int(body_height * TRUNK_LENGTH_RATIO)
        trunk_thickness = TRUNK_THICKNESS

        shape_width = max(body_width, head_radius * 2) + trunk_thickness
        shape_height = body_height + head_radius * 2 + trunk_length
        shape_surface = pygame.Surface((shape_width, shape_height), pygame.SRCALPHA)

        body_rect = pygame.Rect(
            (shape_width - body_width) // 2,
            head_radius,
            body_width,
            body_height,
        )
        pygame.draw.rect(shape_surface, self.color, body_rect, border_radius=body_width // 2)
        head_center = (shape_width // 2, head_radius)
        pygame.draw.circle(shape_surface, self.color, head_center, head_radius)
        trunk_start = (shape_width // 2, body_rect.bottom)
        trunk_end = (shape_width // 2, body_rect.bottom + trunk_length)
        pygame.draw.line(shape_surface, self.color, trunk_start, trunk_end, trunk_thickness)

        rotated = pygame.transform.rotate(shape_surface, -self.angle + 180)
        rotated_rect = rotated.get_rect()
        minus_rect, plus_rect = self._button_rects()
        available_height = minus_rect.top - self.rect.top - self.button_padding
        if self.pivot:
            rotated_rect.center = self.pivot
        else:
            center_y = self.rect.top + available_height // 2
            center_x = self.rect.centerx
            rotated_rect.center = (center_x, center_y)
        surface.blit(rotated, rotated_rect)

        pygame.draw.rect(
            surface, self.color, minus_rect, BUTTON_BORDER_WIDTH, border_radius=BUTTON_RADIUS
        )
        pygame.draw.rect(
            surface, self.color, plus_rect, BUTTON_BORDER_WIDTH, border_radius=BUTTON_RADIUS
        )
        font = pygame.font.Font(None, FONT_SIZE)
        minus_label = font.render("-", True, self.color)
        plus_label = font.render("+", True, self.color)
        surface.blit(minus_label, minus_label.get_rect(center=minus_rect.center))
        surface.blit(plus_label, plus_label.get_rect(center=plus_rect.center))
        angle_label = font.render(f"{self.angle}", True, self.color)
        angle_rect = angle_label.get_rect(
            center=(self.rect.centerx, minus_rect.centery)
        )
        surface.blit(angle_label, angle_rect)
