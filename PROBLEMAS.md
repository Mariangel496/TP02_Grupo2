# Registro de problemas

## Problema N.º 1 - ModuleNotFoundError: No module named 'sim'
- Qué se estaba intentando hacer: ejecutar el controlador de misiones.
- Comando ejecutado: ejecutar mi_tp02.py desde una copia en el repo de entrega, junto con copias de robot.py y misiones.py.
- Resultado esperado: que el programa se conecte al simulador.
- Resultado obtenido: el programa no arrancó.
- Mensaje de error: `ModuleNotFoundError: No module named 'sim'` (robot.py, línea 15: `from sim.robot import EstadoRobot, NoHaySimulador, Robot`)
- Interpretación del grupo: el error no está en nuestro código sino en robot.py, que intenta importar un módulo que no encuentra.
- Hipótesis sobre la causa: robot.py no funciona solo, es un puente que depende de la carpeta entorno/sim de la cátedra. Al copiarlo a otra carpeta perdió esa referencia.
- Solución 1 intentada y resultado: ejecutar desde UadeRobotLab\05LaboratoriosTPs\TP02_Programacion_I con `py -3 mi_desarrollo\mi_tp02.py`. Funcionó.
- Estado final: Resuelto. Definimos que el código se desarrolla y ejecuta en UadeRobotLab, y en el repo de entrega solo va una copia final en codigo/tp02_grupo2.py.
- Evidencia: evidencias/03_errores.

## Problema N.º 2 - El código usaba los límites del TP en PDF y no los del repositorio
- Qué se estaba intentando hacer: integrar la primera versión del controlador que armó una compañera del grupo.
- Comando ejecutado: revisión del código y prueba de la validación contra MISION_CON_ERRORES y la misión propia.
- Resultado esperado: que la validación rechace solo los comandos que el robot no puede ejecutar.
- Resultado obtenido: el código tenía VELOCIDAD_MAX = 0.5, DISTANCIA_MAX = 5.0 y ANGULO_MAX = 180, sacados del PDF. Con esos valores, los comandos de la misión propia a 0.3 m/s pasaban nuestra validación, pero el robot los iba a rechazar.
- Mensaje de error: ninguno todavía. Lo detectamos al comparar las constantes con los límites que muestra el simulador al arrancar: "Limites: 0.2 m/s | 0.5 rad/s | 10.0 s por orden".
- Interpretación del grupo: se mezclaron las dos versiones del TP, cosa que el Orientador pide evitar.
- Hipótesis sobre la causa: el PDF expresa los comandos en distancia y ángulo (en grados) y tiene límites más altos. El repo actual usa velocidad y tiempo, y el ángulo se calcula en radianes. Por eso ANGULO_MAX = 180 comparado contra radianes nunca rechazaba nada.
- Solución 1 intentada y resultado: reemplazar las constantes por las del repo (VELOCIDAD_AVANCE_MAX = 0.2, VELOCIDAD_GIRO_MAX = 0.5, TIEMPO_MAX = 10.0) y rehacer la misión propia dentro de esos límites. Con eso, MISION_CON_ERRORES rechaza los 7 comandos inválidos, cada uno con su motivo.
- Estado final: Resuelto.
- Evidencia: codigo/tp02_grupo2.py y evidencias/06_misiones.

## Problema N.º 3 - INSTALACION.md indica la carpeta de otro TP
- Qué se estaba intentando hacer: verificar el entorno siguiendo el paso 4 de INSTALACION.md.
- Comando ejecutado: la guía indica `cd 05LaboratoriosTPs/TP01_Fundamentos_de_Informatica` y después `cd entorno && python3 -m sim --solo-revisar`.
- Resultado esperado: una guía con los pasos para el TP02.
- Resultado obtenido: la guía apunta a la carpeta del TP01, no a la del TP02. Además usa `python3`, que es el comando de Linux/macOS.
- Mensaje de error: ninguno, lo detectamos al leer la guía antes de ejecutar.
- Interpretación del grupo: INSTALACION.md es una guía compartida entre las materias (lo confirma PLAN_TP02.md: "guía de cero, compartida entre las 7 materias").
- Hipótesis sobre la causa: la guía se escribió para el TP01 y se reutilizó sin adaptar esa ruta.
- Solución 1 intentada y resultado: adaptar los comandos: `cd UadeRobotLab\05LaboratoriosTPs\TP02_Programacion_I\entorno` y `py -3 -m sim --solo-revisar`. Dio [OK] Python, [OK] MuJoCo, [OK] Modelos Unitree y "Todo listo".
- Estado final: Resuelto.
- Evidencia: evidencias/02_instalacion.

## Problema N.º 4 - Python 3.14, más nuevo que el probado por la cátedra
- Qué se estaba intentando hacer: confirmar que la versión de Python sirve para el laboratorio.
- Comando ejecutado: `py -3 --version`
- Resultado esperado: Python 3.10 o superior.
- Resultado obtenido: Python 3.14.4.
- Mensaje de error: ninguno.
- Interpretación del grupo: cumple el mínimo, pero la cátedra probó el paquete con Python 3.12.3 (según INSTALACION.md y PLAN_TP02.md). INSTALACION.md además cuenta que CycloneDDS dejó de usarse justamente porque no tenía versión para Python nuevos.
- Hipótesis sobre la causa: una versión muy nueva de Python puede no tener versión compilada de MuJoCo. En ese caso pip intentaría compilarlo y fallaría.
- Solución 1 intentada y resultado: instalar igual y revisar qué archivo baja pip. Descargó mujoco-3.14.0-cp314-cp314-win_amd64.whl. El "cp314" indica que es una versión hecha para Python 3.14, así que no hizo falta compilar. El import y la verificación del entorno dieron OK.
- Estado final: Resuelto. No hubo que cambiar de versión de Python.
- Evidencia: evidencias/01_entorno y 02_instalacion.

## Problema N.º 5 - Advertencias de PATH al instalar MuJoCo
- Qué se estaba intentando hacer: instalar MuJoCo según INSTALACION.md.
- Comando ejecutado: `py -3 -m pip install --user mujoco`
- Resultado esperado: instalación sin errores.
- Resultado obtenido: "Successfully installed mujoco-3.14.0", pero con advertencias en amarillo.
- Mensaje de error: `WARNING: The script websockets.exe is installed in '...\Python314\Scripts' which is not on PATH.` (lo mismo para f2py.exe y numpy-config.exe)
- Interpretación del grupo: no es un error. Como usamos --user, pip instaló algunos programas auxiliares en una carpeta que Windows no revisa al escribir comandos.
- Hipótesis sobre la causa: la opción --user que pide la guía instala en la carpeta del usuario (AppData\Roaming), que no está en el PATH.
- Solución 1 intentada y resultado: no modificar el PATH, porque nunca ejecutamos esos programas directamente: siempre usamos `py -3 -m ...`. Lo comprobamos con `py -3 -c "import mujoco; print(mujoco.__version__)"`, que dio 3.14.0.
- Estado final: Resuelto (advertencia analizada, no requiere acción).
- Evidencia: evidencias/02_instalacion.