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
        
    def __str__(self) -> str:
        return f"nombre: {self.nombre}, tiempoArrivo: {self.tiempoArrivo}, cantRafagas: {self.cantRafagas}, duracionRafaga: {self.duracionRafaga}, entradaSalida: {self.entradaSalida}, prioridadExterna: {self.prioridadExterna}"
    
    
    
