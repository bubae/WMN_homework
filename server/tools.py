import numpy as np
import random
from time import ctime, gmtime, strftime


category = ['center', 'left', 'right', 'up', 'down', 'left_rotate', 'right_rotate', 'up_rotate', 'down_rotate']

def data_processing(sensor_data, timesteps, data_dim, nb_classes):

	num_data = sensor_data.num_data / timesteps
	Labels = sensor_data.labels

	X_data = np.zeros((num_data, timesteps, data_dim));
	y_data = np.zeros((num_data, nb_classes));

	for i in xrange(0, num_data):
		X_data[i] = sensor_data.all_features[i*timesteps:(i+1)*timesteps]
		tmpArr = np.zeros(nb_classes)
		tmpArr[int(Labels[i*timesteps])] = 1;
		y_data[i] = tmpArr

	return X_data, y_data

def make_name_with_date(prefix, postfix):
	time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	ret_Name = prefix+"_"+time+postfix
	return ret_Name

def labeling(label_data):
	# example = [[1, 50, 1], [300, 400, 2], [410, 470, 3], [510, 550, 2]]
	d_length = 1000

	label = np.zeros(d_length)
	for lrange in label_data:
		label[lrange[0]:lrange[1]] = lrange[2]

	print label
	
	return label


# labeling()
	# for j in xrange(len(sensorData.accelerometers)):
	# combined_data = np.append(np.append(sensorData.accelerometers[j], sensorData.gyroscopes[j], axis=0), [label], axis=0)
	# f_out.write(' '.join([str(x) for x in combined_data]) )
	# f_out.write('\n')