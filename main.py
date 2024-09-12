from Cola import Cola
from Proceso import Proceso
from politicas.Fcfs import Fcfs

datos = "datos.txt"

procesos = Cola()


with open(datos, 'r') as archivo:
    for linea in archivo:
        datos = linea.strip().split(',')
        if len(datos) == 6:
            proceso = Proceso(*datos)
            procesos.encolar(proceso)
    
politica = 0    
    
while politica == 0:
    print("SELECCIONE POLITICA")
    print("1-FCFS") 
    print("2-Prioridad Externa") 
    print("3-Round Robin") 
    print("4-SPN")
    print("5-SRTN")
    print("0-SALIR")
    politica = input("INGRESE: ")
    
if(politica == "1"):
   Fcfs = Fcfs(procesos)
   Fcfs.Iniciar()
   