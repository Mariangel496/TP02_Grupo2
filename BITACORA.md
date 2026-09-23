# Bitácora técnica - TP02

## Análisis previo de la documentación

**a) ¿Qué herramientas necesita el TP?**
- Python 3.10 o superior
- MuJoCo (se instala con pip), que es la ventana 3D del simulador
- Visual C++ Redistributable (solo en Windows, sin esto MuJoCo no carga)
- Los modelos del G1 y el Go2 (ya vienen dentro de la carpeta del TP, en entorno/sim/unitree_mujoco)
- Git para bajar el repo y un editor (usamos VS Code)

**b) ¿Qué versión de Python se requiere?**
Python 3.10 o superior. Nosotros tenemos 3.14.4. La guía muestra de ejemplo 3.12.3, así que 3.14 es más nueva que la que probaron ellos.

**c) ¿Qué componentes ya están instalados en la computadora?**
Python 3.14.4, pip 26.0.1, Git 2.55.0 y VS Code. MuJoCo no estaba instalado (dio ModuleNotFoundError). Falta verificar el Visual C++ Redistributable.

**d) ¿Qué componentes del repositorio oficial de Unitree no son necesarios?**
- CycloneDDS: solo tiene paquetes hasta Python 3.10, con versiones más nuevas falla ("Could not locate cyclonedds")
- El SDK oficial unitree_sdk2_python: usa funciones que solo existen en Linux
- El repo completo unitree_mujoco (299 MB): el TP ya trae recortados solo los modelos del G1 y el Go2
El simulador ahora se comunica por un socket local (127.0.0.1) y no necesita nada de eso.

**e) ¿Qué diferencias observan entre el TP en PDF y la versión actual del repositorio?**
- La API cambió: antes era avanzar(distancia, velocidad) y girar(angulo, sentido). Ahora todo es velocidad y tiempo: avanzar(velocidad, tiempo) y girar(velocidad, tiempo). La distancia y el ángulo se calculan (velocidad × tiempo).
- En girar el sentido lo da el signo: positivo es izquierda, negativo es derecha. Un giro con velocidad negativa ya no es inválido.
- Las funciones cambiaron: antes eran inicializar_robot y procesar_comando, ahora son comando_es_valido, ejecutar_comando, ejecutar_mision y generar_reporte.
- Los límites son más bajos: 0.20 m/s, 0.50 rad/s y 10 s por orden (el PDF decía VELOCIDAD_MAX = 0.5).
- Antes se usaba unitree_sdk_sim.py (solo logs), ahora es MuJoCo con el robot en 3D y robot.py como puente.
- La validación ahora tiene dos capas: la nuestra (comando_es_valido) y la del robot, que tira ErrorDeSeguridad si un valor se pasa del límite. Hay que usar try/except para que la misión no se corte.
- El archivo base ya no es tp02_plantilla.py sino mi_desarrollo/mi_tp02.py, y las misiones están en misiones.py.
- Algo raro que encontramos: en INSTALACION.md el paso 4 dice de entrar a la carpeta TP01_Fundamentos_de_Informatica, no a la del TP02. Parece que la guía es compartida entre materias.

