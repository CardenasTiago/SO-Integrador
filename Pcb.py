class Pcb:
    
    def __init__(self,id,estado,tiempoArribo,cantRafagas,duracionRafaga,prioridadExterna):
        self.id = id
        self.estado = estado
        self.tiempoArribo = tiempoArribo
        self.cantRafagas = cantRafagas
        self.duracionRafaga = duracionRafaga
        self.prioridadExterna = prioridadExterna
        
    
    def getId(self):
        return self.id
    
    def getEstado(self):
        return self.Estado
    
    def getTiempoArribo(self):
        return self.tiempoArribo
    
    def getCantRafagas(self):
        return self.cantRafagas
    
    def getDuracionRafaga(self):
        return self.duracionRafaga
    
    def getPrioridadExterna(self):
        return self.prioridadExterna
    
    def setId(self, id):
        self.id = id
        
    def setEstado(self, estado):
        self.estado = estado
        
    def setTiempoArribo(self, tiempoArribo):
        self.tiempoArribo = tiempoArribo
        
    def setDuracionRafaga(self, duracionRafaga):
        self.duracionRafaga = duracionRafaga
        
    def setPrioridadExterna(self, prioridadExterna):
        self.prioridadExterna = prioridadExterna