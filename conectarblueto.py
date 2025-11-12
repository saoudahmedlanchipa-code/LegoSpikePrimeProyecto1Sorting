import pygame
import asyncio
from bleak import BleakClient
# (Ya no necesitamos nest_asyncio)

# --- Configuración BLE ---
ADDRESS = "38:4B:51:09:2A:7D" 
PYBRICKS_UART_CHAR_UUID = "c5f50002-8280-46f4-bcfc-e45ae33e38f9"

async def main(address):
    
    # --- Inicia Pygame DENTRO de la función async ---
    print("Iniciando Pygame...")
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("Error: No se encontró ningún mando.")
        print("Asegúrate de que esté bien conectado y vuelve a intentarlo.")
        exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Mando conectado: {joystick.get_name()}")

    # Estados para evitar enviar comandos repetidos
    x_presionado = False
    o_presionado = False
    
    print(f"Buscando Hub en {address}...")
    
    try:
        async with BleakClient(address) as client:
            print(f"¡Conectado al Hub en {address}!")
            
            while True:
                # Requerido para que pygame procese eventos
                pygame.event.pump() 

                # --- Lógica del botón X (START) ---
                if joystick.get_button(0) and not x_presionado:
                    print("Enviando comando START...")
                    await client.write_gatt_char(PYBRICKS_UART_CHAR_UUID, b"START\n")
                    x_presionado = True
                elif not joystick.get_button(0):
                    x_presionado = False

                # --- Lógica del botón O (STOP) ---
                if joystick.get_button(1) and not o_presionado:
                    print("Enviando comando STOP...")
                    await client.write_gatt_char(PYBRICKS_UART_CHAR_UUID, b"STOP\n")
                    o_presionado = True
                elif not joystick.get_button(1):
                    o_presionado = False
                
                # Pausa para no saturar el bucle
                await asyncio.sleep(0.05) 
                
    except Exception as e:
        print(f"Error al conectar o durante la ejecución: {e}")
        print("Asegúrate de que:")
        print("  1. El Hub esté encendido y ejecutando el script de Pybricks.")
        print("  2. La dirección MAC sea correcta.")
        print("  3. El Hub no esté conectado a otro dispositivo (como tu celular).")


# --- Ejecutar el programa ---
if __name__ == "__main__":
    
    # --- ESTE ES EL NUEVO PARCHE ---
    # Forzamos a asyncio a usar una política de bucle de eventos
    # diferente (SelectorEventLoop) que no entra en conflicto con
    # el hilo GUI de Windows que pygame activa.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main(ADDRESS))