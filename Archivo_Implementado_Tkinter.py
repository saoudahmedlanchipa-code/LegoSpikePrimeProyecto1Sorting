import asyncio
import threading
import tempfile
import os
from queue import Queue, Empty
import tkinter as tk
from tkinter import ttk

from pybricksdev.ble import find_device
from pybricksdev.connections.pybricks import PybricksHubBLE


# ==================================================
# PROGRAMA PYBRICKS
# ==================================================

def create_program(cmd: str) -> str:

    base = """
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait

hub = PrimeHub()
motor_pos = Motor(Port.D)
motor_emp = Motor(Port.A)
sensor = ColorSensor(Port.B)
"""

    if cmd == "auto":
        return base + """
print("MODO AUTOMATICO INICIADO")

while True:
    color = sensor.color()

    if color == Color.RED:
        print("COLOR:RED")
        motor_pos.run_target(300, -35)
        motor_emp.run_angle(1000, -180)

    elif color == Color.YELLOW:
        print("COLOR:YELLOW")
        motor_pos.run_target(300, -35)
        motor_emp.run_angle(1000, 180)

    elif color == Color.GREEN:
        print("COLOR:GREEN")
        motor_pos.run_target(300, 35)
        motor_emp.run_angle(1000, 180)

    elif color == Color.BLUE:
        print("COLOR:BLUE")
        motor_pos.run_target(300, 35)
        motor_emp.run_angle(1000, -180)

    wait(200)
"""

    commands = {
        "red": "print('COLOR:RED'); motor_pos.run_target(300,-35); motor_emp.run_angle(1000,-180)",
        "yellow": "print('COLOR:YELLOW'); motor_pos.run_target(300,-35); motor_emp.run_angle(1000,180)",
        "green": "print('COLOR:GREEN'); motor_pos.run_target(300,35); motor_emp.run_angle(1000,180)",
        "blue": "print('COLOR:BLUE'); motor_pos.run_target(300,35); motor_emp.run_angle(1000,-180)",
        "emp_up": "motor_emp.run_angle(1000,180)",
        "emp_down": "motor_emp.run_angle(1000,-180)",
        "pos_right": "motor_pos.run_target(300,35)",
        "pos_left": "motor_pos.run_target(300,-35)",
    }

    if cmd in commands:
        return base + commands[cmd] + "\nwait(100)"

    if cmd == "stop":
        return """
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
Motor(Port.D).stop()
Motor(Port.A).stop()
"""

    return ""


async def execute(hub, cmd, log):
    program = create_program(cmd)

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(program)
        path = f.name

    try:
        await hub.run(path, wait=False)
        log(f"Ejecutado: {cmd}")
    except Exception as e:
        log(f"Error: {e}")
    finally:
        os.remove(path)


# ==================================================
# BLE WORKER
# ==================================================

class BLEWorker:
    def __init__(self, log_queue, status_cb):
        self.loop = asyncio.new_event_loop()
        self.queue = asyncio.Queue()
        self.log_queue = log_queue
        self.status_cb = status_cb
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.hub = None

    def log(self, msg):
        self.log_queue.put(msg)

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()

    def send(self, cmd):
        self.loop.call_soon_threadsafe(self.queue.put_nowait, cmd)

    def _run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.main())

    async def main(self):
        self.log("Buscando Hub Bluetooth...")
        device = await find_device("SP----1")

        if not device:
            self.log("No se encontró el Hub")
            self.status_cb(False)
            return

        self.hub = PybricksHubBLE(device)
        await self.hub.connect()
        self.log("Conectado al Hub")
        self.status_cb(True)

        while True:
            cmd = await self.queue.get()
            await execute(self.hub, cmd, self.log)


# ==================================================
# GUI
# ==================================================

class App:
    def __init__(self, root):
        self.root = root
        root.title("Control LEGO – Proyecto Final")
        root.geometry("550x600")

        self.logs = Queue()
        self.worker = BLEWorker(self.logs, self.update_status)

        # -------- Estado conexión --------
        ttk.Label(root, text="Estado de conexión").pack()
        self.status_panel = tk.Canvas(root, width=40, height=40)
        self.status_panel.pack()
        self.status_circle = self.status_panel.create_oval(5, 5, 35, 35, fill="red")

        ttk.Button(root, text="Conectar", command=self.worker.start).pack(pady=5)

        # -------- Automático --------
        ttk.Button(root, text=" MODO AUTOMÁTICO",
                   command=lambda: self.worker.send("auto")).pack(pady=8)

        ttk.Button(root, text=" STOP",
                   command=lambda: self.worker.send("stop")).pack(pady=5)

        # -------- Colores --------
        frame = ttk.LabelFrame(root, text="Control manual por color")
        frame.pack(pady=10)

        ttk.Button(frame, text=" ROJO", command=lambda: self.send_color("red")).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text=" AMARILLO", command=lambda: self.send_color("yellow")).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text=" VERDE", command=lambda: self.send_color("green")).grid(row=1, column=0, padx=5)
        ttk.Button(frame, text=" AZUL", command=lambda: self.send_color("blue")).grid(row=1, column=1, padx=5)

        # -------- Indicador color --------
        ttk.Label(root, text="Color").pack()
        self.color_canvas = tk.Canvas(root, width=120, height=120)
        self.color_canvas.pack()
        self.color_circle = self.color_canvas.create_oval(20, 20, 100, 100, fill="gray")

        # -------- Logs --------
        ttk.Label(root, text="Registro").pack()
        self.text = tk.Text(root, height=8)
        self.text.pack(fill="both", expand=True, padx=10)

        # -------- Teclado --------
        root.bind("<Up>", lambda e: self.worker.send("emp_up"))
        root.bind("<Down>", lambda e: self.worker.send("emp_down"))
        root.bind("<Right>", lambda e: self.worker.send("pos_right"))
        root.bind("<Left>", lambda e: self.worker.send("pos_left"))

        self.update_logs()

    def update_status(self, connected):
        self.status_panel.itemconfig(
            self.status_circle,
            fill="green" if connected else "red"
        )

    def send_color(self, color):
        self.worker.send(color)
        self.update_color(color.upper())

    def update_color(self, color):
        colors = {
            "RED": "red",
            "YELLOW": "yellow",
            "GREEN": "green",
            "BLUE": "blue"
        }
        self.color_canvas.itemconfig(self.color_circle, fill=colors.get(color, "gray"))

    def update_logs(self):
        try:
            while True:
                msg = self.logs.get_nowait()
                self.text.insert("end", msg + "\n")
                self.text.see("end")

                if "COLOR:" in msg:
                    self.update_color(msg.split(":")[1])

        except Empty:
            pass

        self.root.after(200, self.update_logs)


# ==================================================
# MAIN
# ==================================================

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
