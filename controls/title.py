import pygame

class Title(pygame.sprite.DirtySprite):
    def __init__(self, x, y, width, height, text, click):
        super().__init__()          

        self.FONT = pygame.font.SysFont('arial', 22)
      
        self.text = text
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.image_center = self.image.get_rect().center
        text_surf = self.FONT.render(text, True, pygame.Color('white'))
        text_rect = text_surf.get_rect(center=self.image_center)
        # Blit the text onto the images.

        self.image.blit(text_surf, text_rect)

        # This function will be called when the button gets pressed.
        self.button_click = click
        self.button_down = False
        self.is_hovered = False
 
    def update(self, event) -> None:
        pass

    def update_text(self, text: str):
        self.image.fill(pygame.Color('black'))
        self.text = text
        text_sur = self.FONT.render(self.text, True, pygame.Color('white'))
        text_rec =  text_sur.get_rect(center=self.image_center)
        self.image.blit(text_sur, text_rec)
        self.dirty = 1