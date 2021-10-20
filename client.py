import socket
import threading
import random


def read_sok():
    while 1:
        data = sor.recv(1024)
        data_text = data.decode("utf-8")
        print(data_text)


server = 'ip', 53210  # Данные сервера
alias = f"client{random.randint(1, 1000)}"  # Вводим наш псевдоним
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(('', 0))  # Задаем сокет как клиент
sor.sendto(f"/connect 1324fs {alias}".encode('utf-8'), server)  # Уведомляем сервер о подключении
potok = threading.Thread(target=read_sok)
potok.start()

while 1:
    text = input(">>>")
    sor.sendto(f"{text}".encode('utf-8'), server)


# c['volumeup3'] c['volumedown3'] c['volumemute'] s['']
# 5. украйнски сало - h['win','3'] h['ctrl','t'] w['https://youtu.be/zHdceHRWfY0'] p['enter'] t['4'] p['f']
