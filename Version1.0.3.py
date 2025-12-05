import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
from pybricksdev.connections.pybricks import PybricksHub
import pybricksdev
print(f"ESTOY USANDO ESTA LIBRERÍA: {pybricksdev.__file__}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Pybricks")
        self.root.geometry("300x200")

        self.hub = PybricksHub()
        self.loop = None
        self.bt_thread = None

        self.lbl_status = tk.Label(root, text="Estado: Desconectado", fg="red")
        self.lbl_status.pack(pady=20)

        self.btn_connect = tk.Button(root, text="Conectar", command=self.start_connection_thread)
        self.btn_connect.pack(pady=5)

        self.btn_disconnect = tk.Button(root, text="Desconectar", command=self.disconnect, state="disabled")
        self.btn_disconnect.pack(pady=5)

    def start_connection_thread(self):
        self.btn_connect.config(state="disabled", text="Buscando...")
        self.bt_thread = threading.Thread(target=self.run_async_loop, daemon=True)
        self.bt_thread.start()

    def run_async_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_hub())

    async def connect_hub(self):
        try:
            print("Iniciando búsqueda de dispositivo...")
            # En versiones nuevas, connect() no lleva argumentos para búsqueda automática
            await self.hub.connect()
            
            # Si pasa de aquí, es que conectó
            self.root.after(0, self.on_connect_success)
            
            # Mantener la conexión viva
            await self.hub.user_program_stopped.wait()

        except Exception as e:
            # CORRECCIÓN CLAVE: Convertimos el error a texto INMEDIATAMENTE
            error_msg = f"Error: {str(e)}"
            print(error_msg) # Verlo en consola también
            
            # Pasamos el texto (error_msg), NO la variable 'e'
            self.root.after(0, lambda: self.on_connect_fail(error_msg))

    def on_connect_success(self):
        self.lbl_status.config(text="Estado: Conectado", fg="green")
        self.btn_disconnect.config(state="normal")
        self.btn_connect.config(text="Conectado")
        messagebox.showinfo("Éxito", "Hub conectado correctamente")

    def on_connect_fail(self, error_msg):
        self.lbl_status.config(text="Desconectado", fg="red")
        self.btn_connect.config(state="normal", text="Conectar")
        messagebox.showerror("Error de Conexión", error_msg)

    def disconnect(self):
        if self.loop and self.hub:
            asyncio.run_coroutine_threadsafe(self.hub.disconnect(), self.loop)
            self.lbl_status.config(text="Estado: Desconectado", fg="red")
            self.btn_connect.config(state="normal", text="Conectar")
            self.btn_disconnect.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()