import math

def prob_goles(lambda_total: float, limite: float, tipo: str = "under") -> float:
    """
    Calcula la probabilidad de que los goles totales estén por debajo o por encima de un límite dado.
    
    Parámetros:
        lambda_total: promedio de goles esperados (λ)
        limite: número de goles (por ejemplo, 2.5 o 3)
        tipo: "under" o "over"
    
    Retorna:
        Probabilidad (entre 0 y 1)
    """
    limite_entero = math.floor(limite)

    # Probabilidad acumulada hasta el límite
    prob_acum = sum(math.exp(-lambda_total) * (lambda_total ** k) / math.factorial(k)
                    for k in range(limite_entero + 1))
    
    if tipo.lower() == "under":
        return prob_acum
    elif tipo.lower() == "over":
        return 1 - prob_acum
    else:
        raise ValueError("El parámetro 'tipo' debe ser 'under' o 'over'.")