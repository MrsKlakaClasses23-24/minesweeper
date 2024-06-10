from typing import Any, Callable
import pygame

from mine_sweeper import Minesweeper

class GridTile(pygame.sprite.DirtySprite):

    def __init__(self, 
                 row: int,
                 col: int,
                 cell_size: int,
                 font: pygame.font.FontType,
                 flag,
                 mine,
                 on_click: Callable[[int, int], None]):
        super().__init__()       
        
        # size information about the cell
        self.row = row
        self.col = col   
        self.cell_size = cell_size
        self.on_click = on_click
        self.font = font
        self.flag = flag
        self.mine: pygame.Surface = mine
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
 
        self.image.fill(pygame.Color('red'), pygame.Rect(1, 1, cell_size - 2, cell_size - 2))
 
        self.text = None
        self.rect.x = col * cell_size
        self.rect.y = row * cell_size
        self.image_center = self.rect.center

        self.button_down = False     

    def update_text(self, text: str):
        if text == Minesweeper.MINE:
            text_rec =  self.mine.get_rect(center=(self.rect.width/2, self.rect.width/2))
            self.image.blit(self.mine, text_rec)
        elif text == Minesweeper.FLAG:
            text_rec =  self.flag.get_rect(center=(self.rect.width/2, self.rect.width/2))
            self.image.blit(self.flag, text_rec)         
        else:
            self.text = text if text != "0" else ""
            self.image.fill(pygame.Color('white'), pygame.Rect(1, 1, self.cell_size - 2, self.cell_size - 2))
            text_sur = self.font.render(self.text, True, pygame.Color('black'))
            text_rec =  text_sur.get_rect(center=(self.rect.width/2, self.rect.width/2))
            self.image.blit(text_sur, text_rec)
        self.dirty = 1

    def update(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.on_click(self.row, self.col)  # Call the function.
            self.button_down = False