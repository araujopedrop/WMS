# WMS


Para compilar:
- Descargar todo en una carpeta
- Tener instalado pyinstaller (para generar el ejecutable)
- Desde un cmd, moverse hasta la carpeta con los archivos y tipear: pyinstaller --onefile --windowed WMS.py (esto generera algunas carpetas y archivos mas)
- Se habra creado una carpeta que se llama "dist". Adentro deberia estar el WMS.exe. Cortar ese .exe y moverlo afuera, con los demas archivos. 
- Ejecutar el .exe y listo
- A la tarde subo el ejecutable a un drive por las dudas


Funcionalidades listas hasta el 17/01/2022:
- Envio de json a traves de websocket
- Configuracion de websocket desde el boton configuracion (boton Engranaje)

Funcionalidades en curso:
- Conexion con base de datos
- Mostrar por pantalla estado de warehouse
- Recibir datos para actualizar estado de warehouse
- Agregar productos al warehouse por boton "Agregar producto"

