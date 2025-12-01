#py -3.9 -m venv venv




from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait


hub = PrimeHub()

sensor_color = ColorSensor(Port.B)
motor_posicion = Motor(Port.A)
motor_empuje = Motor(Port.D)

while True:
    color_detectado = sensor_color.color()

    if color_detectado == Color.RED or color_detectado == Color.YELLOW:


        motor_posicion.run_target(1000, -35)
        if color_detectado == Color.RED:
        
            motor_empuje.run_angle(1000, -180)

        elif color_detectado == Color.YELLOW:
            motor_empuje.run_angle(1000, 180)
    

    elif color_detectado == Color.GREEN or color_detectado == Color.BLUE:

        motor_posicion.run_target(1000, 35)
        if color_detectado == Color.GREEN:
            motor_empuje.run_angle(1000, 180)

        elif color_detectado == Color.BLUE:
            motor_empuje.run_angle(1000, -180)

    wait(10)




#pybricksdev run ble my_program.py
#pybricksdev devices