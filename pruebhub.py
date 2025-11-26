from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait
from usys import stdin, stdout

hub = PrimeHub()

# Motores
motor_pos = Motor(Port.A)     # Motor de posición
motor_push = Motor(Port.D)    # Motor de empuje

# Sensor de color
sensor = ColorSensor(Port.B)

# Enviar texto por BLE
def ble_send(text):
    try:
        stdout.buffer.write((text + "\n").encode())
        stdout.buffer.flush()
    except:
        pass

# Enviar el color actual
def send_color():
    c = sensor.color()
    if c == Color.RED:
        ble_send("red")
    elif c == Color.YELLOW:
        ble_send("yellow")
    elif c == Color.GREEN:
        ble_send("green")
    elif c == Color.BLUE:
        ble_send("blue")
    else:
        ble_send("none")

# Posiciones iguales a tu sorter original
LEFT_POS = -35
RIGHT_POS = 35

# Empujes iguales
PUSH_LEFT = -180
PUSH_RIGHT = 180

# COMIENZA EL CONTROL MANUAL
ble_send("ready")

while True:
    # Detectar color continuamente
    send_color()

    # Leer comandos desde la app
    if stdin.buffer.any():
        raw = stdin.buffer.readline().decode().strip()
        cmd = raw.lower()

        # Debug opcional en consola Pybricks
        print("CMD:", cmd)

        # --- MOTOR DE POSICIÓN ---
        if cmd == "pos_left":
            motor_pos.run_target(800, LEFT_POS)

        elif cmd == "pos_right":
            motor_pos.run_target(800, RIGHT_POS)

        elif cmd == "pos_stop":
            motor_pos.stop()

        # --- MOTOR DE EMPUJE ---
        elif cmd == "l1":
            motor_push.run_angle(1000, PUSH_LEFT)

        elif cmd == "r1":
            motor_push.run_angle(1000, PUSH_RIGHT)

    wait(20)
