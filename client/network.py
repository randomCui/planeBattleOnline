import pickle
import socket


class Network:
    def __init__(self, ip, port):
        # 初始化自己的socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 保存连接的ip和端口
        self.server = ip
        self.port = port
        self.address = (self.server, self.port)

        # 连接服务器
        self.connect()

        # 初始化自身对象
        self.local_object = None

    def init_player(self, **init_info):
        """
        通过给服务器发送初始化数据得到服务器所给的玩家对象

        :param init_info: 初始化信息
        :return:
        """
        # 发送数据
        self.send(init_info)
        # 接收数据
        self.local_object = self.receive()

    def get_local_object(self):
        # 得到服务器返回的初始化玩家
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
        # 使用pickle将python对象序列化，使用TCP协议传输
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def receive(self):
        # 从服务器得到数据，使用pickle解包
        return pickle.loads(self.client.recv(2048 * 50))

    def disconnect(self):
        # 从服务器断开连接
        self.client.close()
