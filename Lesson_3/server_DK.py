import select
import json
from socket import socket, AF_INET, SOCK_STREAM


class Server():
    def __init__(self):
        self.address = ('', 10000)
        self.messages = {}
        self.clients = []

    def read_messages(self, r_clients):
        for sock in r_clients: #проходим по списку клиентов, которые что-то прислали
            try:
                data = sock.recv(1024)
                json_message = data.decode('utf-8')
                message = json.loads(json_message)
                self.messages[sock] = (message['sender'], message['message']) #словарь  {сокет: сообщение от него}
                print(self.messages)
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
        return self.messages

    def write_responses(self, requests, w_clients): #requests = {сокет: сообщение от него}, w_clients = список подключенных сокетов
        for sock in requests:
            for i in w_clients:
                try:
                    response = requests[sock]
                    msg_dict = {
                        "response": 200,
                        "alert": response
                    }
                    json_message = json.dumps(msg_dict)
                    print(json_message)
                    encoded_message = json_message.encode('utf-8')
                    i.send(encoded_message) #отправляем каждому сокету сообщение
                except:
                    print('Клиент {} {} отключился'.format(i.fileno(), i.getpeername()))
        requests.clear()


    def mainloop(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(self.address)
        s.listen(5)
        s.settimeout(0.5)
        while True:
            try:
                conn, addr = s.accept() #открыли сокет, получили ip и порт (addr)
                print(conn)
                print(addr)
            except:
                pass
            else:
                self.clients.append(conn) #clients - список подключившихся сокетов
            r = [] #список клиентов на чтение
            w = [] #список клиентов на отправку
            try:
                r, w, e = select.select(self.clients, self.clients, [], 0) #clients включаются в список на чтение и на отправку
            except:
                pass
            print(f'r = {r}') #В список попадают сокеты, которые прислали сообщения
            print(f'w = {w}') #В список сразу попадают все плдключенные сокеты
            requests = self.read_messages(r) #получаем словарь {сокет: сообщение от него}
            self.write_responses(requests, w)


def main():
    server = Server()
    server.mainloop()


if __name__ == '__main__':
    main()
