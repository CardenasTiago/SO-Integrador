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
                self.log(f"Proceso {proceso.nombre} espera para ejecutar su TIP", archivo)
                
        if self.procesoEjecutando is None:
            frente = self.procesosNuevos.frente()
            if frente is not None:
                if frente.tiempoEsperando == self.tip:
                    self.log(f"Proceso {frente.nombre} entra a listo", archivo)
                    self.procesosNuevos.desencolarProceso(frente)
                    self.listaProcesosListos.encolar(frente)  # Corrección: Encolar el proceso en "procesos listos"
                    frente.tiempoEsperando = 0  # Reiniciar el tiempo de espera
                    self.so = False
                else:
                    frente.tiempoEsperando += 1
                    self.cpuSO += 1            
                    self.log(f"Proceso {frente.nombre} ejecuta TIP", archivo)
                    self.so = True
            
    
    
    def listoAEjecutar(self, archivo):
        if self.procesoEjecutando is None:
            frente = self.listaProcesosListos.frente()
            if frente is not None:
                if self.conTcp == 0 or self.primerProceso:
                    self.listaProcesosListos.ordenar(clave=lambda proceso: proceso.duracionRafaga, reverse=False)
                    self.procesoEjecutando = self.listaProcesosListos.desencolar()
                    self.log("Proceso " + self.procesoEjecutando.getNombre() + " entro en ejecución", archivo)
                    self.procesoEjecutando.pcb.cantRafagasRestante -= 1
                    self.conTcp = 0
                    self.primerProceso = False
            else:
                self.log("No hay procesos listos", archivo)
    
    
    def bloqueadoAListo(self, archivo):
        for proceso in self.listaProcesosBloqueados.items:
            if proceso.tiempoBloqueado < proceso.entradaSalida:
                proceso.tiempoBloqueado += 1
            else:
                listo = self.listaProcesosBloqueados.desencolar()
                listo.tiempoBloqueado = 0
                listo.tiempoRafaga = 0
                self.listaProcesosListos.encolar(listo)
                self.log("El proceso "+ listo.getNombre() +" pasó de bloqueado a listo", archivo)
                
    def listoABloqueado(self, archivo):
        if self.procesoEjecutando.pcb.cantRafagasRestante == 0: 
            if self.contTfp == self.tfp:
                    # Calcular el tiempo de retorno del proceso finalizado
                    tiempoFinalizacion = self.tiempo
                    tiempoRetorno = tiempoFinalizacion - self.procesoEjecutando.getTiempoArrivo()
                    self.procesoEjecutando.calcularTiempoRetorno(tiempoFinalizacion)
                    
                    # Agregar tiempo de retorno a la lista
                    self.tiemposRetorno.append(tiempoRetorno)
                    
                    self.listaProcesosFinalizados.encolar(self.procesoEjecutando)
                    self.log("Proceso " + self.procesoEjecutando.getNombre() + " Finalizó", archivo)
                    self.procesoEjecutando = None
                    self.contTfp = 0
                    self.conTcp = 0
            else:
                self.contTfp += 1
                self.cpuSO += 1
                self.log(f"Esperando el TFP para finalizar el proceso {self.procesoEjecutando.nombre}" , archivo)
        else:
            if self.conTcp == self.tcp:
                self.log("Proceso " + self.procesoEjecutando.getNombre() + " entró en bloqueo", archivo)
                self.listaProcesosBloqueados.encolar(self.procesoEjecutando)
                self.procesoEjecutando.tiempoBloqueado += 1
                self.procesoEjecutando = None
                self.conTcp = 0
            else:
                self.log("El proceso " + self.procesoEjecutando.getNombre() + " ejecuta el TCP", archivo)
                self.conTcp += 1
                self.cpuSO += 1
          
            
    def Iniciar(self):
        self.SolicitarDatos()
        with open('logs/log-Spn.txt', 'w') as archivo:
            while ((not self.listaProcesos.esta_vacia() or not self.listaProcesosListos.esta_vacia() or not self.listaProcesosBloqueados.esta_vacia() or not self.procesosNuevos.esta_vacia()) or not self.procesoEjecutando == None):
                self.log("--------------------",archivo)
                self.log("TIEMPO " + str(self.tiempo), archivo)
                self.esperandoAListo(archivo)
                self.bloqueadoAListo(archivo)
                if self.procesoEjecutando == None:
                    if not self.listaProcesosListos.esta_vacia():
                        self.listaProcesosListos.ordenar(clave=lambda proceso: proceso.duracionRafaga, reverse=False)
                        self.listoAEjecutar(archivo)
                    else:
                        self.log("No hay proceso en ejecucion y no hay procesos listos", archivo)
                        self.cpuOciosa += 1
                else:
                    if self.procesoEjecutando.getTiempoRafaga() < self.procesoEjecutando.getDuracionRafaga():
                        self.log("Se  ejecuta el proceso "+ self.procesoEjecutando.getNombre(), archivo)
                        self.procesoEjecutando.tiempoRafaga += 1
                        self.cpuProcesos += 1
                    if self.procesoEjecutando.getTiempoRafaga() == self.procesoEjecutando.getDuracionRafaga():
                        self.listoABloqueado(archivo)
                        self.listaProcesosListos.ordenar(clave=lambda proceso: proceso.duracionRafaga, reverse=False)
                        self.listoAEjecutar(archivo)
                        
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
        