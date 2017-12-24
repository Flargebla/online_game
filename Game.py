import GameState
import GamePlayer


class Game:
    def __init__(self):
        self.state = GameState.GameState()

    def get_state(self):
        return self.state.get_state()

    def handle_action_request(self, request):
        if request['action'] == "JOIN":
            self.state.players.append(GamePlayer.GamePlayer(request["client_id"]))
            return {"action_response": "approved"}
        elif request['action'] == "MOVE_UP":
            for p in self.state.players:
                if p.id == request['client_id']:
                    if p.location[0] < self.state.map_height:
                        p.location[0] += 1
                        return {"action_response": "approved"}
        elif request['action'] == "MOVE_DOWN":
            for p in self.state.players:
                if p.id == request['client_id']:
                    if p.location[0] > 0:
                        p.location[0] -= 1
                        return {"action_response": "approved"}
        elif request['action'] == "MOVE_LEFT":
            for p in self.state.players:
                if p.id == request['client_id']:
                    if p.location[1] > 0:
                        p.location[1] -= 1
                        return {"action_response": "approved"}
        elif request['action'] == "MOVE_RIGHT":
            for p in self.state.players:
                if p.id == request['client_id']:
                    if p.location[1] < self.state.map_width:
                        p.location[1] += 1
                        return {"action_response": "approved"}
        return {"action_response": "denied"}
