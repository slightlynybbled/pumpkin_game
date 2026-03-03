"""Shared UI helpers for common widget layout behavior."""

from typing import Tuple

import pygame


def button_rects(
    rect: pygame.Rect, button_size: int, padding: int
) -> Tuple[pygame.Rect, pygame.Rect]:
    """Return rectangles for the minus and plus buttons.

    Args:
        rect: Container rectangle.
        button_size: Square size of each button.
        padding: Inner padding from the container edges.
    """
    minus_rect = pygame.Rect(0, 0, button_size, button_size)
    plus_rect = pygame.Rect(0, 0, button_size, button_size)
    minus_rect.topleft = (
        rect.left + padding,
        rect.bottom - padding - button_size,
    )
    plus_rect.topright = (
        rect.right - padding,
        rect.bottom - padding - button_size,
    )
    return minus_rect, plus_rect


def double_click_step(
    now_ms: int, last_ms: int, double_click_ms: int, base_step: int = 1, double_step: int = 10
) -> int:
    """Return the step size based on a double-click threshold."""
    return double_step if now_ms - last_ms <= double_click_ms else base_step
