import asyncio
from bleak import BleakScanner

async def main():
    print("Buscando dispositivos Bluetooth...")
    print("Asegúrate de que tu Hub esté encendido y parpadeando.")

    # Iniciar el escaneo
    devices = await BleakScanner.discover()

    print("\n--- Dispositivos Encontrados ---")
    hub_encontrado = False
    for device in devices:
        # Los hubs de Pybricks casi siempre tienen "Pybricks" o "LEGO" en el nombre
        if device.name and ("Pybricks" in device.name or "LEGO Hub" in device.name):
            print(f"\n¡POSIBLE HUB ENCONTRADO!")
            print(f"  Nombre: {device.name}")
            print(f"  Dirección (ADDRESS): {device.address} <--- ¡COPIA ESTA!")
            hub_encontrado = True

    if not hub_encontrado:
        print("\nNo se encontró un Hub de Pybricks.")
        print("Intenta de nuevo. Revisa que el Hub esté encendido.")

    print("-------------------------------")

# Ejecutar el scripte
asyncio.run(main())