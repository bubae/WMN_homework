# -*- coding: utf8 -*-

# socket 과 select 모듈 임포트
import init_path
from socket import *
from select import *
import sys, os
import csv
import numpy as np
import readData, tools
from time import ctime, gmtime, strftime
from keras.models import Sequential, model_from_json
from keras.layers import LSTM, Dense

print np.version.version
print "model load..."
filePath = os.path.join("server", "result", "active_model_config.json");
active_model = model_from_json(open(filePath).read())
filePath = os.path.join("server", "result", "active_model_weight.h5");
active_model.load_weights(filePath)
active_model.compile(optimizer='adam', loss='categorical_crossentropy')

filePath = os.path.join("server", "result", "motion_model_config.json");
motion_model = model_from_json(open(filePath).read())
filePath = os.path.join("server", "result", "motion_model_weight.h5");
motion_model.load_weights(filePath)
motion_model.compile(optimizer='adam', loss='categorical_crossentropy')
print "model load complete"

winSize = 30
data_dim = 6
sensorWindow = np.zeros((1, winSize, data_dim));
sensorWindow[0][0:29] = sensorWindow[0][1:30]

# print "test"
sensor_test_data = readData.read_sensor_data("server/data/processed_data/all_test_motion.txt");
X_data, y_data = tools.data_processing(sensor_test_data, 30, 6, 6)
# print X_data.shape
result = motion_model.predict(X_data[0:1])

print result, sensorWindow.shape


# 호스트, 포트와 버퍼 사이즈를 지정
HOST = ''
PORT = 3300
BUFSIZE = 1024
ADDR = (HOST, PORT)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(ADDR)

serverSocket.listen(10)
connection_list = [serverSocket]

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

                print('[INFO][%s] Client(%s) is connected.' % (ctime(), addr_info[0]))

            else:
                data = sock.recv(BUFSIZE)
                if data:
                    data_lines = data.split('\n')
                    for line in data_lines:
                        split_data = line.split(' ')
                        if len(split_data) != 6: break
                        split_data = [float(x) for x in split_data]
                        sensorWindow[0][0:29] = sensorWindow[0][1:30]
                        sensorWindow[0][29] = split_data
    
                    print motion_model.predict(sensorWindow)
                else:
                    connection_list.remove(sock)
                    sock.close()
                    print('[INFO][%s] Disconnected' % ctime())

    except KeyboardInterrupt:
        serverSocket.close()
        sys.exit()