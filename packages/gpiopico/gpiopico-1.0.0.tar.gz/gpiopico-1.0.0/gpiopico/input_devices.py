from umachine import Pin, ADC, UART, I2C
from utime import sleep, sleep_ms
from urtc import DS1307

_VOLTAGE_REF: float = 3.3
_SAMPLES: int = 65535

class RotaryEncoder:
    """
        :dt_pin int
        :clk_pin int
        :sw: int
        :max_step int
        :wrapper bool
        
        encoder = RotaryEncoder(2, 3, 4, max_step=100)

        while True:
            encoder.read()
            sleep(0.009)
            print(encoder.value)
            print(encoder.is_pressed)
    """
    def __init__(
        self,
        dt_pin: int,
        clk_pin: int,
        sw: int,
        max_step: int=10,
        wrapper: bool=True
    ) -> None:
        self._value: int = 0
        self._is_pressed: bool = False
        self._DT_Pin = Pin(dt_pin, Pin.IN, Pin.PULL_UP)
        self._CLK_Pin = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self._SW = Pin(sw, Pin.IN, Pin.PULL_UP)
        self._wrapper: bool = wrapper
        self._previous_value: int = 1
        self._max_step:int = max_step
    
    @property
    def value(self):
        return self._value
    
    @property
    def is_pressed(self):
        return self._is_pressed
    
    def _read_rotatory_state(self) -> None:
        if self._previous_value != self._CLK_Pin.value():
            if not self._CLK_Pin.value():
                if not self._DT_Pin.value():
                    self._value = (self._value - 1)%self._max_step
                else:
                    self._value = (self._value + 1)%self._max_step
            self._previous_value = self._CLK_Pin.value()
        
    def _read_button_state(self) -> None:
        if self._SW.value() == 0:
            if self._wrapper:
                self._is_pressed = not(self._is_pressed)
            else:
                #TODO Change this for Event()
                self._is_pressed = True
    
    def read(self) -> None:
        self._read_button_state()
        self._read_rotatory_state()
        

class AnalogicInputs:
    """
        valid pins: int [26, 27, 28]
    """
    def __init__(
        self,
        adc_pin: int,
        voltage_ref: float = _VOLTAGE_REF
    ) -> None:
        if adc_pin not in [4, 26, 27, 28]:
            raise ValueError('adc_pin defined it´s not analogic pin')
        self._input = ADC(adc_pin)
        self._conversion_factor = voltage_ref / _SAMPLES

    def read_voltage(self) -> float:
        return self._input.read_u16() * self._conversion_factor
    
    def read_adc(self) -> int:
        return self._input.read_u16()

class Potentiometer(AnalogicInputs):
    """
        adc_input = Potentiometer(28)
        while True:
            print(adc_input.read_adc())
            sleep(0.1)
        
        :adc_pin
        :voltage_ref
    """
    def __init__(
        self,
        adc_pin: int,
        voltage_ref: float = _VOLTAGE_REF
    ) -> None:
        super().__init__(adc_pin, voltage_ref)

class Joystick(AnalogicInputs):
    """
        :adc_pin_rx
        :adc_pin_ry
        :button_pin
        :function_after_press -> pure function
        :voltage_ref
        :core_range
        
        joystick = Joystick(26, 27, 22)
        # With event after press button
        # joystick = Joystick(26, 27, 22, function_after_press=test)
        while True:
            direction = joystick.get_direction()
            print(direction)
            sleep(0.1)
    """
    def __init__(
        self,
        adc_pin_rx: int,
        adc_pin_ry: int,
        button_pin:int,
        function_after_press = None,
        voltage_ref: float = _VOLTAGE_REF,
        core_range = (40000, 30000)
    ) -> None:
        super().__init__(adc_pin_rx, voltage_ref)
        self._input_x = self._input
        self._input_y = ADC(adc_pin_ry)
        self._button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self._function_after_press = function_after_press
        self._rx_value: int
        self._ry_value: int
        self._core_range = core_range

    def _run_event(self):
        if not self._button.value() and self._function_after_press:
            self._function_after_press()
    
    def get_direction(self):
        self._rx_value = self._input_x.read_u16()
        self._ry_value = self._input_y.read_u16()
        self._run_event()
        if self._rx_value > self._core_range[0]:
            return 'Up'
        if self._rx_value < self._core_range[1]:
            return 'Down'
        if self._ry_value > self._core_range[0]:
            return 'Right'
        if self._ry_value < self._core_range[1]:
            return 'Left'
        else: return

class LM35(AnalogicInputs):
    pass

class RaspiTemp(AnalogicInputs):
    def __init__(self, )->None:
        super().__init__(4, _VOLTAGE_REF)
    
    def _read_value(self):
        _voltaje = self.read_voltage()
        temperature_celcius = 27 - (_voltaje - 0.706)/0.001721 
        sleep_ms(500)
        return temperature_celcius
    
    def read(self, samples:int=1)->float:
        #TODO apply samples
        return self._read_value()

