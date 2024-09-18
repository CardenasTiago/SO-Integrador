from Pcb import Pcb

class Proceso:
    def __init__(self,nombre,tiempoArrivo,cantRafagas,duracionRafaga,entradaSalida,prioridadExterna):
        self.nombre= nombre
        self.tiempoArrivo = tiempoArrivo
        self.cantRafagas = cantRafagas
        self.duracionRafaga = duracionRafaga
        self.entradaSalida = entradaSalida
        self.prioridadExterna = prioridadExterna
        self.pcb = Pcb(nombre,"listo",tiempoArrivo,cantRafagas,duracionRafaga,prioridadExterna)
        self.tiempoEsperando = 0
        self.tiempoBloqueado = 0
        self.tiempoEstadoListo = 0
        self.tiempoRafaga = 0
        
    def __str__(self) -> str:
        return f"nombre: {self.nombre}, tiempoArrivo: {self.tiempoArrivo}, cantRafagas: {self.cantRafagas}, duracionRafaga: {self.duracionRafaga}, entradaSalida: {self.entradaSalida}, prioridadExterna: {self.prioridadExterna}"
    
    def getNombre(self):
        return self.nombre
    
    def getTiempoArrivo(self):
        return self.tiempoArrivo
    
    def getCantRafagas(self):
        return self.cantRafagas
    
    def getDuracionRafaga(self):
        return self.duracionRafaga
    
    def getEntradaSalida(self):
        return self.entradaSalida
    
    def getPrioridadExterna(self):
        return self.prioridadExterna
    
    def getTiempoRafaga(self):
        return self.tiempoRafaga
    
    def getTiempoEsperando(self):
        return self.tiempoEsperando
    
    
    
