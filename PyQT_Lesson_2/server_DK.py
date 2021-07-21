import select
import json
from socket import socket, AF_INET, SOCK_STREAM

class Server():
    def __init__(self):
        self.address = ('', 10000)
        self.messages = {}
        self.clients = []

    def read_messages(self, r_clients):
        for sock in r_clients:
            try:
                data = sock.recv(1024)
                json_message = data.decode('utf-8')
                message = json.loads(json_message)
                self.messages[sock] = message['message']
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
        return self.messages


    def write_responses(self, requests, w_clients):
        for i in w_clients:
            for sock in requests:
                try:
                    response = requests[sock]
                    msg_dict = {
                        "response": 200,
                        "alert": response
                    }
                    json_message = json.dumps(msg_dict)
                    print(json_message)
                    encoded_message = json_message.encode('utf-8')
                    i.send(encoded_message)
                except:
                    print('Клиент {} {} отключился'.format(i.fileno(), i.getpeername()))
                i.close()


    def mainloop(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(self.address)
        s.listen(5)
        s.settimeout(0.2)
        while True:
            try:
                conn, addr = s.accept()
            except:
                pass
            else:
                self.clients.append(conn)
            r = []
            w = []
            try:
                r, w, e = select.select(self.clients, self.clients, [], 0)
            except:
                pass
            requests = self.read_messages(r)
            self.write_responses(requests, w)

def main():
    server = Server()
    server.mainloop()


if __name__ == '__main__':
    main()
