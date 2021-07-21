'''2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.'''

import subprocess
import ipaddress


def host_range_ping():
    ip_start = input('Enter first ip-address to check: ')
    ip_range = int(input('Enter number of ip-addresses: '))
    for i in range(ip_range):
        try:
            ip = str(ipaddress.ip_address(ip_start) + i)
        except ValueError:
            print('Incorrect ip')
            break
        p = subprocess.Popen(["ping", ip, '-c', '1', "-W", "2"], stdout=subprocess.PIPE)
        p.wait()
        if p.poll():
            print(ip + " - Узел недоступен")
        else:
            print(ip + " - Узел  доступен")


if __name__ == '__main__':
    host_range_ping()
