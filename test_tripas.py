from pybricksdev.connections.pybricks import PybricksHub
import inspect

print("--- INFORME DE AUTOPSIA ---")
# 1. ¿De dónde viene el archivo realmente?
archivo = inspect.getfile(PybricksHub)
print(f"Ubicación: {archivo}")

# 2. ¿Qué código tiene la función connect?
codigo = inspect.getsource(PybricksHub.connect)
print("\nCódigo fuente de 'connect':")
print(codigo)
print("---------------------------")