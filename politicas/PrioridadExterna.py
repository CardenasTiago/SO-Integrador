from Cola import Cola
from Proceso import Proceso

class PrioridadExterna:
    def __init__(self, listaProcesos):
        self.listaProcesos = listaProcesos
        self.listaProcesosListos = Cola()
        self.listaProcesosBloqueados = Cola()
        self.listaProcesosFinalizados = Cola()
        self.procesosNuevos = Cola()
        self.nuevo = None
        self.procesoEjecutando = None
        self.primerProceso = True
        self.tiempo = 0
        self.ejecTip = False
        self.tip = 0
        self.conTip = 0
        self.ejecTfp = False
        self.tfp = 0
        self.tcp = 0
        self.ejecTcp = False
        self.conTcp = 0
        self.conTfp = 0
        self.cpuOciosa = 0
        self.cpuSO = 0
        self.cpuProcesos = 0
        self.tiemposRetorno = []
    
    def SolicitarDatos(self):
        print("INGRESE SIGUIENTES DATOS")
        self.tip = int(input("Tiempo que utiliza el sistema operativo para aceptar los nuevos procesos (TIP): "))
        self.tfp = int(input("Tiempo que utiliza el sistema operativo para terminar los procesos (TFP): "))
        self.tcp = int(input("Tiempo de conmutación entre procesos (TCP):"))
    
    def log(self, mensaje, archivo):
        print(mensaje)
        archivo.write(mensaje + '\n')
    
    def interrupcion(self, archivo, proceso):
        if self.procesoEjecutando:
            self.procesoEjecutando.pcb.duracionRafagaRestante = self.procesoEjecutando.duracionRafaga - self.procesoEjecutando.tiempoRafaga
            self.listaProcesosListos.encolar(self.procesoEjecutando)
            self.log(f"Proceso {self.procesoEjecutando.nombre} es interrumpido", archivo)
            self.procesoEjecutando = None
            self.procesoEjecutando = proceso
            if self.procesoEjecutando.primeraRafaga:
                self.ejecTip = True
            else:
                self.ejecTcp = True
    
    def esperandoAListo(self, archivo):
        for proceso in self.listaProcesos.items:
            if proceso.getTiempoArrivo() == self.tiempo:
                self.log(f"Proceso {proceso.nombre} Entra a Listo", archivo)
                self.listaProcesos.desencolarProceso(proceso)
                self.listaProcesosListos.encolar(proceso)
                
                if self.procesoEjecutando:
                    if proceso.prioridadExterna > self.procesoEjecutando.prioridadExterna:
                        self.log(f"Proceso {proceso.nombre} tiene mayor prioridad que {self.procesoEjecutando.getNombre()}, iniciando conmutación", archivo)
                        self.interrupcion(archivo, proceso)
                        self.conTcp = 0
                else:
                    self.procesoEjecutando = self.listaProcesosListos.desencolarProceso(proceso)
                    self.ejecTip = True
    
    def listoAEjecutar(self, archivo):
        frente = self.listaProcesosListos.frente()
        if self.procesoEjecutando == None and frente != None:
                self.listaProcesosListos.ordenar(clave=lambda proceso: proceso.prioridadExterna, reverse=True)
                self.procesoEjecutando = self.listaProcesosListos.desencolar()
                if not self.procesoEjecutando.primeraRafaga:

                        self.ejecutarTcp(archivo)
                        self.log(f"Proceso {self.procesoEjecutando.getNombre()} entró en ejecución", archivo)
                        
                else:
                    self.ejecutarTip(archivo)
        elif frente == None:
            self.log("No hay procesos listos", archivo)
    
    def bloqueadoAListo(self, archivo):
        procesos_a_mover = []
        for proceso in self.listaProcesosBloqueados.items:
            if proceso.tiempoBloqueado < proceso.entradaSalida:
                proceso.tiempoBloqueado += 1
            else:
                procesos_a_mover.append(proceso)
        
        for proceso in procesos_a_mover:
            self.listaProcesosBloqueados.desencolarProceso(proceso)
            proceso.tiempoBloqueado = 0
            self.listaProcesosListos.encolar(proceso)
            self.log(f"El proceso {proceso.getNombre()} pasó de bloqueado a listo", archivo)
        
        if procesos_a_mover and self.procesoEjecutando:
            proceso_mayor_prioridad = max(procesos_a_mover, key=lambda p: p.prioridadExterna)
            if proceso_mayor_prioridad.prioridadExterna > self.procesoEjecutando.prioridadExterna:
                self.log(f"Proceso {proceso_mayor_prioridad.nombre} tiene mayor prioridad que {self.procesoEjecutando.getNombre()}, iniciando conmutación", archivo)
                self.interrupcion(archivo, proceso_mayor_prioridad)
    
    def ejecutarTip(self,archivo):
        if self.conTip < self.tip:
            self.log(f"Se ejecuta TIP de proceso {self.procesoEjecutando.nombre}", archivo)
            self.conTip += 1
            self.cpuSO += 1
            self.ejecTip = True
        else:
            self.log(f"Fin de TIP", archivo)
            self.ejecTip = False
            self.conTip = 0
            self.procesoEjecutando.primeraRafaga = False
    
    def ejecutarTcp(self, archivo):
        if self.conTcp < self.tcp:
            self.log(f"Ejecutando TCP ({self.conTcp + 1}/{self.tcp})", archivo)
            self.conTcp += 1
            self.cpuSO += 1
            self.ejecTcp = True
        else:
            self.log(f"Fin de TCP", archivo)
            self.ejecTcp = False
            self.conTcp = 0

    
    def listoABloqueado(self, archivo):
        if self.procesoEjecutando:
            self.procesoEjecutando.tiempoRafaga = 0
            self.procesoEjecutando.pcb.cantRafagasRestante -= 1
            if self.procesoEjecutando.pcb.cantRafagasRestante <= 0:
                self.ejecTfp = True
            else:
                self.log(f"Proceso {self.procesoEjecutando.getNombre()} bloqueado", archivo)
                self.listaProcesosBloqueados.encolar(self.procesoEjecutando)
                self.listaProcesosListos.desencolarProceso(self.procesoEjecutando)
                self.procesoEjecutando = None
                
    
    def ejecutarTfp(self, archivo):
        if self.conTfp < self.tfp:
            self.log(f"Ejecutando TFP ({self.conTfp + 1}/{self.tfp}) para finalizar el proceso {self.procesoEjecutando.getNombre()}", archivo)
            self.ejecTfp = True
            self.conTfp += 1
            self.cpuSO += 1     
        else:
            self.ejecTfp = False
            tiempoFinalizacion = self.tiempo
            tiempoRetorno = tiempoFinalizacion - self.procesoEjecutando.getTiempoArrivo()
            self.procesoEjecutando.calcularTiempoRetorno(tiempoFinalizacion)
            self.tiemposRetorno.append(tiempoRetorno)
            self.listaProcesosFinalizados.encolar(self.procesoEjecutando)
            self.log(f"TFP ({self.conTfp}/{self.tfp}) finalizado para el proceso {self.procesoEjecutando.getNombre()}", archivo)
            self.listaProcesosListos.desencolarProceso(self.procesoEjecutando)
            self.procesoEjecutando = None
            self.conTfp = 0

    
    def Iniciar(self):
        self.SolicitarDatos()
        with open('logs/log-PE.txt', 'w') as archivo:
            while (not self.listaProcesos.esta_vacia() or 
                   not self.listaProcesosListos.esta_vacia() or 
                   not self.listaProcesosBloqueados.esta_vacia() or 
                   self.procesoEjecutando is not None):
                
                self.log(f"--------------------", archivo)
                self.log(f"TIEMPO {self.tiempo}", archivo)
                
                self.esperandoAListo(archivo)
                self.bloqueadoAListo(archivo)
                
                if self.ejecTfp:
                    self.ejecutarTfp(archivo)
                elif self.ejecTcp:
                    self.ejecutarTcp(archivo)
                elif self.ejecTip:
                    self.ejecutarTip(archivo)
                
                if self.procesoEjecutando and (not self.ejecTcp and not self.ejecTfp and not self.ejecTip):
                    if self.procesoEjecutando.getTiempoRafaga() < self.procesoEjecutando.getDuracionRafaga():
                        self.log(f"Se ejecuta el proceso {self.procesoEjecutando.getNombre()}", archivo)
                        self.procesoEjecutando.tiempoRafaga += 1
                        self.cpuProcesos += 1
                    if self.procesoEjecutando.getTiempoRafaga() == self.procesoEjecutando.getDuracionRafaga():
                        self.listoABloqueado(archivo)
                else:
                    if not self.ejecTcp and not self.ejecTfp and not self.ejecTip:
                        self.listoAEjecutar(archivo)
                        if self.procesoEjecutando is None:
                            self.log("CPU ociosa", archivo)
                            self.cpuOciosa += 1
                
                for proceso in self.listaProcesosListos.items:
                    proceso.tiempoEstadoListo += 1
                
                self.tiempo += 1
            
            self.log("--------------------------", archivo)    
            self.log("DATOS SOLICITADOS", archivo)      
            self.impProcesos(archivo)
            self.calcularTiemposMedios(archivo)
            self.calcularUsoCPU(archivo)
    
    def impProcesos(self, archivo):
        for proceso in self.listaProcesosFinalizados.items:
           self.log(f"Proceso {proceso.nombre}:", archivo)
           self.log(f"Tiempo de retorno: {proceso.tiempoRetorno}", archivo)     
           self.log(f"Tiempo de retorno normalizado: {proceso.tiempoRetornoNormalizado}", archivo)    
           self.log("--------------------------", archivo)
    
    def calcularTiemposMedios(self, archivo):
        if self.tiemposRetorno:
            totalRetorno = sum(self.tiemposRetorno)
            tiempoMedioRetorno = totalRetorno / len(self.tiemposRetorno)
            self.log(f"Tiempo medio de retorno: {tiempoMedioRetorno}", archivo)
        else:
            self.log("No hay tiempos de retorno para calcular.", archivo)

    def calcularUsoCPU(self, archivo):
        tiempoTotal = self.tiempo
        cpuSOporcentaje = (self.cpuSO / tiempoTotal) * 100 if tiempoTotal > 0 else 0
        cpuProcesosPorcentaje = (self.cpuProcesos / tiempoTotal) * 100 if tiempoTotal > 0 else 0
        cpuOciosaPorcentaje = (self.cpuOciosa / tiempoTotal) * 100 if tiempoTotal > 0 else 0
        self.log(f"CPU utilizada por procesos: {self.cpuProcesos} ({cpuProcesosPorcentaje:.2f}%)", archivo)
        self.log(f"CPU utilizada por SO: {self.cpuSO} ({cpuSOporcentaje:.2f}%)", archivo)
        self.log(f"CPU ociosa: {self.cpuOciosa} ({cpuOciosaPorcentaje:.2f}%)", archivo)