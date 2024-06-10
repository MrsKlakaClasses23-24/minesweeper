from typing import Callable
import pygame

class Button(pygame.sprite.DirtySprite):
    def __init__(self, 
                 x: int, 
                 y: int, 
                 width: int, 
                 height: int, 
                 text: str, 
                 click: Callable):
        super().__init__()          

        self.FONT = pygame.font.SysFont('arial', 22)
        self.image_normal = pygame.transform.scale(pygame.Surface((100, 40)), (width, height))
        self.image_normal.fill(pygame.Color('red'))
        self.image_hover = pygame.transform.scale(pygame.Surface((100, 40)), (width, height))
        self.image_hover.fill(pygame.Color('red3'))
        self.image_down = pygame.transform.scale(pygame.Surface((100, 40)), (width, height))
        self.image_down.fill(pygame.Color('red4'))
        self.text = text
        self.image = self.image_normal 
        self.rect = self.image.get_rect(topleft=(x, y))

        image_center = self.image.get_rect().center
        text_surf = self.FONT.render(text, True, pygame.Color('white'))
        text_rect = text_surf.get_rect(center=image_center)
        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        # This function will be called when the button gets pressed.
        self.button_click = click
        self.button_down = False
        self.is_hovered = False
 
    def update(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
                self.dirty = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.button_click()  # Call the function.
                self.image = self.image_hover
                self.dirty = 1
            self.button_down = False
        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
                self.is_hovered = True
                self.dirty = 1
            elif not collided and self.is_hovered:
                self.image = self.image_normal
                self.dirty = 1