# Conclusiones

# Conclusiones

a- ¿Cuál fue la principal dificultad de instalación?
La instalación de MuJoCo fue rápida (un solo comando y el Visual C++ ya estaba), pero la mayor dificultad fue entender qué documentación seguir. Había un TP en PDF, un Orientador nuevo y la guía del repositorio, y no decían lo mismo. Además, INSTALACION.md es una guía compartida entre materias y en el paso de verificación apunta a la carpeta del TP01, así que hubo que adaptar los comandos al TP02 y a Windows (py -3 en lugar de python3).

b- ¿Qué error requirió mayor investigación?
El ModuleNotFoundError: No module named 'sim'. El error aparecía dentro de robot.py y no en nuestro código, así que al principio no era claro dónde estaba el problema. Leyendo la línea del error vimos que robot.py importa sim.robot, que está en la carpeta entorno de la cátedra, y entendimos que robot.py es un puente que no funciona fuera de esa carpeta.

c- ¿Qué solución resultó efectiva y por qué?
Separar los lugares de trabajo: el código se desarrolla y se ejecuta dentro de UadeRobotLab, donde están robot.py, misiones.py y el entorno del simulador, y en nuestro repositorio solo guardamos la copia final para entregar. Funcionó porque respeta cómo está armado el laboratorio, sin copiar ni modificar archivos de la cátedra.

d- ¿Qué intento no funcionó y qué aprendieron de él?
La primera versión del código usaba los límites del TP en PDF (VELOCIDAD_MAX = 0.5, ANGULO_MAX = 180 en grados). Con esos valores, comandos que el robot iba a rechazar pasaban nuestra validación, y el límite de ángulo nunca se cumplía porque el repositorio trabaja en radianes. Aprendimos a verificar los datos contra la versión vigente (el simulador muestra los límites reales al iniciar: 0.2 m/s, 0.5 rad/s y 10 s) y a no mezclar dos versiones de una consigna.

e- ¿Qué diferencia encontraron entre una guía antigua y la arquitectura actual?
La guía vieja usaba unitree_sdk_sim.py, que solo mostraba mensajes, y expresaba los comandos en distancia y ángulo con sentido ("izquierda"/"derecha"). Además, versiones anteriores pedían instalar CycloneDDS y el SDK oficial de Unitree. La arquitectura actual usa MuJoCo con el modelo oficial del Go2, se comunica por un socket local (127.0.0.1:8765) a través de robot.py y expresa todo en velocidad y tiempo: la distancia y el ángulo se calculan multiplicando, y en girar el signo indica el sentido. Tampoco hace falta CycloneDDS ni el SDK.

f- ¿Hasta qué nivel lograron avanzar?
Llegamos al nivel 10: el programa se conecta al simulador, ejecuta las misiones de la cátedra y una propia, rechaza los comandos inválidos sin cortar la misión y genera el reporte final con los motivos de cada rechazo.

g- Si tuvieran que continuar trabajando, ¿cuál sería el próximo paso?
Probar la misión propia en el Go2 real con supervisión del docente y comparar lo que hace el robot con el reporte del simulador, porque el simulador no patina ni tiene inercia. También nos gustaría leer las misiones desde un archivo de texto, para cambiarlas sin tocar el código.

