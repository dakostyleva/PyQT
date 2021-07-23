'''Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().'''

import subprocess
import ipaddress

node_list = ['2.10.10.1', '127.0.0.1', '192.168.0.1', 'www.google.com']


def host_ping(list):
    for i in list:
        try:
            ip = ipaddress.ip_address(i)
        except ValueError:
            pass

        p = subprocess.Popen(["ping", i, '-c', '1', "-W", "2"], stdout=subprocess.PIPE)
        p.wait()
        if p.poll():
            print(i + " - Узел недоступен")
        else:
            print(i + " - Узел  доступен")


if __name__ == '__main__':
    host_ping(node_list)
