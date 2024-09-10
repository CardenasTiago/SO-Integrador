from Cola import Cola
from Proceso import Proceso
import sys
from os import system

datos = "datos.txt"

procesos = Cola()


with open(datos, 'r') as archivo:
    for linea in archivo:
        datos = linea.strip().split(',')
        if len(datos) == 6:
            proceso = Proceso(*datos)
            procesos.encolar(proceso)
    

procesos.imprimir()
        