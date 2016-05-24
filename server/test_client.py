# -*- coding: utf8 -*-

# socket 모듈을 임포트
from socket import *
from select import select
import sys
import time

# 호스트, 포트와 버퍼 사이즈를 지정
HOST = '143.248.135.71'
PORT = 3330
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 객체를 만들고
clientSocket = socket(AF_INET, SOCK_STREAM)

# 서버와의 연결을 시도
try:
    clientSocket.connect(ADDR)
except Exception as e:
    print('채팅 서버(%s:%s)에 연결 할 수 없습니다.' % ADDR)
    sys.exit()
print('채팅 서버(%s:%s)에 연결 되었습니다.' % ADDR)


def prompt():
    sys.stdout.write('<나> ')
    sys.stdout.flush()

# 무한 루프를 시작
while True:
    try:
        connection_list = [sys.stdin, clientSocket]

        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

        for sock in read_socket:
            if sock == clientSocket:
                data = sock.recv(BUFSIZE)
                if not data:
                    clientSocket.close()
                    sys.exit()
                else:
                    print('%s' % data)  # 메세지 시간은 서버 시간을 따른다
                    # prompt()
            else:
                time.sleep(0.01)
                clientSocket.send("3.12345, 4.12345, 5.12345")

    except KeyboardInterrupt:
        clientSocket.close()
        sys.exit()