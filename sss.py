import shutil
import os
import time

# Esta es la ruta exacta que apareció en tu error
ruta_maldita = r"C:\Users\saoud\AppData\Local\Programs\Python\Python312\Lib\site-packages\pybricksdev"

print(f"Buscando la carpeta corrupta en:\n{ruta_maldita}")

if os.path.exists(ruta_maldita):
    try:
        shutil.rmtree(ruta_maldita)
        print("\n✅ ¡ÉXITO! Carpeta corrupta eliminada correctamente.")
        print("Ahora tu Python está limpio.")
    except Exception as e:
        print(f"\n❌ ERROR: No pude borrarla por permisos. Cierra todo y prueba de nuevo.")
        print(f"Detalle: {e}")
else:
    print("\n⚠️ Ojo: La carpeta ya no existe. Quizás ya se borró.")