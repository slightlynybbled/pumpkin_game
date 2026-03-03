"""Weather adjustment tile placeholder rendering."""

import math
import pygame

WEATHER_RAINY = "rainy"
WEATHER_CLOUDY = "cloudy"
WEATHER_SUNNY = "sunny"
FONT_SIZE = 24
BOLD_FONT_SIZE = 28
BORDER_COLOR = (120, 126, 140)
KNOB_COLOR = (230, 233, 240)
TITLE_Y_OFFSET = 14
SUN_COLOR = (246, 196, 72)
SUN_CORE_COLOR = (252, 224, 128)
SUN_RAY_COUNT = 8
SUN_RAY_LENGTH = 10
SUN_RAY_WIDTH = 2
RAIN_COLOR = (120, 180, 255)
CLOUD_COLOR = (235, 235, 240)
CLOUD_RADIUS = 10
CLOUD_SMALL_RADIUS = 8
CLOUD_OFFSET_X = 12
CLOUD_OFFSET_Y = 4
CLOUD_BASE_WIDTH = 32
CLOUD_BASE_HEIGHT = 12


class WeatherAdjustmentTile:
    """Render a placeholder weather adjustment tile."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int]):
        """Initialize the tile.

        Args:
            rect: Tile rectangle (pygame.Rect or rect-like tuple).
        """
        self.rect = pygame.Rect(rect)
        self.border_color = BORDER_COLOR
        self.knob_color = KNOB_COLOR
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.bold_font = pygame.font.Font(None, BOLD_FONT_SIZE)
        self.state = WEATHER_CLOUDY

    def set_state(self, state: str) -> None:
        """Set the current weather state.

        Args:
            state: Weather state string.
        """
        self.state = state

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the tile UI.

        Args:
            surface: Pygame surface to draw on.
        """
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        title = self.font.render("WEATHER", True, self.knob_color)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + TITLE_Y_OFFSET))
        surface.blit(title, title_rect)

        icon_center = (self.rect.centerx, self.rect.centery - 6)
        if self.state == WEATHER_RAINY:
            icon = self.bold_font.render("////", True, RAIN_COLOR)
            label = self.font.render("RAIN", True, self.knob_color)
            surface.blit(icon, icon.get_rect(center=icon_center))
        elif self.state == WEATHER_SUNNY:
            self._draw_sun_icon(surface, icon_center)
            label = self.font.render("SUN", True, self.knob_color)
        else:
            self._draw_cloud_icon(surface, icon_center)
            label = self.font.render("CLOUD", True, self.knob_color)

        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.bottom - 14))
        surface.blit(label, label_rect)

    def _draw_sun_icon(self, surface: pygame.Surface, center: tuple[int, int]) -> None:
        """Draw a sun icon for sunny weather.

        Args:
            surface: Pygame surface to draw on.
            center: Center position for the sun icon.
        """
        radius = min(self.rect.width, self.rect.height) // 6
        for i in range(SUN_RAY_COUNT):
            angle = math.radians((360 / SUN_RAY_COUNT) * i)
            start = (
                center[0] + int((radius + 2) * math.cos(angle)),
                center[1] + int((radius + 2) * math.sin(angle)),
            )
            end = (
                center[0] + int((radius + SUN_RAY_LENGTH) * math.cos(angle)),
                center[1] + int((radius + SUN_RAY_LENGTH) * math.sin(angle)),
            )
            pygame.draw.line(surface, SUN_COLOR, start, end, SUN_RAY_WIDTH)
        pygame.draw.circle(surface, SUN_COLOR, center, radius + 1)
        pygame.draw.circle(surface, SUN_CORE_COLOR, center, radius - 2)

    def _draw_cloud_icon(self, surface: pygame.Surface, center: tuple[int, int]) -> None:
        """Draw a cloud icon for cloudy weather.

        Args:
            surface: Pygame surface to draw on.
            center: Center position for the cloud icon.
        """
        base_rect = pygame.Rect(0, 0, CLOUD_BASE_WIDTH, CLOUD_BASE_HEIGHT)
        base_rect.center = (center[0], center[1] + CLOUD_OFFSET_Y)
        pygame.draw.ellipse(surface, CLOUD_COLOR, base_rect)
        pygame.draw.circle(
            surface,
            CLOUD_COLOR,
            (center[0] - CLOUD_OFFSET_X, center[1]),
            CLOUD_SMALL_RADIUS,
        )
        pygame.draw.circle(
            surface,
            CLOUD_COLOR,
            (center[0], center[1] - CLOUD_OFFSET_Y),
            CLOUD_RADIUS,
        )
        pygame.draw.circle(
            surface,
            CLOUD_COLOR,
            (center[0] + CLOUD_OFFSET_X, center[1]),
            CLOUD_SMALL_RADIUS,
        )
