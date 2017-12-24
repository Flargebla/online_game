class GameState:
    def __init__(self):
        self.players = []
        self.map_width = 10
        self.map_height = 10

    def get_state(self):
        return {"players": self.players,
                "map_width": self.map_width,
                "map_height": self.map_height}
