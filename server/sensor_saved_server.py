# -*- coding: utf8 -*-

# socket 과 select 모듈 임포트
from socket import *
from select import *
import sys, os
import csv
from time import ctime, gmtime, strftime

# 호스트, 포트와 버퍼 사이즈를 지정
HOST = ''
PORT = 3300
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 객체를 만들고..
serverSocket = socket(AF_INET, SOCK_STREAM)

# 서버 정보를 바인딩
serverSocket.bind(ADDR)

# 요청을 기다림(listen)
serverSocket.listen(10)
connection_list = [serverSocket]

# with open('sensor.csv', 'wb') as csvfile:
#     sensorwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     # sensorwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
#     # 무한 루프를 시작
fileName = None
filePath = None
f_out = None

while connection_list:
    try:
        print('[INFO] Waiting connection...')

        # select 로 요청을 받고, 10초마다 블럭킹을 해제하도록 함
        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

        for sock in read_socket:
            # 새로운 접속
            if sock == serverSocket:
                clientSocket, addr_info = serverSocket.accept()
                connection_list.append(clientSocket)

                fileName = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                fileName = "sensorData_"+fileName+".txt"
                filePath = os.path.join("data", fileName);
                f_out = open(filePath, "w")
                print('[INFO][%s] Client(%s) is connected.' % (ctime(), addr_info[0]))

                # 클라이언트로 응답을 돌려줌
                # for socket_in_list in connection_list:
                #     if socket_in_list != serverSocket and socket_in_list != sock:
                #         try:
                #             socket_in_list.send("connection accept")
                #         except Exception as e:
                #             socket_in_list.close()
                #             connection_list.remove(socket_in_list)
            # 접속한 사용자(클라이언트)로부터 새로운 데이터 받음
            else:
                data = sock.recv(BUFSIZE)
                if data:
                    print('Client Data : %s' % data)
                    # print (type(data))
                    split_data = data.split(', ')

                    f_out.write(" ".join(split_data))
                    # f_out.write("\n")
                    # for socket_in_list in connection_list:
                    #     if socket_in_list != serverSocket and socket_in_list != sock:
                    #         try:
                    #             socket_in_list.send('[%s] %s' % (ctime(), data))
                    #             print('[INFO][%s] 클라이언트로 데이터를 전달합니다.' % ctime())
                    #         except Exception as e:
                    #             print(e.message)
                    #             socket_in_list.close()
                    #             connection_list.remove(socket_in_list)
                    #             continue
                else:
                    connection_list.remove(sock)
                    sock.close()
                    f_out.close()
                    print('[INFO][%s] Disconnected' % ctime())
    except KeyboardInterrupt:
        serverSocket.close()
        f_out.close()    
        sys.exit()