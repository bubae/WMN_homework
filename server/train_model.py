from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn import svm

import numpy as np
import readData

category = ['center', 'left', 'right', 'up', 'down', 'left_rotate', 'right_rotate', 'up_rotate', 'down_rotate']

np.set_printoptions(threshold=np.nan)

# data_dim = 16
# timesteps = 8
# nb_classes = 10

# print "start"

# # expected input data shape: (batch_size, timesteps, data_dim)
# model = Sequential()
# model.add(LSTM(32, return_sequences=True,
#				input_shape=(timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
# model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
# model.add(LSTM(32))  # return a single vector of dimension 32
# model.add(Dense(10, activation='softmax'))

# model.compile(loss='categorical_crossentropy',
#			   optimizer='rmsprop',
#			   metrics=['accuracy'])

# # generate dummy training data
# x_train = np.random.random((1000, timesteps, data_dim))
# y_train = np.random.random((1000, nb_classes))

# # generate dummy validation data
# x_val = np.random.random((100, timesteps, data_dim))
# y_val = np.random.random((100, nb_classes))

# model.fit(x_train, y_train,
#		   batch_size=64, nb_epoch=5,
#		   validation_data=(x_val, y_val))

# print "finished"

def train_lstm(trainData, testData):
	print "hello"

def train_svm(trainData, testData):
	X = trainData.all_features;
	Y = trainData.labels;

	clf = svm.SVC()
	clf.fit(X, Y)  
	# print clf

	print clf.predict(testData.all_features)

	return clf

if __name__ == "__main__":
	trainData = readData.read_sensor_data("processed_data/all_train.txt");
	testData = readData.read_sensor_data("data/test/temp.txt");
	
	print len(testData.all_features)
	train_svm(trainData, testData);
	# for i in xrange(len(testData.all_features)):
		# print testData.all_features[i]
		
	# print sensorData.labels