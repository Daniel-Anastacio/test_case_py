

class Eload:
    """A class that represents the eletronic load
    """
    def __init__(self):
        """Initilazer function
        """
        self.voltage = 0
        self.current = 0
        self.power = self.voltage * self.current
        self._buffer = None

    def write(self, command):
        """The function that send commands to Eload

        Args:
            command (str): Command to get or to set a parameter

        Raises:
            ValueError: Unknown command 
        """
        assert type(command) is str

        if command.startswith('CURR'):
            if command.endswith('?'):
                self._buffer = self.current
            else:
                command_string = command.split(' ')
                self.current = float(command_string[1])

        elif command == 'MEAS:CURR?':
            self._buffer = self.current

        elif command.startswith('VOLT'):
            if command.endswith('?'):
                self._buffer = self.voltage
            else:
                command_string = command.split(' ')
                self.voltage = float(command_string[1])

        elif command == 'MEAS:VOLT?':
            self._buffer = self.voltage

        elif command == 'MEAS:POW?':
           self._buffer = self.current * self.voltage

        else:
            raise ValueError('Not recognized command')

    def read(self):
        """The function that read a data in the buffer

        Returns:
            str: Data to read
        """
        buffer = str(self._buffer)
        self._buffer = None

        return buffer

    def query(self, command):
        """The function that query a attribute in a object Eload 

        Args:
            command (str): Command to get or to set a parameter

        Raises:
            ValueError: A unknown command

        Returns:
            str: A attribute consulted
        """
        assert type(command) is str

        if command == 'CURR?':
            return str(self.current)

        elif command == 'MEAS:CURR?':
            return str(self.current)

        elif command == 'VOLT?':
            return str(self.voltage)

        elif command == 'MEAS:VOLT?':
            return str(self.voltage)

        elif command == 'MEAS:POW?':
            return str(self.current * self.voltage)

        else:
            raise ValueError('Not recognized command')


class PSU:
    """A class that represents the power supply unity
    """
    def __init__(self):
        """Initialazer function
        """
        self.voltage = 0
        self._current = 1

    def get_voltage(self):
        """A function that get the voltage as attribute

        Returns:
            int: The voltage in PSU
        """
        return self.voltage

    def set_voltage(self, voltage):
        """A function that set the voltage as attribute

        Args:
            voltage (int): The value that will be assigned to the element voltage
        """
        assert (type(voltage) is float) or (type(voltage) is int)
        self.voltage = voltage

    def get_current(self):
        """A function that get the current as attribute

        Returns:
            int: The current in PSU
        """
        return self._current

    def get_power(self):
        """A function that calculates the power in PSU

        Returns:
            int: The power in PSU
        """
        return self.voltage * self._current


class Equity:
    """A class that represents tha chamber temperature
    """
    def __init__(self):
        """Initializer function
        """
        self._temperature = 25

    def get_temperature(self):
        """A function to get the temperature in chamber

        Returns:
            int: The temperature in chamber temperature
        """
        return self._temperature

    def set_temperature(self, temperature):
        """A funtion to set a new tmeperature in chamber temperature

        Args:
            temperature (int): The temperature that will be able in chamber temperature
        """
        assert (type(temperature) is float) or (type(temperature) is int)
        self._temperature = temperature