"""Weather adjustment tile placeholder rendering."""

import pygame

WEATHER_MIN = -10
WEATHER_MAX = 10
FONT_SIZE = 24
BORDER_COLOR = (120, 126, 140)
TRACK_COLOR = (150, 160, 175)
KNOB_COLOR = (230, 233, 240)
TRACK_PADDING = 16
TRACK_THICKNESS = 4
KNOB_RADIUS = 6
LABEL_Y_OFFSET = 6
LABEL_LEFT_OFFSET = 6
LABEL_RIGHT_OFFSET = 10
TITLE_Y_OFFSET = 14


class WeatherAdjustmentTile:
    """Render a placeholder weather adjustment tile."""

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
        knob_x = (left + right) // 2
        pygame.draw.circle(surface, self.knob_color, (knob_x, track_y), KNOB_RADIUS)
        left_label = self.font.render(str(WEATHER_MIN), True, self.knob_color)
        right_label = self.font.render(str(WEATHER_MAX), True, self.knob_color)
        surface.blit(left_label, (left - LABEL_LEFT_OFFSET, track_y + LABEL_Y_OFFSET))
        surface.blit(right_label, (right - LABEL_RIGHT_OFFSET, track_y + LABEL_Y_OFFSET))
        title = self.font.render("WEATHER", True, self.knob_color)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + TITLE_Y_OFFSET))
        surface.blit(title, title_rect)
