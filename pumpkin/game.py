"""Main game loop, layout, and shot simulation."""

import math
from typing import Any

import pygame

from pumpkin.angle_adjustment import AngleAdjustmentTile
from pumpkin.board import Board
from pumpkin.clock import ClockTile
from pumpkin.force_adjustment import ForceAdjustmentTile
from pumpkin.mammoth import Mammoth
from pumpkin.quantity_adjustment import QuantityAdjustmentTile
from pumpkin.scoreboard import Scoreboard
from pumpkin.squirt import SquirtButton
from pumpkin.weather_adjustment import WeatherAdjustmentTile

GRAVITY = 9.8
GRAVITY_HALF = 0.5
FLIGHT_TIME_MULTIPLIER = 2.0
MIN_FLIGHT_TIME = 0.01
BOARD_TILES = 8
TILE_SIZE = 60
PADDING_TOP = 24
PADDING_BETWEEN = 16
PADDING_LEFT = 24
PADDING_RIGHT = 24
PANEL_HEIGHT = 72
PADDING_BOTTOM = 24
SIDE_TILE_WIDTH_SCALE = 1.5
SIDE_TILE_GAP = 12
SIDE_TILE_COUNT = 5
PANEL_COLUMNS = 3
PANEL_INDEX_SCOREBOARD = 0
PANEL_INDEX_MAMMOTH = 1
PANEL_INDEX_SQUIRT = 2
SIDE_TILE_INDEX_ANGLE = 0
SIDE_TILE_INDEX_FORCE = 1
SIDE_TILE_INDEX_QUANTITY = 2
SIDE_TILE_INDEX_WEATHER = 3
SIDE_TILE_INDEX_CLOCK = 4
BACKGROUND_COLOR = (20, 22, 30)
ARC_COLOR = (120, 180, 255)
ARC_STEPS = 24
ARC_LINE_WIDTH = 2
ARC_SCALE_POS = 0.3
ARC_SCALE_NEG = -0.3
ARROW_BASE_OFFSET = 6
ARROW_TIP_OFFSET = 10
ARROW_SIDE_OFFSET = 6
ARROW_OUTSET = 8
SHOT_RADIUS_BASE = 4
SHOT_RADIUS_STEP = 2
SHOT_RADIUS_MARGIN = 6
SHOT_TIME_SCALE = 2.0
SHOT_PERSIST_SECONDS = 1.0
FPS = 60
MS_PER_SEC = 1000.0
KEY_STEP = 1
HOLD_DELAY_SECONDS = 1.0
HOLD_REPEAT_INTERVAL = 0.08


