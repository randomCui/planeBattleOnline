import pickle
import socket


class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.address = (self.server, self.port)
        self.connect()
        self.local_object = None

    def init_player(self, **init_info):
        self.send(init_info)
        self.local_object = self.receive()

    def get_local_object(self):
        if self.local_object is None:
            raise ValueError("player hasn't been initialized yet")
        return self.local_object

    def connect(self):
        """
        初始化与服务器的连接

        :return: 从服务器获取的报文
        """
        try:
            self.client.connect(self.address)
            print(self.address)
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(
                data)
            )
        except socket.error as e:
            print(e)

    def receive(self):
        return pickle.loads(self.client.recv(2048))
