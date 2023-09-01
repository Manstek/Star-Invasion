class Gamestats():
    """Отслеживаие статистики для игры."""
    def __init__(self, rl):
        self.settings = rl.settings
        self.reset_stats()

        self.game_active = True
    

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
