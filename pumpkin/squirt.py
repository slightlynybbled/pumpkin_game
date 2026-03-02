"""Squirt button UI and click handling."""

import pygame
from typing import Callable

FONT_SIZE = 32
TEXT_COLOR = (20, 24, 32)
FILL_COLOR = (78, 148, 255)
BORDER_COLOR = (30, 70, 140)
BUTTON_RADIUS = 6
BUTTON_BORDER_WIDTH = 2
MOUSE_LEFT_BUTTON = 1


class SquirtButton:
    """Render a squirt button and notify on click."""

    def __init__(
        self,
        rect: pygame.Rect | tuple[int, int, int, int],
        on_click: Callable[[], None] | None = None,
    ):
        """Initialize the button.

        Args:
            rect: Button rectangle (pygame.Rect or rect-like tuple).
            on_click: Optional callback for click events.
        """
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.text_color = TEXT_COLOR
        self.fill_color = FILL_COLOR
        self.border_color = BORDER_COLOR
        self.on_click = on_click

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse click events.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT_BUTTON:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button.

        Args:
            surface: Pygame surface to draw on.
        """
        pygame.draw.rect(surface, self.fill_color, self.rect, border_radius=BUTTON_RADIUS)
        pygame.draw.rect(
            surface,
            self.border_color,
            self.rect,
            BUTTON_BORDER_WIDTH,
            border_radius=BUTTON_RADIUS,
        )
        text_surface = self.font.render("SQIRT", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
