class GamePlayer:
    def __init__(self, id):
        self.location = [0, 0]
        self.id = id

    def __repr__(self):
        return "<Player #{} @ ({}, {})>".format(self.id,
                                                self.location[0],
                                                self.location[1])
