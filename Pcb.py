class Pcb:
    
    def __init__(self,id,estado,tiempoArribo,cantRafagas,duracionRafaga,prioridadExterna):
        self.id = id
        self.estado = estado
        self.tiempoArribo = tiempoArribo
        self.cantRafagas = cantRafagas
        self.duracionRafaga = duracionRafaga
        self.prioridadExterna = prioridadExterna
        