import threading
import time
import json
from socket import AF_INET, SOCK_STREAM, socket


class ClientSender(threading.Thread):
    def __init__(self, sock):
        self.socket = sock
        super().__init__()

    def run(self):
        client_name = input('Please enter your name: ')
        print (f'Hello, {client_name}! Welcome to the chat!'
               f'\nEnter "q" or "quit" when you\'d like to quit. ')
        while True:
            try:
                message = input('Enter your message: ')
                if message == "quit" or message == "q":
                    break
                else:
                    msg_dict = {
                        "action": "message",
                        "time": time.time(),
                        "sender": client_name,
                        "message": message
                    }
                    json_message = json.dumps(msg_dict)
                    encoded_message = json_message.encode('utf-8')
                    self.socket.send(encoded_message)
            except:
                break


class ClientReader(threading.Thread):
    def __init__(self, sock):
        self.socket = sock
        super().__init__()

    def run(self):
        while True:
            try:
                data = self.socket.recv(1024)
                json_message = data.decode('utf-8')
                message = json.loads(json_message)
                server_response_sender = message['alert'][0]
                server_response_message = message['alert'][1] #(message['sender'], message['message'])
                print(f'\n{server_response_sender}: {server_response_message}')
            except:
                break


def main():
    with socket(AF_INET, SOCK_STREAM) as sock:
        try:
            sock.connect(('', 10000))
        except json.JSONDecodeError:
            print('Cannot decode the JSON-string.')
        except (ConnectionRefusedError, ConnectionError):
            print('Cannot reach the server.')
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
