import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Класс, представлюящий одну звезду."""

    def __init__(self, rl_game):
        super().__init__()
        self.screen = rl_game.screen
        self.settings = rl_game.settings

        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    
    def update(self):
        """Перемещает звёзды вниз по OY."""
        self.y += self.settings.star_speed
        self.rect.y = self.y
    

    def check_edges(self):
        """"Определяет достигли ли звёзды края по OY."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom > screen_rect.bottom or self.rect.top < screen_rect.top:
            return True