class Button:
    def __init__(
        self,
        pin: int,
        invert_logic: bool = False,
        show_value: bool = False
    ) -> None:
        self._input = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._when_pressed = None
        self._on_hold = None
        self._show_value = show_value
        self._value = 1 if not invert_logic else 0

    @staticmethod
    def _validate_callback(callback):
        #TODO CHANGE TO INSTANCE
        if (
            type(callback).__name__ == 'function' or
            type(callback).__name__ == 'bound_method'
        ):
            return
        else:
            raise ValueError('callback will be a function or bound_method')

    @property
    def when_pressed(self):
        return self._when_pressed
    
    @when_pressed.setter
    def when_pressed(self, callback):
        self._validate_callback(callback)
        self._when_pressed = callback
    
    @property
    def on_hold(self):
        return self._on_hold
    
    @on_hold.setter
    def on_hold(self, callback):
        self._validate_callback(callback)
        self._on_hold = callback
    
    def check_state(self):
        _value = self._input.value()
        if self._when_pressed and _value == self._value:
            self._when_pressed()
        else:
            if self._on_hold: self._on_hold()
        (print(_value) if self._show_value else None)
        sleep(0.1)

class PIR:
    def __init__(
        self,
        pin: int,
        show_value: bool = False
    ) -> None:
        self._input = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._when_motion_is_detected = None
        self._value = None
        self._show_value = show_value

    @property
    def value(self):
        return self._input.value()

    @property
    def when_motion_is_detected(self):
        return self._when_motion_is_detected
    
    @when_motion_is_detected.setter
    def when_motion_is_detected(self, callback):
        #TODO CHANGE TO INSTANCE
        if (
            type(callback).__name__ == 'function' or
            type(callback).__name__ == 'bound_method'
        ):
            self._when_motion_is_detected = callback
        else:
            raise ValueError('callback will be a function or bound_method')
    
    def active_motion_detection(self):
        self._value = self._input.value()
        if (
            self._when_motion_is_detected and
            self._value == 1
        ):
            self._when_motion_is_detected()

        (print(self._value) if self._show_value else None)
        sleep(0.2)
        return self._value

class NextionDisplay:
    '''
        display = NextionDisplay(tx=4, rx=5)
        display.write("temp.txt='34 C'")
    '''
    def __init__(
        self,
        uart_number:int,
        tx:int,
        rx:int,
        bits:int=8,
        baudrate:int=9600,
        parity=None,
        stop:int=1
    )->None:
        self._bits = bits
        self._uart = UART(uart_number, baudrate=baudrate, tx=Pin(tx), rx=Pin(rx))
        self._uart.init(bits=bits, parity=parity, stop=stop)
    
    def _process_buffer(self, buffer, only_page_element, format_return):
        if only_page_element and format_return == 'dict':
            return {'component': buffer[2], 'page': buffer[1]}
        return list((buffer)[2:4] if only_page_element else (buffer)[1:])

    def read(
        self,
        page_and_component:bool=False,
        format_return:str='list'
    ):
        _buffer = self._uart.read()

        if _buffer and len(list(_buffer)) == self._bits - 1:
            #page and component
            return self._process_buffer(
                buffer=_buffer,
                only_page_element=page_and_component,
                format_return=format_return
            )
        if _buffer and len(list(_buffer)) == 4:
            #slider
            return list(_buffer)[0]
        return _buffer
    
    def write(self, command:str):
        _command = bytes(str(command), 'UTF-8')
        _base_command = b'\xff\xff\xff'
        _buffer_to_send = _command + _base_command
        self._uart.write(bytearray(_buffer_to_send))

class ClockDS1307:
    def __init__(
        self,
        i2c_number:int,
        pin_scl:int,
        pin_sda:int,
        freq=400000,
        auto_config:bool=False
    )->None:
        self._i2c = I2C(i2c_number, scl=Pin(pin_scl), sda=Pin(pin_sda), freq=freq)
        try:
            self._rtc = DS1307(self._i2c)
            self._now = self._config(auto_config)
            self._rtc.datetime(self._now)
        except (ValueError, ImportError) as e:
            print(e)
        
    def _config(self, auto_config:bool)->tuple:
        year = int(input("Year : "))
        month = int(input("month (Jan --> 1 , Dec --> 12): "))
        date = int(input("date : "))
        day = int(input("day (1 --> monday , 2 --> Tuesday ... 0 --> Sunday): "))
        hour = int(input("hour (24 Hour format): "))
        minute = int(input("minute : "))
        second = int(input("second : "))
        return (year, month, date, day, hour, minute,second, 0)
    
    def read_datetime(self, format_return:str='tuple')->tuple:
        if format_return != 'tuple':
            (year,month,date,day,hour,minute,second,p1) = self._rtc.datetime()
            try:
                formats = {
                    'str': f'{year}-{month}-{date}|{hour}:{minute}:{second}',
                    'mapping': {
                        'year': year,
                        'month': month,
                        'date': date,
                        'day': day,
                        'hour': hour,
                        'minute': minute,
                        'second': second
                    }
                }
                return formats[format_return]
            except KeyError:
                return self._rtc.datetime()
        return self._rtc.datetime()
