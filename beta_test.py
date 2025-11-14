from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
import ubluetooth


hub = PrimeHub()

ble=bluetooth.BLE()
ble.activate(True)
ble_uart = ubluetooth.BLEUART(ble, name="sp1")
sensor_color = ColorSensor(Port.B)
motor_posicion = Motor(Port.A)
motor_empuje = Motor(Port.D)

def on_rx(rx):
    cmd=rx.decode()
    color_detectado = sensor_color.color()

    if cmd=="w":
        motor_posicion.run_target(1000, -35)
        motor_empuje.run_angle(1000, -180)
    elif cmd=="s":
        motor_posicion.run_target(1000, -35)
        motor_empuje.run_angle(1000, 180)
    elif cmd=="a":
        motor_posicion.run_target(1000, 35)
        motor_empuje.run_angle(1000, -180)
    elif cmd=="d":
        motor_posicion.run_target(1000, 35)
        motor_empuje.run_angle(1000, 180)
    ble_uart.on_write(on_rx)

while True:
    wait(10)
