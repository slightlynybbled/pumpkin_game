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
        panel_y = board_origin[1] + self.board_size + self.padding_between
        panel_x = board_origin[0]
        panel_width = self.board_size // 3
        self.scoreboard = Scoreboard((panel_x, panel_y, panel_width, self.panel_height))
        self.mammoth = Mammoth((panel_x + panel_width, panel_y, panel_width, self.panel_height))
        self.squirt_button = SquirtButton(
            (panel_x + panel_width * 2, panel_y, panel_width, self.panel_height)
        )
        board_bottom_center = (
            board_origin[0] + self.board_size // 2,
            board_origin[1] + self.board_size,
        )
        self.mammoth.set_pivot(board_bottom_center)
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

    def update(self):
        pass

    def render(self):
        self.screen.fill((20, 22, 30))
        self.board.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.mammoth.draw(self.screen)
        self.squirt_button.draw(self.screen)
        for tile in self.side_tiles:
            tile.draw(self.screen)
        pygame.display.flip()

    def shutdown(self):
        pygame.quit()

    def run(self):
        try:
            while self.running:
                for event in pygame.event.get():
                    self.handle_event(event)
                self.update()
                self.render()
                self.clock.tick(60)
        finally:
            self.shutdown()
