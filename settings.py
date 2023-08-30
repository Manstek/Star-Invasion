class Settings():
    """Класс для хранения всех настроек."""

    def __init__(self):
        """Инициализирует настройки игры."""
        self.bg_color = (230, 230, 230)
        self.screen_width = 1200
        self.screen_height = 800
        self.ship_speed = 1.5

        self.bullet_speed = 1
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        self.star_speed = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1 - move down ; -1 - move up

