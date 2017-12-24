import zmq
import threading
import time
import sched
import Game


class GameServer:
    def __init__(self,
                 info_port="5557",
                 action_port="5558"):
        self.game = Game.Game()
        self.info_port = info_port
        self.action_port = action_port
        self.context = zmq.Context()
        self._init_action_socket()
        self._init_info_socket()

    def _init_info_socket(self):
        self.receive_socket = self.context.socket(zmq.PUB)
        self.receive_socket.bind("tcp://*:{}".format(self.info_port))
        self.info_thread = threading.Thread(target=self.send_state)
        self.info_thread.start()

    def _init_action_socket(self):
        self.action_socket = self.context.socket(zmq.REP)
        self.action_socket.bind("tcp://*:{}".format(self.action_port))
        self.action_thread = threading.Thread(target=self.listen_inputs)
        self.action_thread.start()

    def listen_inputs(self):
        message = self.action_socket.recv_pyobj()
        print("<Server received input req> {}".format(message))
        response = self.game.handle_action_request(message)
        self.action_socket.send_pyobj(response)
        self.listen_inputs()

    def send_state(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.enter(1, 1, self._send_state)
        self.scheduler.run()

    def _send_state(self):
        self.receive_socket.send_pyobj(self.game.get_state())
        self.scheduler.enter(1, 1, self._send_state)
