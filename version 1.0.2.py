# este codigo lee la entrada del teclado para controlar el robot
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
from usys import stdin
from uselect import poll


hub = PrimeHub()

sensor_color = ColorSensor(Port.B)
motor_posicion = Motor(Port.A)
motor_empuje = Motor(Port.D)

teclado = poll()
teclado.register(stdin)

while True:
    if teclado.poll(0):
        key = stdin.read(1)
        if key=='w':
            motor_posicion.run_target(1000, -35)
            motor_empuje.run_angle(1000, -180)

        elif key == 'a':
            motor_posicion.run_target(1000, -35)
            motor_empuje.run_angle(1000, 180)
        elif key=='s':
            motor_posicion.run_target(1000, 35)
            motor_empuje.run_angle(1000, 180)

        elif key=='d':
            motor_posicion.run_target(1000, 35)
            motor_empuje.run_angle(1000, -180)

    wait(10)