| Nº | Fecha | Acción / comando | Resultado | Problema | Solución intentada | Estado |
|----|-------|------------------|-----------|----------|--------------------|--------|
| 1 | 23/09 | `cd %USERPROFILE%\Desktop` | No encuentra la ruta | El Escritorio está en `C:\Users\Administrator\.vscode\Desktop`, no en la ruta estándar | Probé `OneDrive\Escritorio` (falló). Abrí cmd desde la barra del Explorador | RESUELTO |
| 2 | 23/09 | `git clone https://github.com/Mariangel496/TP02_Grupo2.git` | Repo clonado OK | - | - | RESUELTO |
| 3 | 23/09 | `git push` | Pidió iniciar sesión en GitHub | Primera vez que se sube desde esta PC | Sign in with your browser, autoricé con mi cuenta | RESUELTO |
| 4 | 23/09 | `for /d %d in (evidencias\*) do ...` | No creó los .gitkeep | El comando es de cmd y la terminal era PowerShell | Usé el equivalente en PowerShell (Get-ChildItem ... New-Item) | RESUELTO |
| 5 | 23/09 | `git push` + otro comando en la misma línea | `error: unknown switch 'D'` | Pegué dos comandos juntos sin apretar Enter | Ejecuté un comando por vez | RESUELTO |
| 6 | 23/09 | Comando .gitkeep desde terminal de VS Code | No encontraba la carpeta | La terminal estaba dentro de `evidencias` | `cd ..` para subir a la raíz del repo | RESUELTO |
| 7 | 23/09 | `Get-CimInstance Win32_OperatingSystem` | Windows 11 Pro 10.0.26200 64 bits | - | - | RESUELTO |
| 8 | 23/09 | `py -3 --version` / `python --version` | Python 3.14.4 en ambos | - | - | RESUELTO |
| 9 | 23/09 | `py -3 -m pip --version` | pip 26.0.1 | - | - | RESUELTO |
| 10 | 23/09 | `git --version` | git 2.55.0 | - | - | RESUELTO |
| 11 | 23/09 | `py -3 -c "import mujoco..."` | ModuleNotFoundError | MuJoCo no instalado (esperado) | Se instala en Etapa 3 | PENDIENTE |
| 12 | 23/09 | `git clone https://github.com/tsamaan/UadeRobotLab.git` | Repo clonado (838 archivos, 135 MB) en el Escritorio | - | - | RESUELTO |
| 13 | 23/09 | `dir UadeRobotLab\05LaboratoriosTPs\TP02_Programacion_I` | Carpeta con INSTALACION.md, LEEME_ESTUDIANTE.md, lanzadores y mi_desarrollo | - | - | RESUELTO |
| 14 | 23/09 | `Test-Path` de las 3 DLL de Visual C++ | True, True, True | - | Ya estaba instalado, no hace falta descargarlo | RESUELTO |
| 15 | 23/09 | `py -3 -m pip install --user mujoco` | Successfully installed mujoco-3.14.0 (con numpy, glfw, pyopengl, etc.) | Warnings: scripts instalados en una carpeta que no está en el PATH. Aviso de pip nuevo | No hace falta: no usamos esos .exe directamente, usamos py -3 -m. No actualizamos pip para no cambiar el entorno | RESUELTO |
| 16 | 23/09 | `py -3 -c "import mujoco; print(mujoco.__version__)"` | 3.14.0 | - | - | RESUELTO |
| 17 | 23/09 | `py -3 -m sim --solo-revisar` (desde entorno/) | [OK] Python 3.14.4, [OK] MuJoCo v3.14.0, [OK] Modelos Unitree. Todo listo | - | - | RESUELTO |
| 18 | 23/09 | `.\INICIAR_SIMULADOR.bat` → opción 2 (Go2) | Se abrió la ventana de MuJoCo con el Go2 visible | - | - | RESUELTO |
| 19 | 23/09 | `py -3 mi_desarrollo\mi_tp02.py` (plantilla sin modificar, en otra terminal) | [OK] Conectado a Unitree Go2 y [OK] Desconectado. El robot no se mueve | - | Esperado: las 4 funciones están vacías | RESUELTO |
| 20 | 23/09 | Ejecutar mi_tp02.py desde la carpeta del repo | `ModuleNotFoundError: No module named 'sim'` en robot.py línea 15 | robot.py necesita la carpeta entorno/sim, que solo está en UadeRobotLab | Ejecutar siempre desde UadeRobotLab\...\TP02_Programacion_I. El repo es solo para la entrega | RESUELTO |
| 21 | 23/09 | Ejecutar controlador con MISION_BASICA | 4 ejecutados, 0 rechazados, 0.8 m recorridos. El Go2 avanzó, giró a la derecha y volvió a avanzar | - | - | RESUELTO |
| 22 | 23/09 | Ejecutar controlador con MISION_CON_ERRORES | 4 ejecutados, 7 rechazados con su motivo. La misión no se cortó | - | - | RESUELTO |
| 23 | 23/09 | Ejecutar controlador con MISION_CUADRADO | 9 ejecutados, 1.6 m. El robot volvió al punto de partida | - | Reiniciamos el simulador antes para que arranque desde el origen | RESUELTO |
| 24 | 23/09 | Ejecutar controlador con MISION_PROPIA | 6 ejecutados, 2 rechazados (tiempo de 12 s y comando "correr") | - | - | RESUELTO |