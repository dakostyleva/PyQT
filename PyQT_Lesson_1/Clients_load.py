import os
import time
from subprocess import Popen

from os import *

p_list = []

path_to_file = os.path.dirname(__file__)
path_to_script_clients = os.path.join(path_to_file, "client_DK.py")

while True:
    clients_num = int(input("Введите число клиентских приложений: "))
    user = input("Запустить клиентов (s) / Закрыть клиентов (x) / Выйти (q): ")

    if user == 'q':
        break
    elif user == 's':
        for i in range(clients_num):
            p_list.append(
                Popen(
                    f'osascript -e \'tell application "Terminal" to do'
                    f' script "python3 {path_to_script_clients}"\'',
                    shell=True))
        print(f'Запущено {clients_num} клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
