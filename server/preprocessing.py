import random
import numpy as np
import pylab
import readData
import os
import tools
import shutil

# category = ['center', 'left', 'right', 'up', 'down', 'left_r', 'right_r']
mode = "test"

active_class = ['stop', 'motion']
motion_class = ['left', 'right', 'left_r', 'right_r', 'up', 'down']

# def test_labeling(filePath):
# 	label_data = [[61, 97, 1], [146, 180, 2], [217, 240, 2], [276, 302, 1], [331, 363, 1], [401, 439, 2], [463, 501, 2], [533, 559, 1], [586, 623, 1], [638, 683, 2], [703, 739, 2], [761, 795, 1 ], [915, 942, 7], [967, 994, 8]]
# 	label = tools.labeling(label_data)

# 	sensorData = readData.read_sensor_data(filePath);

# 	f_out = open("processed_data/out.txt", "w")

# 	# print sensorData.accelerometers

# 	for j in xrange(len(sensorData.accelerometers)):
# 		combined_data = np.append(np.append(sensorData.accelerometers[j], sensorData.gyroscopes[j], axis=0), [label[j]], axis=0)
# 		f_out.write(' '.join([str(x) for x in combined_data]) )
# 		f_out.write('\n')
# 	f_out.close();

def combine_all_train():
	
	fileName = [x[:-4] for x in os.listdir('processed_data/' +mode)];
	filePath = [os.path.join("processed_data", mode, x) for x in os.listdir('data/'+mode)];

	f_out = open("processed_data/all_train.txt", "w")	
	for i in xrange(len(fileName)):

		# if fileName[i] == "center":
		# 	label = 0
		# else:
		# 	label = 1

		label = category.index(fileName[i]);
		sensorData = readData.read_sensor_data(filePath[i]);

		for j in xrange(len(sensorData.accelerometers)):
			combined_data = np.append(np.append(sensorData.accelerometers[j], sensorData.gyroscopes[j], axis=0), [label], axis=0)
			f_out.write(' '.join([str(x) for x in combined_data]) )
			f_out.write('\n')

	f_out.close()


def copy_motion_data():
	for category in motion_class:
		fileName = [x for x in os.listdir('data/' + mode + '/' + category)];
		filePath = [os.path.join("data", mode, category, x) for x in os.listdir('data/' + mode + '/' + category)];
		for i in xrange(len(filePath)):
			shutil.copy(filePath[i], os.path.join("data", mode, "motion", fileName[i]))

def first_class_labeling():
	for category in active_class:	

		f_out = open(os.path.join("data", "processed_data", category+".txt"), "w")
		label = active_class.index(category);
		fileName = [x[:-4] for x in os.listdir('data/' + mode + '/' + category)];
		filePath = [os.path.join("data", mode, category, x) for x in os.listdir('data/' + mode + '/' + category)];

		for i in xrange(len(fileName)):
			sensorData = readData.read_sensor_data(filePath[i]);

			for j in xrange(0, int(len(sensorData.all_features)/30)):

				segment_data = sensorData.all_features[j*30:(j+1)*30];

				for k in xrange(30):
					combined_data = np.append(segment_data[k], [label], axis=0)

					f_out.write(' '.join([str(x) for x in combined_data]) )
					f_out.write('\n')

		f_out.close();

	f_class_all_training()

def second_class_labeling():
	for category in motion_class:	

		f_out = open(os.path.join("data", "processed_data", category+".txt"), "w")
		label = motion_class.index(category);
		fileName = [x[:-4] for x in os.listdir('data/' + mode + '/'+ category)];
		filePath = [os.path.join("data",mode, category, x) for x in os.listdir('data/' + mode + '/'+ category)];

		for i in xrange(len(fileName)):
			sensorData = readData.read_sensor_data(filePath[i]);

			for j in xrange(0, int(len(sensorData.all_features)/30)):

				segment_data = sensorData.all_features[j*30:(j+1)*30];

				for k in xrange(30):
					combined_data = np.append(segment_data[k], [label], axis=0)

					f_out.write(' '.join([str(x) for x in combined_data]) )
					f_out.write('\n')

		f_out.close();

	s_class_all_training()

def f_class_all_training():
	for category in active_class:
		f_out = open(os.path.join("data", "processed_data", "all_"+ mode +"_active.txt"), "w")
		filePath = [os.path.join("data","processed_data", x+'.txt') for x in active_class];

		for path in filePath:
			with open(path) as infile:
				for line in infile:
					f_out.write(line)

def s_class_all_training():
	for category in motion_class:
		f_out = open(os.path.join("data", "processed_data", "all_"+ mode +"_motion.txt"), "w")
		filePath = [os.path.join("data","processed_data", x+'.txt') for x in motion_class];

		for path in filePath:
			with open(path) as infile:
				for line in infile:
					f_out.write(line)

if __name__ == "__main__":

	copy_motion_data();
	first_class_labeling();
	second_class_labeling();
	# fileName = [x[:-4] for x in os.listdir('data/train')];
	# filePath = [os.path.join("data","train", x) for x in os.listdir('data/train')];
	# fileDesPath = [os.path.join("processed_data", "train", x) for x in os.listdir('data/train')];


	# for i in xrange(len(fileName)):
	# 	# if fileName[i] == "center":
	# 	# 	label = 0
	# 	# else:
	# 	# 	label = 1

	# 	label = category.index(fileName[i]);
	# 	print label, fileName[i], filePath[i]
	# 	sensorData = readData.read_sensor_data(filePath[i]);

	# 	f_out = open(fileDesPath[i], "w")

	# 	# print sensorData.accelerometers

	# 	for j in xrange(len(sensorData.accelerometers)):
	# 		combined_data = np.append(np.append(sensorData.accelerometers[j], sensorData.gyroscopes[j], axis=0), [label], axis=0)
	# 		f_out.write(' '.join([str(x) for x in combined_data]) )
	# 		f_out.write('\n')
	# 	f_out.close();

	# combine_all_train()
	# test_labeling("data/temp.txt")