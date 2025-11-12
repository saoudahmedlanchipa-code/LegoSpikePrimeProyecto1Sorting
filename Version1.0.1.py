"""

Aca estoy intentando implementar el pygame con pybricks

"""



import pygame
import time



from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

Botones = {
    0:"X",
    1:"O",
    2:"[]",
    3:"T"
    }


hub = PrimeHub()

sensor_color = ColorSensor(Port.B)
motor_posicion = Motor(Port.A)
motor_empuje = Motor(Port.D)


estadobutton = {i:False for i in Botones}

while True:

    pygame.event.pump()
    for i in Botones:
        press = joystick.get_button(i)
        if press and not estadobutton[i]:
            if Botones[i] == "X":
                print("Se toco X")
        estadobutton[i] = press



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




