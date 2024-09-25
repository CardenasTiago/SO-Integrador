from Pcb import Pcb

class Proceso:
    def __init__(self,nombre,tiempoArrivo,cantRafagas,duracionRafaga,entradaSalida,prioridadExterna):
        self.nombre= nombre
        self.tiempoArrivo = int(tiempoArrivo)
        self.cantRafagas = int(cantRafagas)
        self.duracionRafaga = int(duracionRafaga)
        self.entradaSalida = int(entradaSalida)
        self.prioridadExterna = int(prioridadExterna)
        self.pcb = Pcb(self.nombre,"listo",self.tiempoArrivo,self.cantRafagas,self.duracionRafaga,self.prioridadExterna)
        self.tiempoEsperando = 0
        self.tiempoBloqueado = 0
        self.tiempoEstadoListo = 0
        self.tiempoRafaga = 0
        
        self.tiempoRetorno = 0
        self.tiempoRetornoNormalizado = 0
            
    def __str__(self) -> str:
        return f"nombre: {self.nombre}, tiempoArrivo: {self.tiempoArrivo}, cantRafagas: {self.cantRafagas}, duracionRafaga: {self.duracionRafaga}, entradaSalida: {self.entradaSalida}, prioridadExterna: {self.prioridadExterna}"
    
    def getNombre(self):
        return self.nombre
    
    def getTiempoArrivo(self):
        return int(self.tiempoArrivo)
    
    def getCantRafagas(self):
        return int(self.cantRafagas)
    
    def getDuracionRafaga(self):
        return int(self.duracionRafaga)
    
    def getEntradaSalida(self):
        return int(self.entradaSalida)
    
    def getPrioridadExterna(self):
        return int(self.prioridadExterna)
    
    def getTiempoRafaga(self):
        return int(self.tiempoRafaga)
    
    def getTiempoEsperando(self):
        return int(self.tiempoEsperando)
    
    def calcularTiempoRetorno(self, tiempoFinalizacion):
        self.tiempoRetorno = tiempoFinalizacion - self.tiempoArrivo
        self.tiempoRetornoNormalizado = self.tiempoRetorno / (self.cantRafagas * self.duracionRafaga)
        
    
    
    
