import zmq
import threading
import random
import GameState
import GamePlayer


class GameClient:
    def __init__(self,
                 info_port="5557",
                 action_port="5558"):
        self.id = random.randrange(0, 1000)
        self.state = GameState.GameState()
        self.player = GamePlayer.GamePlayer(self.id)
        self.info_port = info_port
        self.action_port = action_port
        self.context = zmq.Context()
        self._init_action_socket()
        self.join_server()
        self._init_info_socket()

    def join_server(self):
        self.action_socket.send_pyobj({"client_id": self.id,
                                       "action": "JOIN"})
        resp = self.action_socket.recv_pyobj()
        if resp['action_response'] == "approved":
            self.state.players.append(self.player)
        else:
            print("FAILED TO JOIN SERVER")

    def _init_info_socket(self):
        self.receive_socket = self.context.socket(zmq.SUB)
        self.receive_socket.connect("tcp://localhost:{}".format(self.info_port))
        self.receive_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.receive_thread = threading.Thread(target=self.get_game_state)
        self.receive_thread.start()

    def _init_action_socket(self):
        self.action_socket = self.context.socket(zmq.REQ)
        self.action_socket.connect("tcp://localhost:{}".format(self.action_port))
        self.action_thread = threading.Thread(target=self.watch_inputs)
        self.action_thread.start()

    def watch_inputs(self):
        a = input("> ")
        if a == 'w':
            self.action_socket.send_pyobj({"client_id": self.id,
                                           "action": "MOVE_UP"})
            resp = self.action_socket.recv_pyobj()
            if resp['action_response'] == "denied":
                print("INVALID MOVE REQUEST")
        elif a == "s":
            self.action_socket.send_pyobj({"client_id": self.id,
                                           "action": "MOVE_DOWN"})
            resp = self.action_socket.recv_pyobj()
            if resp['action_response'] == "denied":
                print("INVALID MOVE REQUEST")
        elif a == "a":
            self.action_socket.send_pyobj({"client_id": self.id,
                                           "action": "MOVE_LEFT"})
            resp = self.action_socket.recv_pyobj()
            if resp['action_response'] == "denied":
                print("INVALID MOVE REQUEST")
        elif a == "d":
            self.action_socket.send_pyobj({"client_id": self.id,
                                           "action": "MOVE_RIGHT"})
            resp = self.action_socket.recv_pyobj()
            if resp['action_response'] == "denied":
                print("INVALID MOVE REQUEST")
        else:
            print("Invalid key")
        self.watch_inputs()

    def get_game_state(self):
        self.state = self.receive_socket.recv_pyobj()
        print(self.state)
        self.get_game_state()
