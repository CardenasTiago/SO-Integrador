from Cola import Cola
from Proceso import Proceso

class Spn:
    def __init__(self, listaProcesos):
        self.listaProcesos = listaProcesos
        self.listaProcesosListos = Cola()
        self.listaProcesosBloqueados = Cola()
        self.listaProcesosFinalizados = Cola()
        self.procesosNuevos = Cola()
        self.procesoEjecutando = None
        self.primerProceso = True
        self.tiempo = 0
        self.tip = 0
        self.tfp = 0
        self.tcp = 0
        self.ejecTcp = False
        self.ejecTfp = False
        self.conTcp = 0
        self.contTfp = 0
        self.so = False
        
        self.cpuOciosa = 0
        self.cpuSO = 0
        self.cpuProcesos = 0
        self.tiemposRetorno = []
        self.tiempoListoTotal = 0
    
    def SolicitarDatos(self):
        print("INGRESE SIGUIENTES DATOS")
        self.tip = int(input("Tiempo que utiliza el sistema operativo para aceptar los nuevos procesos (TIP): "))
        self.tfp = int(input("Tiempo que utiliza el sistema operativo para terminar los procesos (TFP): "))
        self.tcp = int(input("Tiempo de conmutación entre procesos (TCP):"))
    
    def log(self, mensaje, archivo):
        print(mensaje)
        archivo.write(mensaje + '\n')
    
    def esperandoAListo(self, archivo):
        for proceso in self.listaProcesos.items:
                if proceso.getTiempoArrivo() == self.tiempo:
                        self.listaProcesos.desencolarProceso(proceso)
                        self.procesosNuevos.encolar(proceso)
                        self.log(f"Proceso {proceso.nombre} espera para ejecutar su TIP",archivo)
                        
              
        if self.procesoEjecutando == None:          
            frente = self.procesosNuevos.frente()
            if frente != None:
                if frente.tiempoEsperando == self.tip:
                    self.log(f"Proceso {frente.nombre} finaliza su tip",archivo)  
                    self.log(f"Proceso {frente.nombre} Entra a Listo",archivo)
                    self.procesosNuevos.desencolarProceso(frente)
                    self.procesoEjecutando = frente
                    self.procesoEjecutando.pcb.cantRafagasRestante -= 1
                
                    self.so = False
                else:
                    frente.tiempoEsperando += 1
                    self.cpuSO += 1            
                    self.log(f"Proceso {frente.nombre} ejecuta tip",archivo)  
                    self.so = True
            
    
    
    def listoAEjecutar(self, archivo):
        self.listaProcesosListos.ordenar(clave=lambda proceso: proceso.duracionRafaga)
        frente = self.listaProcesosListos.frente()
        if self.procesoEjecutando == None:
            if frente != None:
                if self.conTcp == 0 or self.primerProceso:
                    self.procesoEjecutando = self.listaProcesosListos.desencolar()
                    self.log("Proceso " + self.procesoEjecutando.getNombre() + " entro en ejecucion",archivo)
                    self.procesoEjecutando.tiempoRafaga += 1
                    self.procesoEjecutando.pcb.cantRafagasRestante -= 1
                    self.conTcp = 0
                    self.primerProceso = False
            else:
                if frente == None:
                    self.log("No hay proceoso listos", archivo)
    
    
    def bloqueadoAListo(self, archivo):
        if not self.listaProcesosBloqueados.esta_vacia():
            procesos_a_listo = []
            for proceso in self.listaProcesosBloqueados.items:
                proceso.tiempoBloqueado += 1
                
                if proceso.tiempoBloqueado == proceso.entradaSalida:
                    procesos_a_listo.append(proceso)
            
            for proceso in procesos_a_listo:
                self.listaProcesosBloqueados.desencolarProceso(proceso)
                proceso.tiempoBloqueado = 0
                proceso.tiempoRafaga = 0 
                self.listaProcesosListos.encolar(proceso)
                self.log(f"El proceso {proceso.getNombre()} pasó de bloqueado a listo", archivo)
                self.listaProcesosListos.ordenar(clave=lambda proceso: proceso.duracionRafaga)
                
    def ejecutarTCP(self, archivo):
        if self.procesosNuevos.esta_vacia():
            if self.conTcp == self.tcp:
                if self.procesoEjecutando != None:
                    self.listaProcesosBloqueados.encolar(self.procesoEjecutando)
                self.procesoEjecutando = None
                self.conTcp = 0
                self.so = False
                self.ejecTcp = False
                self.log("Fin de TCP", archivo)
            else:
                self.log("Se ejecuta el TCP", archivo)
                self.conTcp += 1
                self.cpuSO += 1
                self.ejecTcp = True
                self.so = True
        else:
            self.listaProcesosBloqueados.encolar(self.procesoEjecutando)
            self.procesoEjecutando = None
            self.conTcp = 0
            self.so = True
            self.ejecTcp = False
            self.esperandoAListo(archivo)
            
    def ejecutarTFP(self, archivo):
        if self.contTfp == self.tfp:
            tiempoFinalizacion = self.tiempo
            tiempoRetorno = tiempoFinalizacion - self.procesoEjecutando.getTiempoArrivo()
            self.procesoEjecutando.calcularTiempoRetorno(tiempoFinalizacion)

            self.tiemposRetorno.append(tiempoRetorno)

            self.listaProcesosFinalizados.encolar(self.procesoEjecutando)
            self.log("Proceso " + self.procesoEjecutando.getNombre() + " Finalizó", archivo)
            self.procesoEjecutando = None
            self.contTfp = 0
            self.conTcp = 0
            self.so = False
            self.ejecTfp = False
            if not self.procesosNuevos.esta_vacia():
                self.esperandoAListo(archivo)
                self.ejecTfp = False
                self.ejecTcp = False
            else:
                self.so = True
                self.ejecutarTCP(archivo)
        else:
            self.contTfp += 1
            self.cpuSO += 1
            self.so = True
            self.log(f"Ejecuta TFP para finalizar el proceso {self.procesoEjecutando.nombre}", archivo)

            
    def Iniciar(self):
        self.SolicitarDatos()
        with open('logs/log-Spn.txt', 'w') as archivo:
            while ((not self.listaProcesos.esta_vacia() or not self.listaProcesosListos.esta_vacia() or not self.listaProcesosBloqueados.esta_vacia()) or not self.procesoEjecutando == None):
                self.log("--------------------",archivo)
                self.log("TIEMPO " + str(self.tiempo), archivo)
                self.esperandoAListo(archivo)
                self.bloqueadoAListo(archivo)
                if self.so and self.ejecTcp:
                    self.ejecutarTCP(archivo)
                elif self.so and self.ejecTfp:
                    self.ejecutarTFP(archivo)
                if self.procesoEjecutando == None :
                    if not self.listaProcesosListos.esta_vacia() and not self.so:
                        self.listoAEjecutar(archivo)
                    else:
                        self.log("No hay proceso en ejecucion y no hay procesos listos", archivo)
                        self.cpuOciosa += 1
                elif self.procesoEjecutando != None:
                    if self.procesoEjecutando.getTiempoRafaga() < self.procesoEjecutando.getDuracionRafaga():
                        self.log("Se  ejecuta el proceso "+ self.procesoEjecutando.getNombre(), archivo)
                        self.procesoEjecutando.tiempoRafaga += 1
                        self.cpuProcesos += 1
                    if self.procesoEjecutando.getTiempoRafaga() == self.procesoEjecutando.getDuracionRafaga() and not self.ejecTcp and not self.ejecTfp:
                        self.log(f"Proceso {self.procesoEjecutando.nombre} entró en bloqueo", archivo)
                        if self.procesoEjecutando.pcb.cantRafagasRestante == 0:
                            self.so = True
                            self.ejecTfp = True
                        else: 
                            self.so = True
                            self.ejecTcp = True
  
                        
                for proceso in self.listaProcesosListos.items:
                    proceso.tiempoEstadoListo += 1  
                self.tiempo += 1   
            self.log("--------------------------", archivo)    
            self.log("DATOS SOLICITADOS", archivo)  
            self.impProcesos(archivo)
            self.calcularTiemposMedios(archivo)
            self.calcularUsoCPU(archivo)
            
            
    def impProcesos(self,archivo):
        for proceso in self.listaProcesosFinalizados.items:
           self.log(f"Proceso {proceso.nombre}:", archivo)
           self.log(f"Tiempo de retorno: {proceso.tiempoRetorno}", archivo)     
           self.log(f"Tiempo de retorno: {proceso.tiempoRetornoNormalizado}", archivo)    
           self.log("--------------------------", archivo)
                
    def calcularTiemposMedios(self, archivo):
        totalRetorno = sum(self.tiemposRetorno)
        tiempoMedioRetorno = totalRetorno / self.listaProcesosFinalizados.tamano()
        self.log(f"Tiempo medio de retorno: {tiempoMedioRetorno}", archivo)

    def calcularUsoCPU(self,archivo):
        tiempoTotal = self.tiempo
        cpuSOporcentaje = (self.cpuSO / tiempoTotal) * 100
        cpuProcesosPorcentaje = (self.cpuProcesos / tiempoTotal) * 100
        cpuOciosaPorcentaje = (self.cpuOciosa / tiempoTotal) * 100
        self.log(f"CPU utilizada por procesos: {self.cpuProcesos} ({cpuProcesosPorcentaje}%)",archivo)
        self.log(f"CPU utilizada por SO: {self.cpuSO} ({cpuSOporcentaje}%)",archivo)
        self.log(f"CPU ociosa: {self.cpuOciosa} ({cpuOciosaPorcentaje}%)", archivo)