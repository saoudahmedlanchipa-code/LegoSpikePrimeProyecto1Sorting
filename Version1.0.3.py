import asyncio
import tkinter as tk
from pybricksdev.connections import BLEPUPConnection
from pybricksdev.run import run_user_program

# ----------------------------------------------
# conectar por BLE al Spike Prime
# ----------------------------------------------
async def connect():
    global conn
    status_label.config(text="Conectando...")

    conn = BLEPUPConnection()
    await conn.connect()     # busca el hub automáticamente
    status_label.config(text="Conectado ✔")

# ----------------------------------------------
# enviar comando por pybricksdev
# puedes usar micropython o mensajes directos
# ----------------------------------------------
async def send_command(cmd):
    if not conn:
        status_label.config(text="No conectado")
        return

    await conn.write(cmd.encode())

# ----------------------------------------------
# funciones para botones
# ----------------------------------------------
def avanzar():
    asyncio.run(send_command("forward"))

def retroceder():
    asyncio.run(send_command("back"))

def izquierda():
    asyncio.run(send_command("left"))

def derecha():
    asyncio.run(send_command("right"))

# ----------------------------------------------
# interfaz Tkinter
# ----------------------------------------------
root = tk.Tk()
root.title("Control Spike Prime")
root.geometry("400x300")

status_label = tk.Label(root, text="Desconectado", font=("Arial", 16))
status_label.pack(pady=10)

btn_connect = tk.Button(root, text="Conectar", font=("Arial", 14),
                        command=lambda: asyncio.run(connect()))
btn_connect.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Button(frame, text="↑", font=("Arial", 20), width=5,
          command=avanzar).grid(row=0, column=1)
tk.Button(frame, text="←", font=("Arial", 20), width=5,
          command=izquierda).grid(row=1, column=0)
tk.Button(frame, text="→", font=("Arial", 20), width=5,
          command=derecha).grid(row=1, column=2)
tk.Button(frame, text="↓", font=("Arial", 20), width=5,
          command=retroceder).grid(row=2, column=1)

root.mainloop()
