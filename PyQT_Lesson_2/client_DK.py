import threading
import time
import json
from socket import AF_INET, SOCK_STREAM, socket


class ClientSender(threading.Thread):
    def __init__(self, sock):
        self.socket = sock
        super().__init__()

    def run(self):
        while True:
            try:
                what_to_do = input('Choose what to do [(m) - write a message; (q) - quit]: ')
                if what_to_do == 'm':
                    message = input('Enter your message: ')
                    msg_dict = {
                        "action": "message",
                        "time": time.time(),
                        "message": message
                    }
                    json_message = json.dumps(msg_dict)
                    encoded_message = json_message.encode('utf-8')
                    self.socket.send(encoded_message)
                else:
                    print(f'Press m or q')
                    continue
            except:
                print('error_write')


class ClientReader(threading.Thread):
    def __init__(self, sock):
        self.socket = sock
        super().__init__()

    def run(self):
        while True:
            #try:
            data = self.socket.recv(1024)
            json_message = data.decode('utf-8')
            message = json.loads(json_message)
            server_response = message['alert']
            print(f'Message from chat: {server_response}')
            #except:
                #print('error_read')


def main():
    with socket(AF_INET, SOCK_STREAM) as sock:
        try:
            sock.connect(('', 10000))
        except json.JSONDecodeError:
            print('Не удалось декодировать полученную Json строку.')
            exit(1)
        except (ConnectionRefusedError, ConnectionError):
            print(
                f'Не удалось подключиться к серверу, конечный компьютер отверг запрос на подключение.')
            exit(1)
        else:
            w_thread = ClientSender(sock)
            w_thread.daemon = False
            w_thread.start()
            r_thread = ClientReader(sock)
            r_thread.daemon = True
            r_thread.start()
            while True:
                time.sleep(1)
                if w_thread.is_alive() and r_thread.is_alive():
                    continue
                break


if __name__ == '__main__':
    main()
