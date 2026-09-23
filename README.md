# TP02_Grupo2
Controlador de misiones para el robot Unitree Go2 en Python, con gemelo digital en MuJoCo. TP02 de Programación I (UADE): instalación del entorno, bitácora de problemas y misiones.

# TP02 - Programación I - Grupo 2

Controlador de misiones para el robot Unitree Go2 en Python + MuJoCo.

## Integrantes
- Esteban Park 
- Mariangel Delgado
- Lucca Di Dello
- Sofia Gomez

## Estado inicial del entorno

| Elemento | Información obtenida |
|---|---|
| Sistema operativo | Microsoft Windows 11 Pro |
| Versión del SO | 10.0.26200 |
| Arquitectura | 64 bits |
| Python instalado | Sí |
| Versión de Python | 3.14.4 (py -3 y python dan la misma versión) |
| pip disponible | Sí, pip 26.0.1 (en Python 3.14) |
| Git disponible | Sí, git 2.55.0 |
| MuJoCo previamente instalado | No (ModuleNotFoundError al importarlo) |
| IDE utilizado | Visual Studio Code |
| Observaciones | El Escritorio está en C:\Users\Administrator\.vscode\Desktop, no en la ruta estándar. Python 3.14 es una versión reciente, puede haber problemas de compatibilidad con MuJoCo. |
## Arquitectura del laboratorio

mi_tp02.py
   |
   | robot.avanzar(...) / robot.girar(...) / robot.detenerse() / robot.saludar()
   v
robot.py  (puente, no se modifica)
   |
   | socket local 127.0.0.1:8765
   v
Simulador: MuJoCo + modelo Unitree Go2

Nuestro programa no habla directo con el simulador. Llama a funciones de robot.py, que es el puente. robot.py revisa que no nos pasemos de los límites de la materia (0.2 m/s, 0.5 rad/s, 10 s por orden) y si nos pasamos tira un ErrorDeSeguridad. Si está todo bien, manda la orden por un socket local (127.0.0.1, puerto 8765) al simulador, que la ejecuta en el Go2. Lo vimos en la terminal del simulador: "[LOCAL] Escuchando en 127.0.0.1:8765".

## Diseño Top-Down

Problema: hacer que el robot ejecute cualquier misión (una lista de comandos) sin reescribir el código.

main()
├── robot.conectar()
├── ejecutar_mision(robot, mision, historial)
│   └── por cada comando de la misión:
│       ├── comando_es_valido(comando)
│       │   └── motivo_rechazo(comando)
│       └── ejecutar_comando(robot, comando)   (solo si es válido)
│           └── robot.avanzar / girar / saludar / detenerse
│               (con try/except por si el robot tira ErrorDeSeguridad)
├── generar_reporte(historial)
└── robot.desconectar()

| Función | Recibe | Devuelve | Qué hace |
|---|---|---|---|
| motivo_rechazo | un comando (tupla) | texto con el motivo, o "" si está bien | revisa formato: nombre, cantidad de datos, que sean números, tiempo no negativo |
| comando_es_valido | un comando | True / False | usa motivo_rechazo |
| ejecutar_comando | robot, comando | texto con lo que pasó | llama a la orden del robot y atrapa ErrorDeSeguridad |
| ejecutar_mision | robot, misión, historial | nada | recorre la misión, valida, ejecuta y va guardando en historial |
| generar_reporte | historial | nada (imprime) | cuenta ejecutados y rechazados y muestra los motivos |

La validación tiene dos capas: nuestra función atrapa los comandos mal armados y el robot atrapa los valores que se pasan de los límites.

historial es una lista y se pasa por referencia: ejecutar_mision le agrega cosas adentro y no hace falta devolverla. En cambio velocidad y tiempo son números y se pasan por valor.
## Nivel máximo alcanzado