class Game:
    """Manage the game loop, layout, and interactions."""

    def __init__(self):
        """Initialize the game state, UI, and board."""
        pygame.init()
        self.gravity = GRAVITY
        self.tile_size = TILE_SIZE
        self.board_size = self.tile_size * BOARD_TILES
        self.padding_top = PADDING_TOP
        self.padding_between = PADDING_BETWEEN
        self.padding_left = PADDING_LEFT
        self.padding_right = PADDING_RIGHT
        self.panel_height = PANEL_HEIGHT
        self.padding_bottom = PADDING_BOTTOM
        self.side_tile_width = int(self.tile_size * SIDE_TILE_WIDTH_SCALE)
        self.side_tile_gap = SIDE_TILE_GAP
        self.screen_width = (
            self.padding_left
            + self.board_size
            + self.padding_between
            + self.side_tile_width
            + self.padding_right
        )
        self.screen_height = (
            self.padding_top
            + self.board_size
            + self.padding_between
            + self.panel_height
            + self.padding_bottom
        )
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pumpkin")
        self.clock = pygame.time.Clock()
        self.running = True

        board_origin = (self.padding_left, self.padding_top)
        self.board = Board(tile_size=self.tile_size, origin=board_origin)
        self.board_rect = pygame.Rect(board_origin, (self.board_size, self.board_size))
        panel_y = board_origin[1] + self.board_size + self.padding_between
        panel_x = board_origin[0]
        panel_width = self.board_size // PANEL_COLUMNS
        self.scoreboard = Scoreboard(
            (panel_x + panel_width * PANEL_INDEX_SCOREBOARD, panel_y, panel_width, self.panel_height)
        )
        self.mammoth = Mammoth(
            (panel_x + panel_width * PANEL_INDEX_MAMMOTH, panel_y, panel_width, self.panel_height)
        )
        self.squirt_button = SquirtButton(
            (panel_x + panel_width * PANEL_INDEX_SQUIRT, panel_y, panel_width, self.panel_height),
            on_click=self.fire_shot,
        )
        board_bottom_center = (
            board_origin[0] + self.board_size // 2,
            board_origin[1] + self.board_size,
        )
        self.mammoth.set_pivot(board_bottom_center)
        self.shots: list[dict[str, Any]] = []
        self.left_pressed = False
        self.right_pressed = False
        self.left_hold_time = 0.0
        self.right_hold_time = 0.0
        self.left_repeat_time = 0.0
        self.right_repeat_time = 0.0
        side_x = board_origin[0] + self.board_size + self.padding_between
        side_height = self.board_size
        tile_height = (side_height - self.side_tile_gap * (SIDE_TILE_COUNT - 1)) // SIDE_TILE_COUNT
        self.angle_tile = AngleAdjustmentTile(
            (
                side_x,
                board_origin[1] + SIDE_TILE_INDEX_ANGLE * (tile_height + self.side_tile_gap),
                self.side_tile_width,
                tile_height,
            )
        )
        self.force_tile = ForceAdjustmentTile(
            (
                side_x,
                board_origin[1] + SIDE_TILE_INDEX_FORCE * (tile_height + self.side_tile_gap),
                self.side_tile_width,
                tile_height,
            )
        )
        self.quantity_tile = QuantityAdjustmentTile(
            (
                side_x,
                board_origin[1] + SIDE_TILE_INDEX_QUANTITY * (tile_height + self.side_tile_gap),
                self.side_tile_width,
                tile_height,
            )
        )
        self.side_tiles = [
            self.angle_tile,
            self.force_tile,
            self.quantity_tile,
            WeatherAdjustmentTile(
                (
                    side_x,
                    board_origin[1] + SIDE_TILE_INDEX_WEATHER * (tile_height + self.side_tile_gap),
                    self.side_tile_width,
                    tile_height,
                )
            ),
            ClockTile(
                (
                    side_x,
                    board_origin[1] + SIDE_TILE_INDEX_CLOCK * (tile_height + self.side_tile_gap),
                    self.side_tile_width,
                    tile_height,
                )
            ),
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.fire_shot()
            elif event.key == pygame.K_UP:
                if event.mod & pygame.KMOD_CTRL:
                    self.angle_tile.adjust_angle(KEY_STEP)
                else:
                    self.force_tile.adjust_force(KEY_STEP)
            elif event.key == pygame.K_DOWN:
                if event.mod & pygame.KMOD_CTRL:
                    self.angle_tile.adjust_angle(-KEY_STEP)
                else:
                    self.force_tile.adjust_force(-KEY_STEP)
            elif event.key == pygame.K_LEFT:
                self.mammoth.adjust_angle(-KEY_STEP)
            elif event.key == pygame.K_RIGHT:
                self.mammoth.adjust_angle(KEY_STEP)
        self.squirt_button.handle_event(event)
        self.angle_tile.handle_event(event)
        self.force_tile.handle_event(event)
        self.quantity_tile.handle_event(event)
        self.mammoth.handle_event(event)

    def update(self, dt: float) -> None:
        """Advance game simulation.

        Args:
            dt: Delta time in seconds.
        """
        self.board.update(dt)
        self.scoreboard.set_counts(
            self.board.spawned_total, self.board.harvested_total
        )
        self._update_direction_keys(dt)
        if not self.shots:
            return
        remaining = []
        for shot in self.shots:
            if shot["landed"]:
                shot["landed_time"] += dt
                if shot["landed_time"] < SHOT_PERSIST_SECONDS:
                    remaining.append(shot)
                continue
            shot["t"] += dt * shot["time_scale"]
            if shot["t"] >= shot["flight_time"]:
                shot["t"] = shot["flight_time"]
                shot["landed"] = True
                if shot["in_board"] and not shot["water_applied"]:
                    row, col = shot["tile"]
                    self.board.add_water(row, col, shot["quantity"])
                    shot["water_applied"] = True
                remaining.append(shot)
            else:
                remaining.append(shot)
        self.shots = remaining

    def _update_direction_keys(self, dt: float) -> None:
        """Handle held left/right key repeats after a delay.

        Args:
            dt: Delta time in seconds.
        """
        keys = pygame.key.get_pressed()
        left_down = bool(keys[pygame.K_LEFT])
        right_down = bool(keys[pygame.K_RIGHT])

        if left_down:
            if not self.left_pressed:
                self.left_pressed = True
                self.left_hold_time = 0.0
                self.left_repeat_time = 0.0
            else:
                self.left_hold_time += dt
                if self.left_hold_time >= HOLD_DELAY_SECONDS:
                    self.left_repeat_time += dt
                    while self.left_repeat_time >= HOLD_REPEAT_INTERVAL:
                        self.mammoth.adjust_angle(-KEY_STEP)
                        self.left_repeat_time -= HOLD_REPEAT_INTERVAL
        else:
            self.left_pressed = False
            self.left_hold_time = 0.0
            self.left_repeat_time = 0.0

        if right_down:
            if not self.right_pressed:
                self.right_pressed = True
                self.right_hold_time = 0.0
                self.right_repeat_time = 0.0
            else:
                self.right_hold_time += dt
                if self.right_hold_time >= HOLD_DELAY_SECONDS:
                    self.right_repeat_time += dt
                    while self.right_repeat_time >= HOLD_REPEAT_INTERVAL:
                        self.mammoth.adjust_angle(KEY_STEP)
                        self.right_repeat_time -= HOLD_REPEAT_INTERVAL
        else:
            self.right_pressed = False
            self.right_hold_time = 0.0
            self.right_repeat_time = 0.0

    def render(self) -> None:
        """Render the current frame."""
        self.screen.fill(BACKGROUND_COLOR)
        self.board.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.mammoth.draw(self.screen)
        self.squirt_button.draw(self.screen)
        self._draw_shots()
        for tile in self.side_tiles:
            tile.draw(self.screen)
        pygame.display.flip()

    def _draw_shots(self) -> None:
        """Render all active shots and their paths."""
        if not self.shots:
            return
        color = ARC_COLOR
        for shot in self.shots:
            if shot["landed"]:
                if shot["in_board"]:
                    pos = shot["landing"]
                    pygame.draw.circle(self.screen, color, pos, shot["radius"])
                else:
                    marker_pos = shot["marker_pos"]
                    self._draw_offboard_arrow(marker_pos, shot["direction"])
                continue

            path_points = []
            steps = ARC_STEPS
            for i in range(steps + 1):
                t = shot["flight_time"] * (i / steps)
                pos = self._shot_position(shot, t)
                if pos:
                    path_points.append((int(pos[0]), int(pos[1])))
            if len(path_points) >= 2:
                pygame.draw.lines(self.screen, color, False, path_points, ARC_LINE_WIDTH)

            current_pos = self._shot_position(shot, shot["t"])
            if current_pos:
                pygame.draw.circle(
                    self.screen,
                    color,
                    (int(current_pos[0]), int(current_pos[1])),
                    shot["radius"],
                )

    def _draw_offboard_arrow(
        self, pos: tuple[float, float], direction: tuple[float, float]
    ) -> None:
        """Draw an off-board directional arrow marker.

        Args:
            pos: Arrow center position as (x, y).
            direction: Direction vector as (dx, dy).
        """
        dx, dy = direction
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        perp = (-uy, ux)
        base = (pos[0] - ux * ARROW_BASE_OFFSET, pos[1] - uy * ARROW_BASE_OFFSET)
        tip = (pos[0] + ux * ARROW_TIP_OFFSET, pos[1] + uy * ARROW_TIP_OFFSET)
        left = (base[0] + perp[0] * ARROW_SIDE_OFFSET, base[1] + perp[1] * ARROW_SIDE_OFFSET)
        right = (base[0] - perp[0] * ARROW_SIDE_OFFSET, base[1] - perp[1] * ARROW_SIDE_OFFSET)
        pygame.draw.polygon(self.screen, ARC_COLOR, [tip, left, right])

    def _shot_position(self, shot: dict[str, Any], t: float) -> tuple[float, float]:
        """Compute shot position at time t.

        Args:
            shot: Shot state dictionary.
            t: Time in seconds since launch.
        """
        vx = shot["vx"]
        vy = shot["vy"]
        x = vx * t
        y = vy * t - GRAVITY_HALF * self.gravity * t * t
        if y < 0:
            y = 0
        origin = shot["origin"]
        dir_x, dir_y = shot["direction"]
        perp_x, perp_y = -dir_y, dir_x
        arc_scale = ARC_SCALE_NEG if shot["direction_angle"] < 0 else ARC_SCALE_POS
        return (
            origin[0] + dir_x * x + perp_x * (-y * arc_scale),
            origin[1] + dir_y * x + perp_y * (-y * arc_scale),
        )

    def _offboard_marker(
        self, origin: tuple[float, float], direction: tuple[float, float]
    ) -> tuple[float, float]:
        """Compute a marker position just outside the board.

        Args:
            origin: Launch origin as (x, y).
            direction: Direction vector as (dx, dy).
        """
        ox, oy = origin
        dx, dy = direction
        candidates = []
        if dx != 0:
            for edge_x in (self.board_rect.left, self.board_rect.right):
                t = (edge_x - ox) / dx
                if t >= 0:
                    y = oy + t * dy
                    if self.board_rect.top <= y <= self.board_rect.bottom:
                        normal = (-1, 0) if edge_x == self.board_rect.left else (1, 0)
                        candidates.append((t, edge_x, y, normal))
        if dy != 0:
            for edge_y in (self.board_rect.top, self.board_rect.bottom):
                t = (edge_y - oy) / dy
                if t >= 0:
                    x = ox + t * dx
                    if self.board_rect.left <= x <= self.board_rect.right:
                        normal = (0, -1) if edge_y == self.board_rect.top else (0, 1)
                        candidates.append((t, x, edge_y, normal))
        if not candidates:
            return origin
        t, x, y, normal = min(candidates, key=lambda item: item[0])
        return (x + normal[0] * ARROW_OUTSET, y + normal[1] * ARROW_OUTSET)

    def fire_shot(self) -> None:
        """Launch a new shot using current tile settings."""
        force = self.force_tile.force
        vertical_angle = self.angle_tile.angle
        direction_angle = self.mammoth.angle
        quantity = self.quantity_tile.quantity
        origin = (
            self.board_rect.left + self.board_size // 2,
            self.board_rect.top + self.board_size,
        )

        if force <= 0:
            return

        theta = math.radians(vertical_angle)
        scale = math.sqrt(self.board_size * self.gravity) / self.force_tile.max_force
        velocity = force * scale
        vx = velocity * math.cos(theta)
        vy = velocity * math.sin(theta)
        flight_time = (FLIGHT_TIME_MULTIPLIER * vy) / self.gravity if vy > 0 else 0
        range_distance = vx * flight_time
        azimuth = math.radians(direction_angle)
        dx = math.sin(azimuth)
        dy = -math.cos(azimuth)
        landing = (origin[0] + dx * range_distance, origin[1] + dy * range_distance)

        in_board = self.board_rect.collidepoint(landing)
        radius = SHOT_RADIUS_BASE + (quantity - 1) * SHOT_RADIUS_STEP
        radius = min(radius, self.tile_size // 2 - SHOT_RADIUS_MARGIN)
        if in_board:
            col = int((landing[0] - self.board_rect.left) // self.tile_size)
            row = int((landing[1] - self.board_rect.top) // self.tile_size)
            tile_center = (
                self.board_rect.left + col * self.tile_size + self.tile_size // 2,
                self.board_rect.top + row * self.tile_size + self.tile_size // 2,
            )
            self.shots.append(
                {
                    "origin": origin,
                    "direction": (dx, dy),
                    "direction_angle": direction_angle,
                    "t": 0.0,
                    "flight_time": max(flight_time, MIN_FLIGHT_TIME),
                    "vx": vx,
                    "vy": vy,
                    "radius": radius,
                    "landing": (int(tile_center[0]), int(tile_center[1])),
                    "tile": (row, col),
                    "quantity": quantity,
                    "water_applied": False,
                    "in_board": True,
                    "landed": False,
                    "time_scale": SHOT_TIME_SCALE,
                    "landed_time": 0.0,
                }
            )
        else:
            marker_pos = self._offboard_marker(origin, (dx, dy))
            self.shots.append(
                {
                    "origin": origin,
                    "direction": (dx, dy),
                    "direction_angle": direction_angle,
                    "t": 0.0,
                    "flight_time": max(flight_time, MIN_FLIGHT_TIME),
                    "vx": vx,
                    "vy": vy,
                    "radius": radius,
                    "marker_pos": marker_pos,
                    "quantity": quantity,
                    "water_applied": False,
                    "in_board": False,
                    "landed": False,
                    "time_scale": SHOT_TIME_SCALE,
                    "landed_time": 0.0,
                }
            )

    def shutdown(self) -> None:
        """Shutdown pygame cleanly."""
        pygame.quit()

    def run(self) -> None:
        """Run the main game loop."""
        try:
            while self.running:
                dt = self.clock.tick(FPS) / MS_PER_SEC
                for event in pygame.event.get():
                    self.handle_event(event)
                self.update(dt)
                self.render()
        finally:
            self.shutdown()
