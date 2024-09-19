class Cola:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        else:
            return None

    def frente(self):
        if not self.esta_vacia():
            return self.items[0]
        else:
            return None

    def tamano(self):
        return len(self.items)
    
    def ordenar(self, clave=None, reverse=False):
        """
        Ordena la cola según una clave proporcionada.

        :param clave: Función que especifica un parámetro por el cual ordenar (similar a sorted).
        :param reverse: Si es True, ordena en orden descendente.
        """
        self.items.sort(key=clave, reverse=reverse)
    

    def imprimir(self):
        print("Contenido de la cola:")
        for proceso in self.items:
            print(proceso)
        print("--------------------")