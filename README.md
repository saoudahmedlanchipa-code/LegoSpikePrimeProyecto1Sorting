Manual de usuario

El manual de usuario no es necesario incluirlo en este documento, pero sí debe estar disponible en el repositorio de GitHub del proyecto.
Este manual debe presentarse como un archivo README.md, que incluya los siguientes elementos:

●	Nombre del proyecto:
Incluir el nombre del proyecto y una breve descripción que indique qué se hace y para quién está pensado.

		Ejemplo:

	Una herramienta CLI ligera que convierte archivos Markdown en HTML usando templates personalizables.

●	Características:
		Incluir una lista clara de las principales características o funcionalidades del sistema.

		Ejemplo: 
●	Convierte Markdown en HTML.
●	Soporta templates personalizables.
●	Modo watch para re-build automático.
●	Sin dependencias externas.

●	Instalación:

Describir los pasos necesarios para preparar el sistema antes de poder controlar el robot mediante la interfaz.

	Se recomienda generar un archivo ejecutable a partir del código y publicar una release en el repositorio de GitHub.
	
		Para la release es necesario indicar:

●	URL de descarga, por ejemplo: 		
https://github.com/username/project/releases

●	Sistema operativo compatible (es importante considerar el OS del usuario final).
●	Instrucciones de instalación del ejecutable, desde la descarga hasta la primera ejecución para controlar el robot.

	Si no se provee un ejecutable, incluya los pasos para instalar y ejecutar el proyecto desde el código fuente.
		





		Ejemplo: 

		git clone https://github.com/username/project.git
		cd project
		python3 client.py
		python3 server.py


●	Uso básico:

	Describir paso a paso cómo realizar cada una de las acciones mencionadas en la sección de características.

		Ejemplo:

●	Convertir markdown en HTML:

			./project input.md -o output.html


●	Usar un template personalizado

./project input.md --template template.html
		

●	Capturas
		
		Incluir capturas de pantalla de la interfaz del sistema y/o una demostración en formato GIF

