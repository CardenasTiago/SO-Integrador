class Proceso:
    def __init__(self,nombre,at,rt,bt,ea,pe):
        self.nombre= nombre
        self.at = at
        self.rt = rt
        self.bt = bt
        self.ea = ea
        self.pe = pe
        
    def __str__(self) -> str:
        return f"nombre: {self.nombre}, at: {self.at}, rt: {self.rt}, bt: {self.bt}, ea: {self.ea}, pe: {self.pe}"
    
    
    
