import pygame


class Rocket():
    """Класс для управления ракетой."""

    def __init__(self, screen_game):
        self.screen = screen_game.screen
        self.screen_rect = screen_game.screen.get_rect()
        
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.settings = screen_game.settings
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    
    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)
    

    def update(self):
        """Обновляет позицию корабля с учётом флага."""
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        
        self.rect.x = self.x
        self.rect.y = self.y
    

    def center_rocket(self):
        """Размещает корабль в центр левой стороны."""
        self.rect.left = self.screen_rect.left
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
