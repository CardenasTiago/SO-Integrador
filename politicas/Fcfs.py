from Cola import Cola
from Proceso import Proceso

class Fcfs:
    
    def __init__(self, listaProcesos,):
        self.listaProcesos = Cola()
        self.listaProcesos = listaProcesos
        self.listaProcesosListos = Cola()
        self.procesoEjecutando = Proceso
        self.procesoEjecutando = None
        self.tiempo = 0
        self.tip = 0
        self.tfp = 0
        self.tcp = 0
        self.conTcp = 0
    
    def SolicitarDatos(self):
        print("INGRESE SIGUIENTES DATOS")
        self.tip = input("Tiempo que utiliza el sistema operativo para aceptar los nuevos procesos (TIP): ")
        self.tfp = input("Tiempo que utiliza el sistema operativo para terminar los procesos (TFP): ")
        self.tcp = input("Tiempo de conmutación entre procesos (TCP):")
    
    
    def ProcesoListo(self):
        process = self.listaProcesos.desencolar()
        self.listaProcesosListos.encolar(process)
        print("Proceso " + process.getNombre() + " entro a Listo")
        
    
    def esperandoAListo(self):
        frente = Proceso()
        frente = self.listaProcesos.frente()
        if frente.getTiempoArrivo() == self.tiempo or frente.getTiempoEsperando() >= 1:
            if frente.getTiempoArrivo() == self.tiempo:
                if frente.getTiempoEsperando() == self.tip:
                    self.ProcesoListo()
                else:
                    frente.tiempoEsperando += 1
            else: 
                if frente.getTiempoEsperando() >= 1:
                    if frente.getTiempoEsperando() == self.tip:
                     self.ProcesoListo()
                    else:
                        frente.tiempoEsperando += 1
    
    
    
    def listoAEjecutar(self):
        if self.procesoEjecutando == None:
            if self.conTcp == self.tcp:
                self.procesoEjecutando = self.listaProcesosListos.desencolar()
                print("Proceso " + self.procesoEjecutando.getNombre() + " entro en ejecucion")
                self.conTcp = 0
            else:
                frente = Proceso()
                frente = self.listaProcesosListos.frente()
                print("El proceso " + frente.getNombre() + "todavia no puede ejecutar, falta tiempo")
                self.conTcp += 1
    
    
    
    def finPorceso(self):
        print("Proceso " +  self.procesoEjecutando.getNombre() + " dejo de ejecutarse")
        self.procesoEjecutando = None
        
    
    
    
    def Iniciar(self):
        self.SolicitarDatos()
        while (not self.listaProcesos.esta_vacia() or not self.listaProcesosListos.esta_vacia()):
            print("TIEMPO: " + self.tiempo)
            if self.procesoEjecutando != None:
                if self.procesoEjecutando.getTiempoRafaga() == self.procesoEjecutando.getDuracionRafaga():
                    self.finPorceso()
                    self.listoAEjecutar()
            else:
                if self.listaProcesosListos.esta_vacia:
                    self.esperandoAListo()
                    
                    
                    
                    
                    
            self.tiempo += 1
                
                
                
            
                
                