import asyncio
from pybricksdev.connections import BLEConnection
from pynput import keyboard

hub_name="sp1"

async def main():
    conn=await
BLEConnection.connect(hub_name)
    print("conectado al spike")

    def on_press(key):
        try:
            k=key.char
            if k in ["w","a","s","d"]:

asyncio.run(conn.write(k.encode()))
        except:
            pass
    with
Keyboard.Listener(on_press=on_press)as
listener:
    listener.join()
    asyncio.run(main())
