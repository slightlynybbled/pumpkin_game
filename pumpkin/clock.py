"""Clock tile placeholder rendering."""

import pygame

FONT_SIZE = 24
BORDER_COLOR = (120, 126, 140)
FACE_COLOR = (230, 233, 240)
FACE_RADIUS_SCALE = 3
FACE_BORDER_WIDTH = 2
HAND_WIDTH = 2
TITLE_Y_OFFSET = 14
HAND_TOP_MARGIN = 4
HAND_RIGHT_MARGIN = 6


class ClockTile:
    """Render a placeholder clock tile."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int]):
        """Initialize the tile.

        Args:
            rect: Tile rectangle (pygame.Rect or rect-like tuple).
        """
        self.rect = pygame.Rect(rect)
        self.border_color = BORDER_COLOR
        self.face_color = FACE_COLOR
        self.font = pygame.font.Font(None, FONT_SIZE)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the clock tile.

        Args:
            surface: Pygame surface to draw on.
        """
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        center = self.rect.center
        radius = min(self.rect.width, self.rect.height) // FACE_RADIUS_SCALE
        if radius > 0:
            pygame.draw.circle(surface, self.face_color, center, radius, FACE_BORDER_WIDTH)
            pygame.draw.line(
                surface,
                self.face_color,
                center,
                (center[0], center[1] - radius + HAND_TOP_MARGIN),
                HAND_WIDTH,
            )
            pygame.draw.line(
                surface,
                self.face_color,
                center,
                (center[0] + radius - HAND_RIGHT_MARGIN, center[1]),
                HAND_WIDTH,
            )
        title = self.font.render("CLOCK", True, self.face_color)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + TITLE_Y_OFFSET))
        surface.blit(title, title_rect)
