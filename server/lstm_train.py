from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras import backend as K
import numpy as np
import collections
import readData
import tools
import os
import h5py
import modelSetting as setting

np.set_printoptions(threshold=np.nan)

active_class = ['stop', 'motion']
motion_class = ['left', 'right', 'left_r', 'right_r', 'up', 'down', 'arm_down', 'arm_up']


# def data_processing(sensor_data, timesteps, data_dim, nb_classes):

# 	num_data = sensor_data.num_data / timesteps
# 	Labels = sensor_data.labels

# 	X_data = np.zeros((num_data, timesteps, data_dim));
# 	y_data = np.zeros((num_data, nb_classes));

# 	for i in xrange(0, num_data):
# 		X_data[i] = sensor_data.all_features[i*30:(i+1)*30]
# 		tmpArr = np.zeros(nb_classes)
# 		tmpArr[int(Labels[i*30])] = 1;
# 		y_data[i] = tmpArr

# 	return X_data, y_data

def build_model(timesteps, data_dim, nb_classes):

	model = Sequential()
	model.add(LSTM(512, return_sequences=True, input_shape=(timesteps, data_dim)))
	model.add(Dropout(setting.dropout))
	model.add(LSTM(512, return_sequences=False))
	model.add(Dropout(setting.dropout))
	model.add(Dense(nb_classes, activation='softmax'))
	# model.add(LSTM(32, return_sequences=True,
	#                input_shape=(timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
	# model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
	# model.add(LSTM(32))  # return a single vector of dimension 32
	# model.add(Dense(nb_classes, activation='softmax'))

	model.compile(loss='categorical_crossentropy',
	              optimizer='adam',
	              metrics=['accuracy'])

	return model


def active_learning(timesteps, data_dim, nb_classes):
	sensor_data = readData.read_sensor_data("data/processed_data/all_train_active.txt");
	sensor_test_data = readData.read_sensor_data("data/processed_data/all_test_active.txt");

	X_train, y_train = tools.data_processing(sensor_data, timesteps, data_dim, nb_classes)
	X_test, y_test = tools.data_processing(sensor_test_data, timesteps, data_dim, nb_classes);

	model = build_model(timesteps, data_dim, nb_classes)

	model.fit(X_train, y_train, batch_size=32, nb_epoch=1, validation_data=(X_test, y_test))

	fileNameH5 = "active_model_weight.h5"
	fileNameJSON = "active_model_config.json"

	filePath = os.path.join("result", fileNameH5);
	model.save_weights(filePath)
	filePath = os.path.join("result", fileNameJSON);
	open(filePath, 'w').write(model.to_json())

def motion_learning(timesteps, data_dim, nb_classes):
	# train_set, train_label, val_set, val_label = split_train_val(readData.read_sensor_data("processed_data/all_train_motion.txt"));
	sensor_data = readData.read_sensor_data("data/processed_data/all_train_motion.txt");
	sensor_test_data = readData.read_sensor_data("data/processed_data/all_test_motion.txt");

	X_train, y_train = tools.data_processing(sensor_data, timesteps, data_dim, nb_classes)
	X_test, y_test = tools.data_processing(sensor_test_data, timesteps, data_dim, nb_classes);

	model = build_model(timesteps, data_dim, nb_classes)

	model.fit(X_train, y_train, batch_size=32, nb_epoch=1, validation_data=(X_test, y_test))

	fileNameH5 = "motion_model_weight.h5"
	fileNameJSON = "motion_model_config.json"

	filePath = os.path.join("result", fileNameH5);
	model.save_weights(filePath)
	filePath = os.path.join("result", fileNameJSON);
	open(filePath, 'w').write(model.to_json())


if __name__ == "__main__":

	active_learning(30, 6, 2);
	motion_learning(30, 6, len(motion_class));




# model = model_from_json(open('my_model_architecture.json').read())
# model.load_weights('my_model_weights.h5')
