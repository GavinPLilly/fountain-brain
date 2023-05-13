"""
    Set up GPIO
    Take measurement
        Take five, average middle 3
        Level, datetime
    Try to POST measurement
        If success wait
        If not, write to txt file
"""
import RPi.GPIO as GPIO
import time

class Ultra_sonic:
    _SPEED_OF_SOUND =  1125.0 * 12.0 # in inches/second
    _SENSOR_TO_TOP = 3.5 # inches
    _HEIGHT_OF_TANK = 52.0 # inches from 0% water to 100% water
    def __init__(self):
        self._GPIO_init()

    def _GPIO_init(self):
        """Inits GPIO hardware pins"""
        GPIO.setmode(GPIO.BCM)
        self.TRIG = 23
        self.ECHO = 24
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setwarnings(False)

    def _GPIO_restart(self):
        """Re-inits GPIO hardware pins"""
        self.cleanup()
        self._GPIO_init()

    def _take_single_measurement_inches(self):
        """Returns the reading in inches from a single pulse of the sensor"""
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        timeout_start = time.time()
        pulse_start = time.time()

        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
            if(pulse_start - timer_start > 1):
                raise Exception("Error reading ultra sonic senor")
        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()
            if(pulse_end - pulse_start > 1):
                self._GPIO_restart()
                raise Exception("Error reading ultra sonic sensor")

        pulse_duration = pulse_end - pulse_start
        distance_in_inches = (pulse_duration * self._SPEED_OF_SOUND) / 2

        return distance_in_inches

    def get_measurement(self):
        """
        Takes 5 readings, returns average of middle 3 as percent of
        Well Manager tank height
        """
        measurements = []
        for x in range(0, 5):
            while(True):
                try:
                    measurements.append(self._take_single_measurement())
                    break
                except:
                    pass
        measurements.sort()
        middle_average = (measurements[1] + measurements[2] + measurements[3]) / 3
        percentage_filled = (
                                (
                                    self._HEIGHT_OF_TANK -
                                    (middle_average - self._SENSOR_TO_TOP)
                                )
                                / self._HEIGHT_OF_TANK
                             ) * 100
        return percentage_filled

    def cleanup(self):
        """
            Cleans up the GPIO pins before stopping the program
        """
        GPIO.cleanup()

class Data_exporter:
    def __init__(self):
        pass
    def export(self):
        try:
            # TODO: check if there is cached data to post
            self.post()
        except:
            self.write_to_file()
    def post(self):
        pass
    def write_to_file(self):
        pass

class RPI:
    def __init__(self):
        ultra_sonic = Ultra_sonic()
        data_exporter = Data_exporter()

    def run(self):
        # take measurement
        # export data
