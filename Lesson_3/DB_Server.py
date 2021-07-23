'''1. Начать реализацию класса «Хранилище» для серверной стороны. Хранение необходимо осуществлять в базе данных.
В качестве СУБД использовать sqlite. Для взаимодействия с БД можно применять ORM.
Опорная схема базы данных:
На стороне сервера БД содержит следующие таблицы:
a) клиент:
* логин;
* информация.
b) историяклиента:
* время входа;
* ip-адрес.
c) списокконтактов (составляется на основании выборки всех записей с id_владельца):
* id_владельца;
* id_клиента.'''

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Time
from sqlalchemy.orm import mapper, sessionmaker
from server_DK import Server

engine = create_engine('sqlite:///BD_Server.sqlite', echo=True)

metadata = MetaData()
clients_table = Table('clients', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('login', String),
                      Column('information', String)
                      )

clients_history_table = Table('clients_history', metadata,
                              Column('id', Integer, primary_key=True),
                              Column('client_id', Integer, ForeignKey('clients.id')),
                              Column('login_time', Time),
                              Column('ip_address', String)
                              )

contact_list = Table('contacts', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('owner_id', Integer, ForeignKey('clients.id')),
                     Column('client_id', Integer, ForeignKey('clients.id'))
                     )

metadata.create_all(engine)


class Client:
    def __init__(self, id, login, info):
        self.id = id
        self.login = login
        self.info = info


class ClientHistory:
    def __init__(self, id, client_id, login_time, ip_address):
        self.id = id
        self.client_id = client_id
        self.login_time = login_time
        self.ip_address = ip_address

class Contacts:
    def __init__(self, owner_id, client_id):
        self.id = id
        self.owner_id = owner_id
        self.client_id = client_id


mapper(Client, clients_table)
mapper(ClientHistory, clients_history_table)
mapper(Contacts, contact_list)
