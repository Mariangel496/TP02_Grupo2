# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  	Esteban Lucas Park Chae - Sofia Gomez Marquez - Lucca Di Lello - Mariangel Delgado Perez

#  Comision:     Programacion 1 - Miercoles - Noche
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  CONSTANTES
#  Son los limites de la materia (los mismos que usa robot.py).
#  Estan en mayuscula y no se modifican nunca durante el programa.
# =====================================================================
VELOCIDAD_AVANCE_MAX = 0.2      # m/s
VELOCIDAD_GIRO_MAX = 0.5        # rad/s
TIEMPO_MAX = 10.0               # segundos por orden

COMANDOS_VALIDOS = ("avanzar", "girar", "detenerse", "saludar")
COMANDOS_SIN_DATOS = ("detenerse", "saludar")


# =====================================================================
#  MISION PROPIA (8 comandos, 2 invalidos a proposito)
# =====================================================================
MISION_PROPIA = [
    ("avanzar", 0.2, 3.0),      # 0.2 x 3.0 = 0.6 metros
    ("girar", 0.5, 3.14),       # 0.5 x 3.14 = 1.57 rad = 90 grados a la izquierda
    ("avanzar", 0.15, 2.0),     # 0.3 metros
    ("saludar",),
    ("girar", -0.5, 1.57),      # 45 grados a la derecha
    ("avanzar", 0.2, 12.0),     # MAL: 12 segundos supera el tiempo maximo
    ("correr", 0.2, 1.0),       # MAL: ese comando no existe
    ("detenerse",),
]


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def obtener_motivo_rechazo(comando):
    """Revisa un comando y devuelve el motivo por el que es invalido.
    Si el comando esta bien, devuelve un texto vacio ("")."""
    if type(comando) != tuple or len(comando) == 0:
        return "El comando no es una tupla o esta vacio"

    nombre = comando[0]

    if nombre not in COMANDOS_VALIDOS:
        return f"Comando desconocido: '{nombre}'"

    if nombre in COMANDOS_SIN_DATOS:
        if len(comando) != 1:
            return f"'{nombre}' no lleva datos"
        return ""

    # avanzar y girar llevan exactamente 2 datos: velocidad y tiempo
    if len(comando) != 3:
        return f"'{nombre}' necesita velocidad y tiempo"

    velocidad = comando[1]
    tiempo = comando[2]

    if type(velocidad) != int and type(velocidad) != float:
        return f"La velocidad '{velocidad}' no es un numero"

    if type(tiempo) != int and type(tiempo) != float:
        return f"El tiempo '{tiempo}' no es un numero"

    if tiempo < 0:
        return "El tiempo no puede ser negativo"

    if tiempo > TIEMPO_MAX:
        return f"El tiempo {tiempo} s supera el maximo de {TIEMPO_MAX} s"

    # El maximo depende del comando. En girar el signo solo indica
    # el sentido, por eso se compara contra el maximo y su negativo.
    if nombre == "avanzar":
        maximo = VELOCIDAD_AVANCE_MAX
        unidad = "m/s"
    else:
        maximo = VELOCIDAD_GIRO_MAX
        unidad = "rad/s"

    if velocidad > maximo or velocidad < -maximo:
        return f"La velocidad {velocidad} {unidad} supera el maximo de {maximo} {unidad}"

    return ""


def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False."""
    return obtener_motivo_rechazo(comando) == ""


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot.
    Devuelve una tupla: (se_ejecuto, mensaje, distancia, duracion)."""
    nombre = comando[0]

    try:
        if nombre == "avanzar":
            velocidad = comando[1]
            tiempo = comando[2]
            robot.avanzar(velocidad=velocidad, tiempo=tiempo)
            distancia = velocidad * tiempo
            if distancia < 0:
                distancia = -distancia
            return True, f"Avanzo a {velocidad} m/s durante {tiempo} s", distancia, tiempo

        elif nombre == "girar":
            velocidad = comando[1]
            tiempo = comando[2]
            robot.girar(velocidad=velocidad, tiempo=tiempo)
            return True, f"Giro a {velocidad} rad/s durante {tiempo} s", 0, tiempo

        elif nombre == "detenerse":
            robot.detenerse()
            return True, "Se detuvo", 0, 0

        elif nombre == "saludar":
            robot.saludar()
            return True, "Saludo", 0, 0

    except ErrorDeSeguridad as error:
        # Segunda capa: si igual se paso algo, el robot lo rechaza
        # y la mision sigue.
        return False, f"El robot lo rechazo por seguridad: {error}", 0, 0

    return False, "No se pudo ejecutar el comando", 0, 0


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos y guarda en historial que paso
    con cada uno. historial es una lista: se modifica aca adentro
    y no hace falta devolverla (pasaje por referencia)."""
    print(f"\n=== Iniciando mision: {len(mision)} comandos ===")

    for numero, comando in enumerate(mision, start=1):
        print(f"\nComando {numero}: {comando}")

        motivo = obtener_motivo_rechazo(comando)
        if motivo != "":
            historial.append({"comando": comando, "estado": "rechazado",
                              "motivo": motivo, "distancia": 0, "duracion": 0})
            print(f"[RECHAZADO] {motivo}")
            continue    

        se_ejecuto, mensaje, distancia, duracion = ejecutar_comando(robot, comando)

        if se_ejecuto:
            estado = "ejecutado"
            print(f"[OK] {mensaje}")
        else:
            estado = "rechazado"
            print(f"[RECHAZADO] {mensaje}")

        historial.append({"comando": comando, "estado": estado,
                          "motivo": mensaje, "distancia": distancia, "duracion": duracion})

    print("\n=== Mision finalizada ===")


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision."""
    ejecutados = 0
    rechazados = 0
    distancia_total = 0
    duracion_total = 0

    for registro in historial:
        if registro["estado"] == "ejecutado":
            ejecutados += 1
            distancia_total += registro["distancia"]
            duracion_total += registro["duracion"]
        else:
            rechazados += 1

    print("\n========================================")
    print("REPORTE FINAL")
    print("========================================")
    print(f"Comandos recibidos:   {len(historial)}")
    print(f"Comandos ejecutados:  {ejecutados}")
    print(f"Comandos rechazados:  {rechazados}")
    print(f"Distancia recorrida:  {round(distancia_total, 2)} m")
    print(f"Duracion estimada:    {round(duracion_total, 2)} s")

    if rechazados > 0:
        print("\nMotivos de los rechazos:")
        numero = 1
        for registro in historial:
            if registro["estado"] == "rechazado":
                print(f"  {numero}. {registro['comando']} -> {registro['motivo']}")
                numero += 1

    print("========================================")


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()
    historial = []

    try:
        
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()