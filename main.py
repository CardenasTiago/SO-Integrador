from Cola import Cola
from Proceso import Proceso
from politicas.Fcfs import Fcfs
from politicas.Spn import Spn
from politicas.Srtn import Srtn
datos = "datos.txt"

procesos = Cola()


with open(datos, 'r') as archivo:
    for linea in archivo:
        datos = linea.strip().split(',')
        if len(datos) == 6:
            nombre = datos[0]
            tiempoArrivo = int(datos[1])
            cantRafagas = int(datos[2])
            duracionRafaga = int(datos[3])
            entradaSalida = datos[4]
            prioridadExterna = int(datos[5])
            proceso = Proceso(nombre, tiempoArrivo, cantRafagas, duracionRafaga, entradaSalida, prioridadExterna)
            procesos.encolar(proceso)
    
politica = 0    
    
while politica == 0:
    print("SELECCIONE POLITICA")
    print("1-FCFS") 
    print("2-Spn") 
    print("3-SRTN") 
    print("4-Prioridad Externa")
    print("5-RoundRobin")
    print("0-SALIR")
    try:
        politica = int(input("INGRESE: "))  # Convertimos a entero
        if politica == 1:
            fcfsPolitica = Fcfs(procesos)
            fcfsPolitica.Iniciar()
            #fcfsPolitica.prueba()
        elif politica == 2:
            spnPolitica = Spn(procesos)
            spnPolitica.Iniciar()
            #spnPolitica.prueba()
        elif politica == 3:
            srtPolitica = Srtn(procesos)
            srtPolitica.Iniciar()
        
    except ValueError:
        print("Por favor, ingrese un número válido.")