"""Quantity adjustment tile UI and input handling."""

import pygame
from typing import Tuple

QUANTITY_MIN = 1
QUANTITY_MAX = 10
QUANTITY_START = 5
FONT_SIZE = 24
BORDER_COLOR = (120, 126, 140)
LINE_COLOR = (230, 233, 240)
WATER_COLOR = (120, 180, 255)
BUTTON_MIN_SIZE = 26
BUTTON_WIDTH_RATIO = 4
BUTTON_PADDING = 10
BUTTON_RADIUS = 4
BUCKET_WIDTH_RATIO = 0.55
BUCKET_HEIGHT_RATIO = 0.45
BUCKET_PADDING = 12
FILL_MIN_HEIGHT = 4
BUCKET_INSET = 3
BUTTON_BORDER_WIDTH = 2
MOUSE_LEFT_BUTTON = 1


class QuantityAdjustmentTile:
    """Render and update the quantity adjustment tile."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int]):
        """Initialize the tile.

        Args:
            rect: Tile rectangle (pygame.Rect or rect-like tuple).
        """
        self.rect = pygame.Rect(rect)
        self.border_color = BORDER_COLOR
        self.line_color = LINE_COLOR
        self.water_color = WATER_COLOR
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.quantity = QUANTITY_START
        self.min_quantity = QUANTITY_MIN
        self.max_quantity = QUANTITY_MAX
        self.button_size = max(BUTTON_MIN_SIZE, self.rect.width // BUTTON_WIDTH_RATIO)
        self.button_padding = BUTTON_PADDING

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

    def _apply_quantity_delta(self, delta: int) -> None:
        """Adjust the quantity within bounds.

        Args:
            delta: Signed change in quantity.
        """
        self.quantity = max(
            self.min_quantity, min(self.max_quantity, self.quantity + delta)
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse click events.

        Args:
            event: Pygame event to process.
        """
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != MOUSE_LEFT_BUTTON:
            return
        minus_rect, plus_rect = self._button_rects()
        if plus_rect.collidepoint(event.pos):
            self._apply_quantity_delta(1)
        elif minus_rect.collidepoint(event.pos):
            self._apply_quantity_delta(-1)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the tile UI.

        Args:
            surface: Pygame surface to draw on.
        """
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
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

        bucket_width = int(self.rect.width * BUCKET_WIDTH_RATIO)
        bucket_height = int(self.rect.height * BUCKET_HEIGHT_RATIO)
        bucket_left = self.rect.centerx - bucket_width // 2
        bucket_bottom = minus_rect.top - BUCKET_PADDING
        bucket_top = bucket_bottom - bucket_height
        bucket_rect = pygame.Rect(bucket_left, bucket_top, bucket_width, bucket_height)

        fill_ratio = (self.quantity - self.min_quantity) / (
            self.max_quantity - self.min_quantity
        )
        fill_height = max(FILL_MIN_HEIGHT, int(bucket_rect.height * fill_ratio))
        fill_rect = pygame.Rect(
            bucket_rect.left + BUCKET_INSET,
            bucket_rect.bottom - fill_height,
            bucket_rect.width - BUCKET_INSET * 2,
            fill_height,
        )
        pygame.draw.rect(surface, self.water_color, fill_rect)
        pygame.draw.rect(surface, self.line_color, bucket_rect, 2)

        qty_label = self.font.render(str(self.quantity), True, self.line_color)
        qty_rect = qty_label.get_rect(center=bucket_rect.center)
        surface.blit(qty_label, qty_rect)
