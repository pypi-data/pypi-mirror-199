import neopixel
from umachine import Pin, PWM
from utime import sleep
from gpiopico.utils import AnalogicMap, hex_to_rgb

_SAMPLES: int = 65534


class SimpleDigitalControl:
    """
        :pin(int)
        :inverted_logic(bool)
        
        led = SimpleDigitalControl(2, inverted_logic=True)
        print('ON')
        led.change_state(True)
        sleep(2)
        print('OFF')
        led.change_state(False)
        sleep(2)

    """
    def __init__(self, pin: int, inverted_logic:bool = False):
        self._inverted_logic = inverted_logic
        self._state = True if inverted_logic else False
        self._pin = Pin(pin, Pin.OUT)

    @property
    def state(self):
        return self._state

    def change_state(self, state:bool):
        self._state = (
            state if self._inverted_logic else not(state)
        )
        self._pin.value(self._state)
    
    def on(self):
        self._pin.value(
           0 if self._inverted_logic else 1
        )
    
    def off(self):
        self._pin.value(
           1 if self._inverted_logic else 0
        )

class FullDigitalControl:
    """
        :pin(int)
        :inverted_logic(bool)
        :use_mapping(bool)
        
        led = FullDigitalControl(2, inverted_logic=True)
        led = Led(2, True)
        led.on()
        sleep(2)
        led.off()
        sleep(2)
        led.pwm_value(125)
        sleep(2)
    """
    def __init__(
        self,
        pin: int,
        inverted_logic: bool=False,
        limit_range:int=255,
        use_mapping: bool=True
    ) -> None:
        self._inverted_logic = inverted_logic
        self._pin = PWM(Pin(pin))
        self._pwm_value = 0
        self._use_mapping = use_mapping
        self._mapping = AnalogicMap()
        self._range_map = (_SAMPLES, 0) if inverted_logic else (0, _SAMPLES)
        self._limit_range =  limit_range

    @property
    def pwm_value(self):
        return self._pwm_value

    def pwm_value(self, pwm_value: int, limit_range=None) -> None:
        if self._use_mapping:
            _pwm_value = (
                self._mapping.create_map(
                    pwm_value,
                    0,
                    limit_range if limit_range else self._limit_range,
                    self._range_map[0],
                    self._range_map[1]
                )
            )
            _pwm_value = (
                _pwm_value if self._inverted_logic else _pwm_value
            )
            self._pwm_value = _pwm_value
            self._pin.duty_u16(_pwm_value)
        else:
            self._pwm_value = pwm_value
            self._pin.duty_u16(pwm_value)
    
    def on(self):
        self._pin.duty_u16(
           0 if self._inverted_logic else _SAMPLES
        )
    
    def off(self):
        self._pin.duty_u16(
           _SAMPLES if self._inverted_logic else 0
        )
            

class Relay(SimpleDigitalControl):
    def __init__(self, pin: int, inverted_logic: bool = False):
        super().__init__(pin, inverted_logic)

class Led(FullDigitalControl):
    def __init__(self, pin: int, inverted_logic: bool = False, limit_range:int=255):
        super().__init__(pin, inverted_logic, limit_range)

class SolidStateRelay(FullDigitalControl):
    def __init__(self, pin: int, inverted_logic: bool = False) -> None:
        super().__init__(pin, inverted_logic)

class Motor:
    """
        :pin_forward(int)
        :pin_backward(int)
        
        from gpiopico import Motor
        motor_a = Motor(0,1)
        motor_a.forward()
        sleep(2)
        motor_a.backward()
        sleep(2)
        motor_a.stop()
    """
    def __init__(self, pin_forward: int, pin_backward: int) -> None:
        self._pin_forward = FullDigitalControl(pin_forward)
        self._pin_backward = FullDigitalControl(pin_backward)
        self._limit_range = 100
        self.stop()
        
    def forward(self, velocity=None) -> None:
        """
            :velocity(int) 0% - 100%
        """
        if velocity:
            self._pin_forward.pwm_value(
                velocity if velocity <= 100 else 100,
                self._limit_range
            )
        self._pin_forward.on()
        self._pin_backward.off()
    
    def backward(self, velocity=None) -> None:
        """
            :velocity(int) 0% - 100%
        """
        if velocity:
            self._pin_backward.pwm_value(
                velocity if velocity <= 100 else 100,
                self._limit_range
            )
        self._pin_backward.on()
        self._pin_forward.off()
    
    def stop(self) -> None:
        self._pin_forward.off()
        self._pin_backward.off()
        sleep(0.5)

class Car:
    #TODO Create methods
    """Basic Car with two motors
    """
    def __init__(self, motor_a:tuple, motor_b:tuple) -> None:
        self._motor_a = Motor(motor_a[0], motor_a[1])
        self._motor_b = Motor(motor_b[0], motor_b[1])

class RGB:
    def __init__(
        self,
        pin_red:int,
        pin_green:int,
        pin_blue:int,
        limit_range:int=255,
        inverted_logic:bool=False,
    ) -> None:
        self._red = Led(pin=pin_red, inverted_logic=inverted_logic, limit_range=limit_range)
        self._green = Led(pin=pin_green, inverted_logic=inverted_logic, limit_range=limit_range)
        self._blue = Led(pin=pin_blue, inverted_logic=inverted_logic, limit_range=limit_range)

    def define_color(
        self,
        red:int=None,
        green:int=None,
        blue:int=None,
        color_hex:str=None
    ) -> None:
        if color_hex:
            red, green, blue = hex_to_rgb(color_hex)
        self._red.pwm_value(red)
        self._green.pwm_value(green)
        self._blue.pwm_value(blue)
    
    def off(self):
        self._red.off()
        self._green.off()
        self._blue.off()

class NeoPixel:
    '''
    # from gpiopico import NeoPixel
    # neo_pixel = NeoPixel(15, 8)
    # neo_pixel.write(['FF00FF','000000','FF00FF','000000','FF00FF','000000','FF05FF','000000'])
    '''
    def __init__(self, pin:int, lenght:int, matrix=[]) -> None:
        self._lenght = lenght
        self._pin = Pin(pin, Pin.OUT)
        self._n = neopixel.NeoPixel(self._pin, lenght)
        self._matrix = matrix
    
    def _create_base_matrix(self):
        return ['000000' for _ in range(self._lenght)]
    
    def _define_colors(self):
        for index, color in enumerate(self._matrix):
            self._n[index] = hex_to_rgb(color)
    
    def write(self, matrix=None):
        self._matrix = matrix if matrix else self._matrix
        if len(self._matrix) != self._lenght:
            raise ValueError('Matrix error')
        self._define_colors()
        self._n.write()
        
    def off(self):
        self._matrix = self._create_base_matrix()
        self._define_colors()
        self._n.write()
        
    def write_movement(
        self,
        matrix:str,
        wait:float=1.0,
        reverse:bool=False
    ) -> None:
        def _get_index(index) -> int:
            return -(index+1)

        for index, _ in enumerate(range(self._lenght)):
            _base = self._create_base_matrix()
            _base[_get_index(index) if reverse else index] = matrix
            self._matrix = _base
            self._define_colors()
            self._n.write()
            sleep(wait)
        self.off()
