import socket
import pickle


class Network:
    def __init__(self,port,**init_info):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5556
        self.address = (self.server, self.port)
        self.connect()
        self.local_player = self.send(init_info)
        self.player_list = []

    def get_local_player(self):
        return self.local_player

    def get_player_list(self):
        return self.player_list

    def connect(self):
        """
        初始化与服务器的连接

        :return: 从服务器获取的报文
        """
        try:
            self.client.connect(self.address)
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*10))
        except socket.error as e:
            print(e)
            