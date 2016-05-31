import random
import numpy as np
import pylab
import readData
import os
import tools
import shutil

# category = ['center', 'left', 'right', 'up', 'down', 'left_r', 'right_r']
# mode = "test"

testRatio = 0.2

active_class = ['stop', 'motion']
motion_class = ['left', 'right', 'left_r', 'right_r', 'up', 'down', 'arm_down', 'arm_up']

def copy_motion_data():
	for category in motion_class:
		fileName = [x for x in os.listdir('data/train/' + category)];
		filePath = [os.path.join("data", "train", category, x) for x in os.listdir('data/train/' + category)];
		for i in xrange(len(filePath)):
			shutil.copy(filePath[i], os.path.join("data", "train", "motion", fileName[i]))

def funccc(outFile, label, index, filePath):
	f_out = open(os.path.join("data", "processed_data", outFile+".txt"), "w")

	for i in index:
		sensorData = readData.read_sensor_data(filePath[i]);

		for j in xrange(0, int(len(sensorData.all_features)/30)):

			segment_data = sensorData.all_features[j*30:(j+1)*30];

			for k in xrange(30):
				combined_data = np.append(segment_data[k], [label], axis=0)

				f_out.write(' '.join([str(x) for x in combined_data]) )
				f_out.write('\n')		
	f_out.close();


def first_class_labeling():

	for category in active_class:	

		label = active_class.index(category);
		fileName = [x[:-4] for x in os.listdir('data/train/' + category)];
		filePath = [os.path.join("data", "train", category, x) for x in os.listdir('data/train/' + category)];

		numData = len(fileName)
		numTest = int(numData * testRatio)
		numTrain = numData - numTest
		temp_arr = np.arange(0, numData)
		mask = np.ones(temp_arr.shape, dtype=bool)
		testIndex = np.random.choice(len(temp_arr), numTest)
		mask[testIndex] = 0
		trainIndex = temp_arr[mask]

		funccc("train_"+category, label, trainIndex, filePath)
		funccc("test_"+category, label, testIndex, filePath)

	f_class_all_training("train")
	f_class_all_training("test")

def second_class_labeling():
	for category in motion_class:	

		# f_out = open(os.path.join("data", "processed_data", category+".txt"), "w")
		label = motion_class.index(category);
		fileName = [x[:-4] for x in os.listdir('data/train/' + category)];
		filePath = [os.path.join("data", "train", category, x) for x in os.listdir('data/train/' + category)];

		numData = len(fileName)
		numTest = int(numData * testRatio)
		numTrain = numData - numTest
		temp_arr = np.arange(0, numData)
		mask = np.ones(temp_arr.shape, dtype=bool)
		testIndex = np.random.choice(len(temp_arr), numTest)
		mask[testIndex] = 0
		trainIndex = temp_arr[mask]

		funccc("train_"+category, label, trainIndex, filePath)
		funccc("test_"+category, label, testIndex, filePath)


	s_class_all_training("train")
	s_class_all_training("test")

def f_class_all_training(mode):

	f_out = open(os.path.join("data", "processed_data", "all_"+ mode +"_active.txt"), "w")

	for category in active_class:
		filePath = [os.path.join("data","processed_data", mode+ '_' + x +'.txt') for x in active_class];

		for path in filePath:
			with open(path) as infile:
				for line in infile:
					f_out.write(line)

	f_out.close();

def s_class_all_training(mode):

	f_out = open(os.path.join("data", "processed_data", "all_"+ mode +"_motion.txt"), "w")
	for category in motion_class:
		filePath = [os.path.join("data","processed_data", mode+ '_' + x +'.txt') for x in motion_class];

		for path in filePath:
			with open(path) as infile:
				for line in infile:
					f_out.write(line)

	f_out.close();

if __name__ == "__main__":

	copy_motion_data();
	first_class_labeling();
	second_class_labeling();
