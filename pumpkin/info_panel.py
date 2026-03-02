"""Info button UI and overlay rendering."""

from typing import Iterable

import pygame

INFO_BUTTON_SIZE = 28
INFO_BUTTON_MARGIN = 12
INFO_BUTTON_BG = (230, 233, 240)
INFO_BUTTON_FG = (20, 24, 32)
INFO_BUTTON_BORDER = (120, 126, 140)
INFO_BUTTON_BORDER_WIDTH = 2
INFO_FONT_SIZE = 20
INFO_TEXT_COLOR = (235, 235, 235)
INFO_BG_COLOR = (8, 10, 14, 220)
INFO_BORDER_COLOR = (120, 126, 140)
INFO_BORDER_WIDTH = 2
INFO_PADDING = 16
INFO_LINE_SPACING = 6
MOUSE_LEFT_BUTTON = 1


class InfoButton:
    """Render an info button and overlay text."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int]):
        """Initialize the info button.

        Args:
            rect: Button rectangle (pygame.Rect or rect-like tuple).
        """
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(None, INFO_FONT_SIZE)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse click events.

        Args:
            event: Pygame event to process.

        Returns:
            True if the button was clicked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT_BUTTON:
            return self.rect.collidepoint(event.pos)
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the info button.

        Args:
            surface: Pygame surface to draw on.
        """
        center = self.rect.center
        radius = self.rect.width // 2
        pygame.draw.circle(surface, INFO_BUTTON_BG, center, radius)
        pygame.draw.circle(surface, INFO_BUTTON_BORDER, center, radius, INFO_BUTTON_BORDER_WIDTH)
        label = self.font.render("i", True, INFO_BUTTON_FG)
        surface.blit(label, label.get_rect(center=center))

    def draw_overlay(self, surface: pygame.Surface, lines: Iterable[str]) -> None:
        """Draw a help overlay with the provided lines.

        Args:
            surface: Pygame surface to draw on.
            lines: Text lines to display.
        """
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill(INFO_BG_COLOR)
        surface.blit(overlay, (0, 0))

        font = pygame.font.Font(None, INFO_FONT_SIZE)
        line_height = font.get_linesize()
        text_lines = [font.render(line, True, INFO_TEXT_COLOR) for line in lines]
        total_height = len(text_lines) * line_height + max(0, len(text_lines) - 1) * INFO_LINE_SPACING
        box_width = max((line.get_width() for line in text_lines), default=0) + INFO_PADDING * 2
        box_height = total_height + INFO_PADDING * 2
        box_rect = pygame.Rect(
            (surface.get_width() - box_width) // 2,
            (surface.get_height() - box_height) // 2,
            box_width,
            box_height,
        )
        pygame.draw.rect(surface, INFO_BORDER_COLOR, box_rect, INFO_BORDER_WIDTH)

        y = box_rect.top + INFO_PADDING
        for line_surface in text_lines:
            surface.blit(line_surface, (box_rect.left + INFO_PADDING, y))
            y += line_height + INFO_LINE_SPACING
