class Buffer:
    def __init__(self, id_buffer, tiempo, proceso_anterior, proceso_siguiente):
        self.id_buffer = id_buffer
        self.tiempo = tiempo
        self.proceso_anterior = proceso_anterior
        self.proceso_siguiente = proceso_siguiente