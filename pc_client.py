import asyncio
import socket
import time
import pyautogui
import requests
import xdo
from mss import mss


users = [[], []]  # name, addres
password = "1324fs"

server_ip, server_port = 'ip', 53210

token = "Token"
user_to = 12345678987654321

name = token.split(':')[0]


async def run_server(host, port):  # запуск сервера
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((str(host), int(port)))
    print('PC client start')
    await read_request()


async def server_add_client(data, addres):
    global users, moder
    client_text = data.decode('utf-8')
    if client_text.split(' ')[0] == "/connect":
        if client_text.split(' ')[1] != password:
            sock.sendto("Доступ заблокирован".encode('utf-8'), addres)
        else:
            print(f'connect {addres}')
            users[0].append(client_text.split(' ')[2])
            users[1].append(addres)
    else:
        sock.sendto("Доступ заблокирован".encode('utf-8'), addres)


async def read_request():
    global users
    while True:
        data, addres = sock.recvfrom(8096)
        if addres not in users[1]:
            await server_add_client(data, addres)

        else:
            command_text = data.decode('utf-8')
            if command_text == "/help":
                sock.sendto("hotkey'и можно найти в доках pyautogui\nпримеры:\n"
                            "1. c['volumeup3'] c['volumedown3'] c['volumemute']\n"
                            "2. h['win','3'] h['ctrl','t'] w['https://www.youtube.com/watch?v=dK2rxOVcH38'] p['enter'] t['4'] p['f']".encode('utf-8'), addres)
            elif command_text == "/exit":
                users = [[], []]
                print(f'disconnect {addres}')
            else:
                command_list = command_text.split(' ')
                # print(command_list)
                for i in command_list:
                    time.sleep(1)
                    if i[:1] == "h":  # hotkey
                        pyautogui.hotkey(*[i.replace("'", "") for i in i[2:-1].split(",")])
                    elif i[:1] == "p":  # press
                        pyautogui.press(*[i.replace("'", "") for i in i[2:-1].split(",")])
                    elif i[:1] == "w":  # write
                        pyautogui.write(i[3:-2].replace("$_$", " "), interval=0.02)
                    elif i[:1] == "t":  # time
                        time.sleep(int(i[3:-2]))
                    elif i[:1] == "c":  # command
                        if i[3:-2] == "volmemute":
                            xdo.Xdo().send_keysequence_window(xdo.CURRENTWINDOW, b"XF86AudioMute")
                        elif "volmeup" in i[3:-2]:
                            for j in range(int(i[3:-2].replace("volmeup", ""))):
                                xdo.Xdo().send_keysequence_window(xdo.CURRENTWINDOW, b"XF86AudioRaiseVolume")
                        elif "volmedown" in i[3:-2]:
                            for j in range(int(i[3:-2].replace("volmedown", ""))):
                                xdo.Xdo().send_keysequence_window(xdo.CURRENTWINDOW, b"XF86AudioLowerVolume")
                    elif i[:1] == "s":
                        with mss() as sct:
                            sct.shot()

                        file = r"monitor-1.png"
                        files = {
                            'photo': open(file, 'rb')
                        }
                        message = ('https://api.telegram.org/bot' + token + '/sendPhoto?chat_id='
                                   + str(user_to))
                        requests.post(message, files=files)

                sock.sendto("Выполненно".encode('utf-8'), addres)


if __name__ == '__main__':
    asyncio.run(run_server(server_ip, server_port))
