"""Clock tile placeholder rendering."""

import pygame

FONT_SIZE = 24
BORDER_COLOR = (120, 126, 140)
TITLE_Y_OFFSET = 14
START_BUTTON_HEIGHT = 22
START_BUTTON_WIDTH_RATIO = 0.8
START_BUTTON_RADIUS = 4
START_BUTTON_COLOR = (78, 148, 255)
START_BUTTON_TEXT = "START"
RESTART_BUTTON_TEXT = "RESTART"
TIME_TEXT_COLOR = (235, 235, 235)
SCORE_TEXT_COLOR = (235, 235, 235)
MOUSE_LEFT_BUTTON = 1


class ClockTile:
    """Render a placeholder clock tile."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int]):
        """Initialize the tile.

        Args:
            rect: Tile rectangle (pygame.Rect or rect-like tuple).
        """
        self.rect = pygame.Rect(rect)
        self.border_color = BORDER_COLOR
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.running = False
        self.remaining_seconds = 0.0
        self.score_text = ""
        self.game_over = False

    def set_state(self, running: bool, remaining_seconds: float, score_text: str, game_over: bool) -> None:
        """Update clock state and display values.

        Args:
            running: Whether the timer is running.
            remaining_seconds: Seconds remaining in the countdown.
            score_text: Score display when game is over.
            game_over: Whether the countdown has finished.
        """
        self.running = running
        self.remaining_seconds = max(0.0, remaining_seconds)
        self.score_text = score_text
        self.game_over = game_over

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse click events.

        Args:
            event: Pygame event to process.

        Returns:
            True if the start button was clicked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT_BUTTON:
            return self._action_button_rect().collidepoint(event.pos)
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the clock tile.

        Args:
            surface: Pygame surface to draw on.
        """
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        title = self.font.render("CLOCK", True, TIME_TEXT_COLOR)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + TITLE_Y_OFFSET))
        surface.blit(title, title_rect)

        if self.game_over:
            score = self.font.render(self.score_text, True, SCORE_TEXT_COLOR)
            score_rect = score.get_rect(center=self.rect.center)
            surface.blit(score, score_rect)
            button_rect = self._action_button_rect()
            pygame.draw.rect(
                surface, START_BUTTON_COLOR, button_rect, border_radius=START_BUTTON_RADIUS
            )
            label = self.font.render(RESTART_BUTTON_TEXT, True, TIME_TEXT_COLOR)
            surface.blit(label, label.get_rect(center=button_rect.center))
            return

        minutes = int(self.remaining_seconds) // 60
        seconds = int(self.remaining_seconds) % 60
        time_text = f"{minutes}:{seconds:02d}"
        time_surface = self.font.render(time_text, True, TIME_TEXT_COLOR)
        time_rect = time_surface.get_rect(center=self.rect.center)
        surface.blit(time_surface, time_rect)

        if not self.running and not self.game_over:
            button_rect = self._action_button_rect()
            pygame.draw.rect(
                surface, START_BUTTON_COLOR, button_rect, border_radius=START_BUTTON_RADIUS
            )
            label = self.font.render(START_BUTTON_TEXT, True, TIME_TEXT_COLOR)
            surface.blit(label, label.get_rect(center=button_rect.center))

    def _action_button_rect(self) -> pygame.Rect:
        """Compute the start/restart button rectangle."""
        width = int(self.rect.width * START_BUTTON_WIDTH_RATIO)
        left = self.rect.centerx - width // 2
        top = self.rect.bottom - START_BUTTON_HEIGHT - 6
        return pygame.Rect(left, top, width, START_BUTTON_HEIGHT)
