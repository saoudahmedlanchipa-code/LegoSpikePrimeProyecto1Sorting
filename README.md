# Sistema de Clasificación por Color con LEGO Spike

Este proyecto permite controlar un robot LEGO Spike Prime mediante una interfaz gráfica en Python,
capaz de operar en modo manual y automático para clasificar objetos según su color.
Está pensado para estudiantes de ingeniería y cursos de robótica educativa.




## Características

- Interfaz gráfica desarrollada con Tkinter.
- Conexión Bluetooth BLE con LEGO Spike Prime.
- Control manual por botones de colores.
- Control manual mediante teclado (flechas).
- Modo automático con detección de color.
- Indicador visual del color detectado.
- Panel de estado de conexión (conectado / desconectado).
- Registro de eventos y acciones.



## Sistemas operativos
- Windows 10 / 11 (64 bits)


## Instalación desde el código fuente

1. Clonar el repositorio:

   git clone https://github.com/tuusuario/nombre-del-proyecto.git

2. Entrar al directorio:

   cd nombre-del-proyecto

3. Instalar dependencias:

   pip install pybricksdev

4. Ejecutar el programa:

   python main.py



## Uso básico

### Conectar el robot

![WhatsApp Image 2025-12-29 at 10 57 43 AM](https://github.com/user-attachments/assets/fabc0030-30d4-48d7-81b6-21fa767ff3f7)

1. Encender el LEGO Spike Prime.
2. Ejecutar la aplicación.
3. Presionar el botón "Conectar".
4. El panel de estado se pondrá de color verde.




### Modo manual por colores

- Presionar los botones ROJO, AMARILLO, VERDE o AZUL para ejecutar el movimiento correspondiente.

### Control por teclado

- Flecha arriba: motor de empuje +180°.
- Flecha abajo: motor de empuje -180°.
- Flecha derecha: motor de posición +35°.
- Flecha izquierda: motor de posición -35°.

### Modo automático

1. Presionar el botón "Modo Automático".
2. El robot detectará colores automáticamente.
3. Para detenerlo, presionar el botón STOP.











