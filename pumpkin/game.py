import math

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


class Game:
    def __init__(self):
        pygame.init()
        self.gravity = 9.8
        self.tile_size = 60
        self.board_size = self.tile_size * 8
        self.padding_top = 24
        self.padding_between = 16
        self.padding_left = 24
        self.padding_right = 24
        self.panel_height = 72
        self.padding_bottom = 24
        self.side_tile_width = int(self.tile_size * 1.5)
        self.side_tile_gap = 12
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
        panel_width = self.board_size // 3
        self.scoreboard = Scoreboard((panel_x, panel_y, panel_width, self.panel_height))
        self.mammoth = Mammoth((panel_x + panel_width, panel_y, panel_width, self.panel_height))
        self.squirt_button = SquirtButton(
            (panel_x + panel_width * 2, panel_y, panel_width, self.panel_height),
            on_click=self.fire_shot,
        )
        board_bottom_center = (
            board_origin[0] + self.board_size // 2,
            board_origin[1] + self.board_size,
        )
        self.mammoth.set_pivot(board_bottom_center)
        self.shots = []
        side_x = board_origin[0] + self.board_size + self.padding_between
        side_height = self.board_size
        tile_height = (side_height - self.side_tile_gap * 4) // 5
        self.angle_tile = AngleAdjustmentTile(
            (side_x, board_origin[1], self.side_tile_width, tile_height)
        )
        self.force_tile = ForceAdjustmentTile(
            (
                side_x,
                board_origin[1] + (tile_height + self.side_tile_gap),
                self.side_tile_width,
                tile_height,
            )
        )
        self.quantity_tile = QuantityAdjustmentTile(
            (
                side_x,
                board_origin[1] + 2 * (tile_height + self.side_tile_gap),
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
                    board_origin[1] + 3 * (tile_height + self.side_tile_gap),
                    self.side_tile_width,
                    tile_height,
                )
            ),
            ClockTile(
                (
                    side_x,
                    board_origin[1] + 4 * (tile_height + self.side_tile_gap),
                    self.side_tile_width,
                    tile_height,
                )
            ),
        ]

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        self.squirt_button.handle_event(event)
        self.angle_tile.handle_event(event)
        self.force_tile.handle_event(event)
        self.quantity_tile.handle_event(event)
        self.mammoth.handle_event(event)

    def update(self, dt):
        self.board.update(dt)
        self.scoreboard.set_counts(
            self.board.spawned_total, self.board.harvested_total
        )
        if not self.shots:
            return
        remaining = []
        for shot in self.shots:
            if shot["landed"]:
                shot["landed_time"] += dt
                if shot["landed_time"] < 1.0:
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

    def render(self):
        self.screen.fill((20, 22, 30))
        self.board.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.mammoth.draw(self.screen)
        self.squirt_button.draw(self.screen)
        self._draw_shots()
        for tile in self.side_tiles:
            tile.draw(self.screen)
        pygame.display.flip()

    def _draw_shots(self):
        if not self.shots:
            return
        color = (120, 180, 255)
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
            steps = 24
            for i in range(steps + 1):
                t = shot["flight_time"] * (i / steps)
                pos = self._shot_position(shot, t)
                if pos:
                    path_points.append((int(pos[0]), int(pos[1])))
            if len(path_points) >= 2:
                pygame.draw.lines(self.screen, color, False, path_points, 2)

            current_pos = self._shot_position(shot, shot["t"])
            if current_pos:
                pygame.draw.circle(
                    self.screen,
                    color,
                    (int(current_pos[0]), int(current_pos[1])),
                    shot["radius"],
                )

    def _draw_offboard_arrow(self, pos, direction):
        dx, dy = direction
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        perp = (-uy, ux)
        base = (pos[0] - ux * 6, pos[1] - uy * 6)
        tip = (pos[0] + ux * 10, pos[1] + uy * 10)
        left = (base[0] + perp[0] * 6, base[1] + perp[1] * 6)
        right = (base[0] - perp[0] * 6, base[1] - perp[1] * 6)
        pygame.draw.polygon(self.screen, (120, 180, 255), [tip, left, right])

    def _shot_position(self, shot, t):
        vx = shot["vx"]
        vy = shot["vy"]
        x = vx * t
        y = vy * t - 0.5 * self.gravity * t * t
        if y < 0:
            y = 0
        origin = shot["origin"]
        dir_x, dir_y = shot["direction"]
        perp_x, perp_y = -dir_y, dir_x
        arc_scale = -0.3 if shot["direction_angle"] < 0 else 0.3
        return (
            origin[0] + dir_x * x + perp_x * (-y * arc_scale),
            origin[1] + dir_y * x + perp_y * (-y * arc_scale),
        )

    def _offboard_marker(self, origin, direction):
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
        return (x + normal[0] * 8, y + normal[1] * 8)

    def fire_shot(self):
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
        flight_time = (2 * vy) / self.gravity if vy > 0 else 0
        range_distance = vx * flight_time
        azimuth = math.radians(direction_angle)
        dx = math.sin(azimuth)
        dy = -math.cos(azimuth)
        landing = (origin[0] + dx * range_distance, origin[1] + dy * range_distance)

        in_board = self.board_rect.collidepoint(landing)
        radius = 4 + (quantity - 1) * 2
        radius = min(radius, self.tile_size // 2 - 6)
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
                "flight_time": max(flight_time, 0.01),
                "vx": vx,
                "vy": vy,
                "radius": radius,
                "landing": (int(tile_center[0]), int(tile_center[1])),
                "tile": (row, col),
                "quantity": quantity,
                "water_applied": False,
                "in_board": True,
                "landed": False,
                "time_scale": 2.0,
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
                "flight_time": max(flight_time, 0.01),
                "vx": vx,
                "vy": vy,
                "radius": radius,
                "marker_pos": marker_pos,
                "quantity": quantity,
                "water_applied": False,
                "in_board": False,
                "landed": False,
                "time_scale": 2.0,
                "landed_time": 0.0,
            }
            )

    def shutdown(self):
        pygame.quit()

    def run(self):
        try:
            while self.running:
                dt = self.clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    self.handle_event(event)
                self.update(dt)
                self.render()
        finally:
            self.shutdown()
