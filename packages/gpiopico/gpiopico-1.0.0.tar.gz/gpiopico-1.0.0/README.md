# GPIO CONTROL IN RASPBERRY PI PICO
## Hardware control

### Input Devices
- Touch Sensor
- Potenciometer
- Joystick
- PIR
- LM35
- Nextion Display
### Ouput Devices
- LED
- Relay
- Solid state relay
- Motor DC
- RGB
- Servo motor
### Descargar paquete
```
pip install gpiopico
```


### Blink
```python
from gpiopico import Led
from utime import sleep

if __name__=='__main__':
    led = Led(pin=0, inverted_logic=True)#common anode
    
    for _ in range(4):
        led.on()
        sleep(1)
        led.off()
        sleep(1)

    for pwm in range(256):
      led.pwm_value(pwm)#0-255
      sleep(0.2)

```
### Button
```python
from gpiopico import Led, Button
from utime import sleep

if __name__=='__main__':
    led = Led(pin=0, inverted_logic=True)#common anode
    button = Button(pin=1)
    
    button.when_pressed = led.on
    button.on_hold = led.off 
    
    while True:
        button.check_state()
```