import random
import numpy
import pylab
import math

class KalmanFilter(object):

	def __init__(self, process_variance, estimated_measurement_variance):
		self.process_variance = process_variance
		self.estimated_measurement_variance = estimated_measurement_variance
		self.posteri_estimate = 0.0
		self.posteri_error_estimate = 1.0

	def input_latest_noisy_measurement(self, measurement):
		priori_estimate = self.posteri_estimate
		priori_error_estimate = self.posteri_error_estimate + self.process_variance

		blending_factor = priori_error_estimate / (priori_error_estimate + self.estimated_measurement_variance)
		self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
		self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

	def get_latest_estimated_measurement(self):
		return self.posteri_estimate

class DataSet(object):
	def __init__(self, accelerometers, gyroscopes, all_features, labels, num_data):
		self._accelerometers = accelerometers
		self._gyroscopes = gyroscopes
		self._all_features = all_features
		self._labels = labels
		self._num_data = num_data
		self._kalman_accelerometers = []
		self._kalman_gyroscopes = []
		self._kalman_features = []

		# self.kalman_filtering();
	@property
	def accelerometers(self):
		return self._accelerometers

	@property
	def gyroscopes(self):
		return self._gyroscopes

	@property
	def all_features(self):
		return self._all_features

	@property
	def labels(self):
		return self._labels

	@property
	def num_data(self):
		return self._num_data

	@property
	def kalman_features(self):
		return self._kalman_features
	

	def kalman_filtering(self, features):
		iteration_count = len(features)

		noise_accel_x = [x[0] for x in features]
		noise_accel_y = [x[1] for x in features]
		noise_accel_z = [x[2] for x in features]

		noise_gyro_x = [x[3] for x in features]
		noise_gyro_y = [x[4] for x in features]
		noise_gyro_z = [x[5] for x in features]

		measurement_standard_deviation = numpy.std([random.random() * 2.0 - 1.0 for j in xrange(iteration_count)])
		estimated_measurement_variance = measurement_standard_deviation ** 2  # 0.05 ** 2

		process_variance = 5.0e-3

		kalman_filter_accel_X = KalmanFilter(process_variance, estimated_measurement_variance)
		kalman_filter_accel_Y = KalmanFilter(process_variance, estimated_measurement_variance)
		kalman_filter_accel_Z = KalmanFilter(process_variance, estimated_measurement_variance)

		kalman_filter_gyro_X = KalmanFilter(process_variance, estimated_measurement_variance)
		kalman_filter_gyro_Y = KalmanFilter(process_variance, estimated_measurement_variance)
		kalman_filter_gyro_Z = KalmanFilter(process_variance, estimated_measurement_variance)

		for iteration in xrange(1, iteration_count):
			kalman_filter_accel_X.input_latest_noisy_measurement(noise_accel_x[iteration])			
			kalman_filter_accel_Y.input_latest_noisy_measurement(noise_accel_y[iteration])
			kalman_filter_accel_Z.input_latest_noisy_measurement(noise_accel_z[iteration])
			kalman_filter_gyro_X.input_latest_noisy_measurement(noise_gyro_x[iteration])
			kalman_filter_gyro_Y.input_latest_noisy_measurement(noise_gyro_y[iteration])
			kalman_filter_gyro_Z.input_latest_noisy_measurement(noise_gyro_z[iteration])

			accel_x = kalman_filter_accel_X.get_latest_estimated_measurement()
			accel_y = kalman_filter_accel_Y.get_latest_estimated_measurement()
			accel_z = kalman_filter_accel_Z.get_latest_estimated_measurement()
			gyro_x = kalman_filter_gyro_X.get_latest_estimated_measurement()
			gyro_y = kalman_filter_gyro_Y.get_latest_estimated_measurement()
			gyro_z = kalman_filter_gyro_Z.get_latest_estimated_measurement()

			self._kalman_features.append([accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z])

		self._kalman_features = np.array(self._kalman_features)
		
def read_data_from_text(data_dir):
	accelerometers = [];
	gyroscopes = [];
	labels = [];
	f_read = open(data_dir, "r")

	while True:
		line = f_read.readline()
		split_data = line.split(' ')
		if not line or len(split_data) < 6: break
		split_data[5] = split_data[5][:-1]
		split_data = [float(x) for x in split_data]
		accelerometers.append(split_data[0:3])
		gyroscopes.append(split_data[3:6])
		if len(split_data) ==7:
			labels.append(split_data[6]);

		# print split_data[0:3], split_data[3:6], len(split_data)
	f_read.close()
	accelerometers = numpy.array(accelerometers)
	gyroscopes = numpy.array(gyroscopes)
	labels = numpy.array(labels)
	# print accelerometers.shape
	# print gyroscopes.shape
	return accelerometers, gyroscopes, labels

def read_sensor_data(data_dir):
	
	accelerometers, gyroscopes, labels = read_data_from_text(data_dir)

	data_set = DataSet(accelerometers, gyroscopes, numpy.append(accelerometers, gyroscopes, axis=1) , labels, len(accelerometers));

	# if fake_data:
	#	 data_sets.train = DataSet([], [], fake_data=True)
	#	 data_sets.validation = DataSet([], [], fake_data=True)
	#	 data_sets.test = DataSet([], [], fake_data=True)
	#	 return data_sets
	# TRAIN_IMAGES = 'train-images-idx3-ubyte.gz'
	# TRAIN_LABELS = 'train-labels-idx1-ubyte.gz'
	# TEST_IMAGES = 't10k-images-idx3-ubyte.gz'
	# TEST_LABELS = 't10k-labels-idx1-ubyte.gz'
	# VALIDATION_SIZE = 5000
	# local_file = maybe_download(TRAIN_IMAGES, train_dir)
	# train_images = extract_images(local_file)
	# local_file = maybe_download(TRAIN_LABELS, train_dir)
	# train_labels = extract_labels(local_file, one_hot=one_hot)
	# local_file = maybe_download(TEST_IMAGES, train_dir)
	# test_images = extract_images(local_file)
	# local_file = maybe_download(TEST_LABELS, train_dir)
	# test_labels = extract_labels(local_file, one_hot=one_hot)
	# validation_images = train_images[:VALIDATION_SIZE]
	# validation_labels = train_labels[:VALIDATION_SIZE]
	# train_images = train_images[VALIDATION_SIZE:]
	# train_labels = train_labels[VALIDATION_SIZE:]
	# data_sets.train = DataSet(train_images, train_labels)
	# data_sets.validation = DataSet(validation_images, validation_labels)
	# data_sets.test = DataSet(test_images, test_labels)
	return data_set

if __name__ == "__main__":
	read_sensor_data("data/center.txt");