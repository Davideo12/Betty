import math

def prob_btts(home_avg: float, away_avg: float) -> float:
    """ Calcula probabilidad de que ambos equipos marquen (BTTS)
        usando promedio de goles y distribución Poisson.
    """
    p_home_0 = math.exp(-home_avg)
    p_away_0 = math.exp(-away_avg)

    # Probabilidad de que al menos uno no marque
    p_no_btts = p_home_0 + p_away_0 - (p_home_0 * p_away_0)

    return 1 - p_no_btts