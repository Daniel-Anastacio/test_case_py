

#TESTE UNDERVOLTAGE

from instruments_academy import Eload, Equity, PSU
from time import sleep


class TestA:
    def __init__(self):
        self._id = 1000,
        self._name = 'Undervoltage academy',
        self._description = 'Dont need'
        self._fsm_state = "START"
        self._fsm_sleep_time = 0.1
        self._temperature_step = 0
    def _fsm(self):
        if self._fsm_state == "START":
            print(f'Actual state: {self._fsm_state}')

            self.eload = Eload()
            self.equity = Equity()
            self.psu = PSU()

            self._config_eload()
            self._config_equity()
            self._config_psu()

            self._temperature = [-10, 25, 85]
            self._actual_temperature = self._temperature[self._temperature_step]
            if not -20 <= _actual_temperature <= 100:
                raise ValueError('Temperature range error')

            self._temperature_stabilization_time = 40
            if not 0 <= _temperature_stabilization_time <= 60:
                raise ValueError('Temperature stabilization time range error') 

            self._current = 0.0
            assert type(self._current) is float
            if not 0.0 <= self._current <= 10.0:
                raise ValueError('Current range error')

            self._initial_voltage = 0
            self._final_voltage = 0
            self._voltage_step = 0.5
            self._psu_steps = 0


            self._fsm_state = "CONFIG EQUITY"

        elif self._fsm_state == "CONFIG ELOAD":
            print(f'Actual state: {self._fsm_state}')
            self.eload.write(f"CURR {self._current}")
            sleep(1)

            self._fsm_state = "CONFIG PSU"

        elif self._fsm_state == "CONFIG EQUITY":
            print(f'Actual state: {self._fsm_state}')
            self.equity.set_temperature(self._actual_temperature)
            while self._actual_temperature != self.equity.get_temperature():
                sleep(1)
            sleep(self._temperature_stabilization_time)


            self._fsm_state = "CONFIG ELOAD"

        elif self._fsm_state == "CONFIG PSU":
            print(f'Actual state: {self._fsm_state}')
            self.psu.set_voltage(self._initial_voltage)
            sleep(1)
            self._fsm_state = "SHOW OUTPUT"

        elif self._fsm_state == "SHOW OUTPUT":
            print(f'Actual state: {self._fsm_state}')

            self._final_voltage = self.psu.get_voltage + self._voltage_step * self._psu_steps

            print(f'Eload current: {self.eload.query("CURR?")}')
            print(f'Eload voltage: {self.eload.query("VOLT?")}')
            
            print(f'PSU current: {self.psu.get_current()}')
            print(f'PSU voltage: {self._final_voltage}')
            
            sleep(1)

            self._psu_steps += 1 
            if self._initial_voltage > self._final_voltage:
                self._fsm_state = "VERIFY TEMPERATURE"
            else:
                self._fsm_state = "SHOW OUTPUT"
        
        elif self._fsm_state == "VERIFY TEMPERATURE":
            print(f"Actual state: {self._fsm_state}")
            self._temperature_step += 1
            if not self._temperature_step >= len(self._temperature):
                self._actual_temperature = self._temperature[self._temperature_step]
                self._fsm_state = "CONFIG EQUITY"
            else:
                self._fsm_state = "END"

        elif self._fsm_state == "END":
            print(f'Actual state: {self._fsm_state}')
            self.psu.set_voltage(0.0)
            self.eload.write('CURR 0')
            self.equity.set_temperature(25)

            self._stop_flag = True

        else:
            exception_message = "FSM reached an invalid state"
            raise Exception(exception_message)

    def _config_eload(self):
        self.eload.write("CURR 0")

    def _config_equity(self):
        self.equity.set_temperature(25)

    def _config_psu(self):
        self.psu.set_voltage(0)

    def _main(self):
        self._stop_flag = False
        while self._stop_flag is False:
            self._fsm()
            sleep(self._fsm_sleep_time)
        print('Test is done')
    
if __name__ == '__main__':
    test = TestA()
    test._main()