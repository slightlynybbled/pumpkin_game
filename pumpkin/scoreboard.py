import pygame

FONT_SIZE = 32
TEXT_COLOR = (235, 235, 235)
BORDER_COLOR = (120, 126, 140)


class Scoreboard:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.text_color = TEXT_COLOR
        self.border_color = BORDER_COLOR
        self.spawned = 0
        self.harvested = 0

    def set_counts(self, spawned, harvested):
        self.spawned = spawned
        self.harvested = harvested

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        line_height = self.font.get_linesize()
        top_y = self.rect.centery - line_height // 2
        spawned_text = self.font.render(f"SPAWNED {self.spawned}", True, self.text_color)
        harvested_text = self.font.render(
            f"HARVESTED {self.harvested}", True, self.text_color
        )
        spawned_rect = spawned_text.get_rect(center=(self.rect.centerx, top_y))
        harvested_rect = harvested_text.get_rect(
            center=(self.rect.centerx, top_y + line_height)
        )
        surface.blit(spawned_text, spawned_rect)
        surface.blit(harvested_text, harvested_rect)
