

class Apuesta:

    def __init__(self, evento:str, liga:str, mercado:str, equipo:str, cuota:float, probabilidad_real:float, bankroll:float, date:str):
        self.evento = evento
        self.liga = liga
        self.mercado = mercado
        self.equipo = equipo
        self.cuota = cuota
        self.probabilidad_real = probabilidad_real
        self.bankroll = bankroll
        self.date = date

        self.stake = self.calcular_fraccion_kelly() * bankroll
        self.probabilidad_implicita = 1/cuota

    # EV de la apuesta
    def calcular_valor_esperado(self) -> float:
        return ( self.probabilidad_real * (self.cuota - 1) ) - (( 1 - self.probabilidad_real) * 1 )

    # Calcula la fraccion kelly
    def calcular_fraccion_kelly(self) -> float:
        b = 1/self.cuota
        f = ( self.probabilidad_real * ( b + 1 ) - 1 ) / b
        return max(0.01, f/2) # Evita fracciones negativas | Usamos half_kelly

    # Reotrno sobre inversion 
    def calcular_roi(self) -> float:
        if self.stake:
            return (self.calcular_utilidad() / self.stake ) * 100
        else: 
            return 0


    # Ganancia total de la apuesta
    def calcular_ganancia(self) -> float:
        return self.stake * self.cuota
    
    # Utilidad de la apuesta 
    def calcular_utilidad(self) -> float:
        return self.calcular_ganancia() - self.stake
    
    # Diferencia entre probabilidad real y probabilidad implícita de la cuota.
    def calcular_edge(self) -> float:
        return self.probabilidad_real - self.probabilidad_implicita

    # Devuelve True si el EV es positico
    def es_apuesta_con_valor(self) -> bool:
        if (self.calcular_valor_esperado() > 0) and (self.calcular_edge() > 0):
            return True
        else:
            return False
        

    def to_dict(self) -> dict:
        return {
            "evento": self.evento,
            "mercado": self.mercado,
            "equipo": self.equipo,
            "cuota": self.cuota,
            "probabilidad_Real": self.probabilidad_real,
            "stake": self.stake,
            "date": self.date
        }
    
    def __str__(self):
        return f"\nEvento: {self.evento}\nApuesta con valor: {self.es_apuesta_con_valor()} \nStake: ${self.stake:.2f} \nUtilidad: ${self.calcular_utilidad():.2f}\nProbabilidad: {self.probabilidad_real*100:.2f}%\nEdge: {self.calcular_edge():.4f}"