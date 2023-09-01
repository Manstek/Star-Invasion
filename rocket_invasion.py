import sys
from time import sleep
import pygame

from game_stats import Gamestats
from settings import Settings
from rocket import Rocket
from bullet import Bullet
from star import Star



class RocketInvasion:
    """Класс для управления кораблём."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Rocket launcher')

        self.stats = Gamestats(self)
        
        self.ship = Rocket(self)

        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_sky()


    
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_stars()

            self._update_screen()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу Bullet."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.x > self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_star_collisions()
    

    def _check_bullet_star_collisions(self):
        """Обработка коллизий снарядов c пришельцами."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.stars, True, True)
        if not self.stars:
            self.bullets.empty()
            self._create_sky()      


    def _create_sky(self):
        """Создание звёздного неба."""
        star = Star(self)
        star_width, star_height = star.rect.size
        ship_height = self.ship.rect.height
        ship_weight = self.ship.rect.width

        available_space_x = self.settings.screen_width - (2 * ship_weight)
        number_star_x = available_space_x // (star_width * 2)

        available_space_y = self.settings.screen_height

        number_rows = available_space_y // (2 * star_height)

        for row_number in range(number_rows):
            for star_number in range(number_star_x):
                self._create_star(row_number, star_number)
    

    def _create_star(self, row_number, alien_number):
        """Создание звезды и размещение её в ряду."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = 10 * star_width + 2 * star_width * alien_number
        star.rect.x = star.x
        star.y = 2 * star_height * row_number
        star.rect.y = star.y

        self.stars.add(star)
    

    def _update_stars(self):
        self._check_fleet_edges()
        self.stars.update()

        if pygame.sprite.spritecollideany(self.ship, self.stars):
            self._ship_hit()
        
        self._check_star_bottom()
    

    def _check_fleet_edges(self):
        """Проверка достижения края экрана."""
        for star in self.stars.sprites():
            if star.check_edges():
                self._change_fleet_direction()
                break
    

    def _change_fleet_direction(self):
        """Спуск влево и смена направления движения."""
        for star in self.stars.sprites():
            star.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _check_star_bottom(self):
        """Проверяет, добрались ли звёзды до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for star in self.stars.sprites():
            if star.rect.left <= screen_rect.left:
                self._ship_hit()
                break
    

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.stars.empty()
            self.bullets.empty()

            self._create_sky()
            self.ship.center_rocket()
            sleep(1)
        else:
            self.stats.game_active = False


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.stars.draw(self.screen)
        
        pygame.display.flip()
    


if __name__ == '__main__':
    rl = RocketInvasion()
    rl.run_game()
