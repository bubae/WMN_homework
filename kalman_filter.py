import random
import numpy
import pylab
import init_path
import readData

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

if __name__ == "__main__":

    sensorData = readData.read_sensor_data("server/data/temp.txt");
    print sensorData.accelerometers
    iteration_count = sensorData.num_data

    # actual_values = [-0.37727 + j * j * 0.00001 for j in xrange(iteration_count)]
    # noisy_measurement = [random.random() * 2.0 - 1.0 + actual_val for actual_val in actual_values]

    noise_accel_x = [x[0] for x in sensorData.gyroscopes]
    noise_accel_y = [x[1] for x in sensorData.gyroscopes]
    noise_accel_z = [x[2] for x in sensorData.gyroscopes]

    # in practice we would take our sensor, log some readings and get the
    # standard deviation
    measurement_standard_deviation = numpy.std([random.random() * 2.0 - 1.0 for j in xrange(iteration_count)])

    # The smaller this number, the fewer fluctuations, but can also venture off
    # course...
    process_variance = 5.0e-3
    estimated_measurement_variance = measurement_standard_deviation ** 2  # 0.05 ** 2

    print measurement_standard_deviation
    print estimated_measurement_variance
    kalman_filter_X = KalmanFilter(process_variance, estimated_measurement_variance)
    kalman_filter_Y = KalmanFilter(process_variance, estimated_measurement_variance)
    kalman_filter_Z = KalmanFilter(process_variance, estimated_measurement_variance)

    accelerometers_X = []
    accelerometers_Y = []
    accelerometers_Z = []

    for iteration in xrange(1, iteration_count):
        kalman_filter_X.input_latest_noisy_measurement(noise_accel_x[iteration])
        accelerometers_X.append(kalman_filter_X.get_latest_estimated_measurement())

        kalman_filter_Y.input_latest_noisy_measurement(noise_accel_y[iteration])
        accelerometers_Y.append(kalman_filter_Y.get_latest_estimated_measurement())

        kalman_filter_Z.input_latest_noisy_measurement(noise_accel_z[iteration])
        accelerometers_Z.append(kalman_filter_Z.get_latest_estimated_measurement())

    # print sensorData
    pylab.figure()
    pylab.plot(noise_accel_x, color='r', label='noisy x')
    # pylab.plot(noise_accel_y, color='r', label='noisy y')
    # pylab.plot(noise_accel_z, color='r', label='noisy z')
    pylab.plot(accelerometers_X, '-b', label='a posteri estimate x')
    # pylab.plot(accelerometers_Y, '-b', label='a posteri estimate y')
    # pylab.plot(accelerometers_Z, '-b', label='a posteri estimate z')
    # pylab.plot(actual_values, color='g', label='truth value')
    pylab.legend()
    pylab.xlabel('Iteration')
    pylab.ylabel('Voltage')
    pylab.show()

# import random

# # intial parameters
# iteration_count = 500
# actual_values = [-0.37727 + j * j * 0.00001 for j in xrange(iteration_count)]
# noisy_measurement = [random.random() * 0.6 - 0.3 + actual_val for actual_val in actual_values]

# process_variance = 1e-5  # process variance

# estimated_measurement_variance = 0.1 ** 2  # estimate of measurement variance, change to see effect

# # allocate space for arrays
# posteri_estimate_for_graphing = []

# # intial guesses
# posteri_estimate = 0.0
# posteri_error_estimate = 1.0

# for iteration in range(1, iteration_count):
#     # time update
#     priori_estimate = posteri_estimate
#     priori_error_estimate = posteri_error_estimate + process_variance

#     # measurement update
#     blending_factor = priori_error_estimate / (priori_error_estimate + estimated_measurement_variance)
#     posteri_estimate = priori_estimate + blending_factor * (noisy_measurement[iteration] - priori_estimate)
#     posteri_error_estimate = (1 - blending_factor) * priori_error_estimate
#     posteri_estimate_for_graphing.append(posteri_estimate)

# import pylab
# pylab.figure()
# pylab.plot(noisy_measurement, color='r', label='noisy measurements')
# pylab.plot(posteri_estimate_for_graphing, 'b-', label='a posteri estimate')
# pylab.plot(actual_values, color='g', label='truth value')
# pylab.legend()
# pylab.xlabel('Iteration')
# pylab.ylabel('Voltage')
# pylab.show()