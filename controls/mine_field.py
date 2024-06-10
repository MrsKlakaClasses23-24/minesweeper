from typing import Dict, List, Tuple
import pygame

from controls.grid_tile import GridTile
from mine_sweeper import MoveResult


class Minefield():
    FIELD_PADDING = 20
    def __init__(self, 
                 screen_height: int, 
                 screen_width: int, 
                 cell_height: int = 8, 
                 cell_width: int = 8,
                 callback = None) -> None:
        self.font = pygame.font.SysFont("arial", 22)
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.cell_grid:List[List[GridTile]] = []
        self.cell_sprites = pygame.sprite.LayeredDirty()
        self.callback = callback
        cell_size = min(self.screen_width//self.cell_width,
                        self.screen_height//self.cell_height)
        
        flag = pygame.image.load("assets/images/flag.png")
        flag = pygame.transform.scale(flag, (cell_size, cell_size))
        mine = pygame.image.load("assets/images/mine.png")
        mine = pygame.transform.scale(mine, (cell_size, cell_size))

        for i in range(self.cell_height):
            self.cell_grid.append([])
            for j in range(self.cell_width):
                tile = GridTile(i, j, cell_size, self.font, flag, mine, self.click_handler)
                self.cell_grid[i].append(tile)
                self.cell_sprites.add(tile)
       
      

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.cell_sprites.update(event)

    def click_handler(self, x, y):
        action_status:MoveResult = self.callback(x,y)
        if action_status is not None:
            self.update_cells(action_status.updates)

    def update_cells(self, updates:Dict[Tuple[int,int], str]):
        for key, value in updates.items():
            self.cell_grid[key[0]][key[1]].update_text(value)
