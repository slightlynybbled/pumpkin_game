import pygame


class Mammoth:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.color = (139, 94, 60)
        self.angle = 0
        self.min_angle = -90
        self.max_angle = 90
        self.button_size = max(26, self.rect.width // 4)
        self.button_padding = 10
        self.double_click_ms = 350
        self.last_click_time = {"plus": 0, "minus": 0}
        self.pivot = None

    def set_pivot(self, pivot):
        self.pivot = pivot

    def _button_rects(self):
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

    def _apply_angle_delta(self, delta):
        self.angle = max(self.min_angle, min(self.max_angle, self.angle + delta))

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
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

    def draw(self, surface):
        body_width = int(self.rect.width * 0.32)
        body_height = int(self.rect.height * 0.5)
        head_radius = int(body_width * 0.35)
        trunk_length = int(body_height * 0.3)
        trunk_thickness = 4

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

        pygame.draw.rect(surface, self.color, minus_rect, 2, border_radius=4)
        pygame.draw.rect(surface, self.color, plus_rect, 2, border_radius=4)
        font = pygame.font.Font(None, 24)
        minus_label = font.render("-", True, self.color)
        plus_label = font.render("+", True, self.color)
        surface.blit(minus_label, minus_label.get_rect(center=minus_rect.center))
        surface.blit(plus_label, plus_label.get_rect(center=plus_rect.center))
        angle_label = font.render(f"{self.angle}", True, self.color)
        angle_rect = angle_label.get_rect(
            center=(self.rect.centerx, minus_rect.centery)
        )
        surface.blit(angle_label, angle_rect)
