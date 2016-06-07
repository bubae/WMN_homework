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
import tools

active_class = ['stop', 'motion']
motion_class = ['left', 'right', 'left_r', 'right_r', 'up', 'down', 'arm_down', 'arm_up']

print "model load..."
filePath = os.path.join("server", "result", "active_model_config.json");
active_model = model_from_json(open(filePath).read())
filePath = os.path.join("server", "result", "active_model_weight.h5");
active_model.load_weights(filePath)
active_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])

filePath = os.path.join("server", "result", "motion_model_config.json");
motion_model = model_from_json(open(filePath).read())
filePath = os.path.join("server", "result", "motion_model_weight.h5");
motion_model.load_weights(filePath)
motion_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])
print "model load complete"
# test_on_batch

m_threshold = 0.5
a_threshold = 0.5

def main():
	# sensor_test_data = readData.read_sensor_data("data/processed_data/all_test_active.txt");
	timesteps = 30
	data_dim = 6
	nb_classes = 2

	sensor_test_data = readData.read_sensor_data("server/data/demo_data.txt");
	# X_test, y_test = tools.data_processing(sensor_test_data, timesteps, data_dim, nb_classes);
	# val = active_model.evaluate(X_test, y_test, batch_size=1, show_accuracy=True)
	f_out = open("demo_output.txt", "w")
	sensorWindow = np.zeros((1, timesteps, data_dim));
	# print sensor_test_data.num_data-30
	for i in xrange(0, sensor_test_data.num_data-30):
		sensorWindow[0] = sensor_test_data.all_features[i:i+30]

		# print sensorWindow.shape
		softmax_active = active_model.predict(sensorWindow)
		# print softmax_active
		a_index = np.where(softmax_active[0]==max(softmax_active[0]))[0][0]
		# print max(softmax_active), active_class[index]
		softmax_motion = motion_model.predict(sensorWindow)
		m_index = np.where(softmax_motion[0]==max(softmax_motion[0]))[0][0]

		if a_index == 1:
			if max(softmax_motion[0]) > m_threshold:
				output = motion_class[m_index] + " " + str(max(softmax_motion[0])) + "\n"
				f_out.write(output)
				print motion_class[m_index], max(softmax_motion[0]) 
		else:
			if max(softmax_active[0]) > a_threshold:
				output = active_class[a_index] + " " + str(max(softmax_active[0])) + "\n"
				f_out.write(output)
				print active_class[a_index], max(softmax_active[0])

	f_out.close();
if __name__ == "__main__":
	main()