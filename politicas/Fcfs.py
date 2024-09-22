from Cola import Cola
from Proceso import Proceso

class Fcfs:
    
    def __init__(self, listaProcesos):
        self.listaProcesos = listaProcesos
        self.listaProcesosListos = Cola()
        self.listaProcesosBloqueados = Cola()
        self.listaProcesosFinalizados = Cola()
        self.procesoEjecutando = None
        self.primerProceso = True
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
        frente = self.listaProcesosListos.frente()
        if self.procesoEjecutando == None:
            if frente != None:
                if self.conTcp == 0 or self.primerProceso:
                    self.procesoEjecutando = self.listaProcesosListos.desencolar()
                    print("Proceso " + self.procesoEjecutando.getNombre() + " entro en ejecucion")
                    self.procesoEjecutando.pcb.cantRafagas -= 1
                    self.conTcp = 0
                    self.primerProceso = False
            else:
                if frente == None:
                    print("No hay proceoso listos")
    
    
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
                
    """        
    def listoABloqueado(self):
        if self.procesoEjecutando.pcb.cantRafagas == 0: 
            if self.contTfp == self.tfp:
                # Finaliza el proceso y reinicia las variables necesarias
                self.listaProcesosFinalizados.encolar(self.procesoEjecutando)
                print("Proceso " + self.procesoEjecutando.getNombre() + " Finalizó")
                self.procesoEjecutando = None
                self.contTfp = 0
                self.conTcp = 0
                # Después de finalizar, intenta ejecutar otro proceso si hay en la cola de listos
                if not self.listaProcesosListos.esta_vacia():
                    self.listoAEjecutar()
                else:
                    print("No hay más proce and self.tiempo <= 60sos listos para ejecutar.")
            else:
                self.contTfp += 1
                print("Esperando el TFP para finalizar el proceso.")
        else:
            if self.conTcp == self.tcp:
                print("Proceso " + self.procesoEjecutando.getNombre() + " entró en bloqueo")
                self.listaProcesosBloqueados.encolar(self.procesoEjecutando)
                if self.procesoEjecutando.pcb.cantRafagas > 0:
                    self.procesoEjecutando.pcb.cantRafagas -= 1
                self.procesoEjecutando.tiempoBloqueado += 1
                self.procesoEjecutando = None
                self.conTcp = 0
                # Intenta ejecutar otro proceso después de bloquear el actual
                if not self.listaProcesosListos.esta_vacia():
                    self.listoAEjecutar()
                else:
                    print("No hay más procesos listos para ejecutar.")
            else:
                print("El proceso " + self.procesoEjecutando.getNombre() + " ejecuta el TCP")
                self.conTcp += 1
    """
    def listoABloqueado(self):
        if self.procesoEjecutando.pcb.cantRafagas == 0: 
            if self.contTfp == self.tfp:
                # Finaliza el proceso y reinicia las variables necesarias
                self.listaProcesosFinalizados.encolar(self.procesoEjecutando)
                print("Proceso " + self.procesoEjecutando.getNombre() + " Finalizó")
                self.procesoEjecutando = None
                self.contTfp = 0
                self.conTcp = 0
                # Después de finalizar, intenta ejecutar otro proceso si hay en la cola de listos
                if not self.listaProcesosListos.esta_vacia():
                    self.listoAEjecutar()
                else:
                    print("No hay más proce and self.tiempo <= 60sos listos para ejecutar.")
            else:
                self.contTfp += 1
                print("Esperando el TFP para finalizar el proceso.")
        else:
            if self.conTcp == self.tcp:
                print("Proceso " + self.procesoEjecutando.getNombre() + " entró en bloqueo")
                self.listaProcesosBloqueados.encolar(self.procesoEjecutando)
                self.procesoEjecutando.tiempoBloqueado += 1
                self.procesoEjecutando = None
                self.conTcp = 0
                # Intenta ejecutar otro proceso después de bloquear el actual
                if not self.listaProcesosListos.esta_vacia():
                    self.listoAEjecutar()
                else:
                    print("No hay más procesos listos para ejecutar.")
            else:
                print("El proceso " + self.procesoEjecutando.getNombre() + " ejecuta el TCP")
                self.conTcp += 1
          
            
    def Iniciar(self):
        self.SolicitarDatos()
        while ((not self.listaProcesos.esta_vacia() or not self.listaProcesosListos.esta_vacia() or not self.listaProcesosBloqueados.esta_vacia()) or not self.procesoEjecutando == None):
            print("TIEMPO " + str(self.tiempo))
            self.esperandoAListo()
            self.bloqueadoAListo()
            if self.procesoEjecutando == None:
                self.listoAEjecutar()
            else:
                if self.procesoEjecutando.getTiempoRafaga() < self.procesoEjecutando.getDuracionRafaga():
                    print("Se sigue ejecutanto el proceso "+ self.procesoEjecutando.getNombre())
                    self.procesoEjecutando.tiempoRafaga += 1
                if self.procesoEjecutando.getTiempoRafaga() == self.procesoEjecutando.getDuracionRafaga():
                    self.listoABloqueado()
            self.tiempo += 1
                