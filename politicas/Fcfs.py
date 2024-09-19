from Cola import Cola
from Proceso import Proceso

class Fcfs:
    
    def __init__(self, listaProcesos,):
        self.listaProcesos = listaProcesos
        self.listaProcesosListos = Cola()
        self.listaProcesosBloqueados = Cola()
        self.listaProcesosFinalizados = Cola()
        self.procesoEjecutando = None
        self.tiempo = 0
        self.tip = 0
        self.tfp = 0
        self.tcp = 0
        self.conTcp = 0
        self.contTfp = 0
    
    def SolicitarDatos(self):
        print("INGRESE SIGUIENTES DATOS")
        self.tip = int(input("Tiempo que utiliza el sistema operativo para aceptar los nuevos procesos (TIP): "))
        self.tfp = int(input("Tiempo que utiliza el sistema operativo para terminar los procesos (TFP): "))
        self.tcp = int(input("Tiempo de conmutación entre procesos (TCP):"))
    
    
    def ProcesoListo(self):
        process = self.listaProcesos.desencolar()
        self.listaProcesosListos.encolar(process)
        print("Proceso " + process.getNombre() + " entro a Listo")
        
    
    def esperandoAListo(self):
        for proceso in self.listaProcesos.items:
            if proceso.getTiempoArrivo() == self.tiempo or proceso.getTiempoEsperando() >= 1:
                if proceso.getTiempoArrivo() == self.tiempo:
                    if proceso.getTiempoEsperando() == self.tip:
                        x = self.listaProcesos.desencolar()
                        self.listaProcesosListos.encolar(x)
                        print("Proceso " + x.getNombre() + " entro a Listo")
                    else:
                        proceso.tiempoEsperando += 1
                else:
                    if proceso.getTiempoEsperando() >= 1:
                        if proceso.getTiempoEsperando() == self.tip:
                            x = self.listaProcesos.desencolar()
                            self.listaProcesosListos.encolar(x)
                            print("Proceso " + x.getNombre() + " entro a Listo")
                        else:
                            proceso.tiempoEsperando += 1
        
    
    
    def listoAEjecutar(self):
        if self.procesoEjecutando == None:
            if self.conTcp == self.tcp:
                self.procesoEjecutando = self.listaProcesosListos.desencolar()
                print("Proceso " + self.procesoEjecutando.getNombre() + " entro en ejecucion")
                self.conTcp = 0
            else:
                frente = self.listaProcesosListos.frente()
                if frente == None:
                    print("No hay proceoso listos")
                else:
                    print("El proceso " + frente.getNombre() + " todavia no puede ejecutar, falta tiempo")
                    self.conTcp += 1
                
    
    def bloqueadoAListo(self):
        for proceso in self.listaProcesosBloqueados.items:
            if proceso.tiempoBloqueado < proceso.entradaSalida:
                proceso.tiempoBloqueado += 1
            else:
                listo = self.listaProcesosBloqueados.desencolar()
                listo.tiempoBloqueado = 0
                listo.tiempoRafaga = 0
                self.listaProcesosListos.encolar(listo)
                print("El proceso "+ listo.getNombre() +" pasó de bloqueado a listo")
                
                
    def listoABloqueado(self):
        if self.procesoEjecutando.pcb.cantRafagas == 0: 
            if self.contTfp == self.tfp:
                self.listaProcesosFinalizados.encolar(self.procesoEjecutando)
                print("proceso "+ self.procesoEjecutando.getNombre()+ " Finalizo")
                self.procesoEjecutando = None
                self.listoAEjecutar()
            else:
                self.contTfp += 1
                print("falta tfp para finalizar")
        else:
            self.listaProcesosBloqueados.encolar(self.procesoEjecutando)
            self.procesoEjecutando.pcb.cantRafagas -= 1
            print("Proceso "+ self.procesoEjecutando.getNombre()+ " entro en bloqueo")
            self.procesoEjecutando = None
            self.listoAEjecutar()
            
        
    
    def Iniciar(self):
        self.SolicitarDatos()
        while ((not self.listaProcesos.esta_vacia() or not self.listaProcesosListos.esta_vacia() or not self.listaProcesosBloqueados.esta_vacia()) or self.procesoEjecutando != None):
            print("TIEMPO " + str(self.tiempo))
            self.esperandoAListo()
            self.bloqueadoAListo()
            if self.procesoEjecutando == None:
                self.listoAEjecutar()
            else:
                if self.procesoEjecutando.getTiempoRafaga() < self.procesoEjecutando.getDuracionRafaga():
                    print("Se sigue ejecutanto el proceso "+ self.procesoEjecutando.getNombre())
                    self.procesoEjecutando.tiempoRafaga += 1
                else:
                    if self.procesoEjecutando.getTiempoRafaga() == self.procesoEjecutando.getDuracionRafaga():
                        self.listoABloqueado()

            self.tiempo += 1
                
            
                
                