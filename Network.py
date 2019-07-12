import socket
import pickle

def get_ip_address():
    ''' return ip address of local network '''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class Network:
    ''' this class used as bridge between client and server '''

    #constructor
    def __init__(self):

        #create socket 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #local network ip
        self.ip = '192.168.1.7' #get_ip_address() 

        #port
        self.port = 5555

    def connect(self):
        ''' connect to server '''

        #connect 
        self.client.connect((self.ip,self.port))

        #get player shape
        return pickle.loads(self.client.recv(4096 * 2))

    def receive_object(self):
        return pickle.loads(self.client.recv(8192))

    def send_object(self,data):
        self.client.send(pickle.dumps(data))
        return pickle.loads(self.client.recv(8192))





'''class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.11.250.207"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)'''