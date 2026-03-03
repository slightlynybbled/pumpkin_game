"""Force adjustment tile UI and input handling."""

import pygame

from pumpkin.ui_helpers import button_rects

FORCE_MIN = 1
FORCE_MAX = 10
FORCE_START = 5
FONT_SIZE = 24
BORDER_COLOR = (120, 126, 140)
TRACK_COLOR = (150, 160, 175)
KNOB_COLOR = (230, 233, 240)
BUTTON_MIN_SIZE = 26
BUTTON_WIDTH_RATIO = 4
BUTTON_PADDING = 10
BUTTON_RADIUS = 4
TRACK_PADDING = 16
TRACK_THICKNESS = 4
KNOB_RADIUS = 6
LABEL_Y_OFFSET = 22
LABEL_LEFT_OFFSET = 4
LABEL_RIGHT_OFFSET = 12
TITLE_Y_OFFSET = 14
BUTTON_BORDER_WIDTH = 2
MOUSE_LEFT_BUTTON = 1


class ForceAdjustmentTile:
    """Render and update the force adjustment tile."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int]):
        """Initialize the tile.

        Args:
            rect: Tile rectangle (pygame.Rect or rect-like tuple).
        """
        self.rect = pygame.Rect(rect)
        self.border_color = BORDER_COLOR
        self.track_color = TRACK_COLOR
        self.knob_color = KNOB_COLOR
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.force = FORCE_START
        self.min_force = FORCE_MIN
        self.max_force = FORCE_MAX
        self.button_size = max(BUTTON_MIN_SIZE, self.rect.width // BUTTON_WIDTH_RATIO)
        self.button_padding = BUTTON_PADDING

    def _apply_force_delta(self, delta: int) -> None:
        """Adjust the force within bounds.

        Args:
            delta: Signed change in force.
        """
        self.force = max(self.min_force, min(self.max_force, self.force + delta))

    def adjust_force(self, delta: int) -> None:
        """Adjust the force by a signed delta.

        Args:
            delta: Signed change in force.
        """
        self._apply_force_delta(delta)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse click events.

        Args:
            event: Pygame event to process.
        """
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != MOUSE_LEFT_BUTTON:
            return
        minus_rect, plus_rect = button_rects(self.rect, self.button_size, self.button_padding)
        if plus_rect.collidepoint(event.pos):
            self._apply_force_delta(1)
        elif minus_rect.collidepoint(event.pos):
            self._apply_force_delta(-1)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the tile UI.

        Args:
            surface: Pygame surface to draw on.
        """
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        track_y = self.rect.centery
        left = self.rect.left + TRACK_PADDING
        right = self.rect.right - TRACK_PADDING
        pygame.draw.line(
            surface, self.track_color, (left, track_y), (right, track_y), TRACK_THICKNESS
        )
        knob_x = int(left + (right - left) * (self.force / self.max_force))
        pygame.draw.circle(surface, self.knob_color, (knob_x, track_y), KNOB_RADIUS)
        left_label = self.font.render(str(self.min_force), True, self.knob_color)
        right_label = self.font.render(str(self.max_force), True, self.knob_color)
        surface.blit(left_label, (left - LABEL_LEFT_OFFSET, track_y - LABEL_Y_OFFSET))
        surface.blit(right_label, (right - LABEL_RIGHT_OFFSET, track_y - LABEL_Y_OFFSET))
        title = self.font.render("FORCE", True, self.knob_color)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + TITLE_Y_OFFSET))
        surface.blit(title, title_rect)
        minus_rect, plus_rect = button_rects(self.rect, self.button_size, self.button_padding)
        pygame.draw.rect(
            surface, self.knob_color, minus_rect, BUTTON_BORDER_WIDTH, border_radius=BUTTON_RADIUS
        )
        pygame.draw.rect(
            surface, self.knob_color, plus_rect, BUTTON_BORDER_WIDTH, border_radius=BUTTON_RADIUS
        )
        minus_label = self.font.render("-", True, self.knob_color)
        plus_label = self.font.render("+", True, self.knob_color)
        surface.blit(minus_label, minus_label.get_rect(center=minus_rect.center))
        surface.blit(plus_label, plus_label.get_rect(center=plus_rect.center))
