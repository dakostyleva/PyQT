'''3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:'''
import subprocess
import ipaddress
from tabulate import tabulate

unreach_list = []
reach_list = []


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
            #print(ip + " - Узел недоступен")
            unreach_list.append(ip)
        else:
            #print(ip + " - Узел  доступен")
            reach_list.append(ip)
    dict = {'Недоступные узлы': unreach_list, 'Доступные узлы':reach_list}
    print(tabulate(dict, headers='keys'))


if __name__ == '__main__':
    host_range_ping()
