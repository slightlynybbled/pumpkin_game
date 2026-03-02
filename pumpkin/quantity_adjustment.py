import pygame


class QuantityAdjustmentTile:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.border_color = (120, 126, 140)
        self.line_color = (230, 233, 240)
        self.water_color = (120, 180, 255)
        self.font = pygame.font.Font(None, 24)
        self.quantity = 5
        self.min_quantity = 1
        self.max_quantity = 10
        self.button_size = max(26, self.rect.width // 4)
        self.button_padding = 10

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

    def _apply_quantity_delta(self, delta):
        self.quantity = max(
            self.min_quantity, min(self.max_quantity, self.quantity + delta)
        )

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        minus_rect, plus_rect = self._button_rects()
        if plus_rect.collidepoint(event.pos):
            self._apply_quantity_delta(1)
        elif minus_rect.collidepoint(event.pos):
            self._apply_quantity_delta(-1)

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        minus_rect, plus_rect = self._button_rects()
        pygame.draw.rect(surface, self.line_color, minus_rect, 2, border_radius=4)
        pygame.draw.rect(surface, self.line_color, plus_rect, 2, border_radius=4)
        minus_label = self.font.render("-", True, self.line_color)
        plus_label = self.font.render("+", True, self.line_color)
        surface.blit(minus_label, minus_label.get_rect(center=minus_rect.center))
        surface.blit(plus_label, plus_label.get_rect(center=plus_rect.center))

        bucket_width = int(self.rect.width * 0.55)
        bucket_height = int(self.rect.height * 0.45)
        bucket_left = self.rect.centerx - bucket_width // 2
        bucket_bottom = minus_rect.top - 12
        bucket_top = bucket_bottom - bucket_height
        bucket_rect = pygame.Rect(bucket_left, bucket_top, bucket_width, bucket_height)

        fill_ratio = (self.quantity - self.min_quantity) / (
            self.max_quantity - self.min_quantity
        )
        fill_height = max(4, int(bucket_rect.height * fill_ratio))
        fill_rect = pygame.Rect(
            bucket_rect.left + 3,
            bucket_rect.bottom - fill_height,
            bucket_rect.width - 6,
            fill_height,
        )
        pygame.draw.rect(surface, self.water_color, fill_rect)
        pygame.draw.rect(surface, self.line_color, bucket_rect, 2)

        qty_label = self.font.render(str(self.quantity), True, self.line_color)
        qty_rect = qty_label.get_rect(center=bucket_rect.center)
        surface.blit(qty_label, qty_rect)
