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

pub = rospy.Publisher('/cmd_vel', Twist)

def move_drone(predict):
    pub.publish(Twist(Vector3(1,0,0), Vector3(0,0,0)))
    pub.publish(Twist(Vector3(-1,0,0), Vector3(0,0,0)))
    pub.publish(Twist(Vector3(0,1,0), Vector3(0,0,0)))
    pub.publish(Twist(Vector3(0,-1,0), Vector3(0,0,0)))

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
    
                    predict = motion_model.predict(sensorWindow)
                    move_drone(predict)
                else:
                    connection_list.remove(sock)
                    sock.close()
                    print('[INFO][%s] Disconnected' % ctime())

    except KeyboardInterrupt:
        serverSocket.close()
        sys.exit()

# class MyForm(wx.Frame):
#     def __init__(self):
#         self.pub = rospy.Publisher('/cmd_vel', Twist)
#         rospy.init_node('keyboard')

#         wx.Frame.__init__(self, None, wx.ID_ANY, "Key Press Tutorials")

#         panel = wx.Panel(self, wx.ID_ANY)
#         btn = wx.Button(panel, label="OK")

#         btn.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

#         TIMER_ID = 100
#         timer = wx.Timer(panel, TIMER_ID)
#         timer.Start(100)
#         wx.EVT_TIMER(panel, TIMER_ID, on_timer)
        
#     def onKeyPress(self, event):
#         keycode = event.GetKeyCode()
#         if keycode == wx.WXK_UP:
#             print "up"
#             self.pub.publish(Twist(Vector3(1,0,0), Vector3(0,0,0)))
#         elif keycode == wx.WXK_DOWN:
#             print "down"
#             self.pub.publish(Twist(Vector3(-1,0,0), Vector3(0,0,0)))
#         elif keycode == wx.WXK_LEFT:
#             print "left"
#             self.pub.publish(Twist(Vector3(0,1,0), Vector3(0,0,0)))
#         elif keycode == wx.WXK_RIGHT:
#             print "right"
#             self.pub.publish(Twist(Vector3(0,-1,0), Vector3(0,0,0)))

#     def on_timer(event):
#         pass

# if __name__ == "__main__":
#     app = wx.PySimpleApp()
#     frame = MyForm()
#     frame.Show()
#     app.MainLoop()