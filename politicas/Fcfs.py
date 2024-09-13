from Cola import Cola
from Proceso import Proceso

class Fcfs:
    
    def __init__(self, listaProcesos,):
        self.listaProcesos = Cola()
        self.listaProcesos = listaProcesos
        self.procesosListos = Cola()
        self.tiempo = 0
        self.tip = 0
        self.tfp = 0
        self.tcp = 0
    
    
    def SolicitarDatos(self):
        print("INGRESE SIGUIENTES DATOS")
        self.tip = input("Tiempo que utiliza el sistema operativo para aceptar los nuevos procesos (TIP): ")
        self.tfp = input("Tiempo que utiliza el sistema operativo para terminar los procesos (TFP): ")
        self.tcp = input("Tiempo de conmutación entre procesos (TCP):")
    
    def Iniciar(self):
        self.SolicitarDatos()
        while (not self.listaProcesos.esta_vacia()):
            procesoActual = Proceso()
            procesoActual = self.listaProcesos.desencolar()
            
            if(procesoActual.g)
                
            