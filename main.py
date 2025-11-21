from core.apuesta import Apuesta
from utils.probilidad_goles import prob_goles
from core.services.excel.excel_data import obtener_bankroll
import math
from utils.loger_fucker import LogerFucker

bankroll = obtener_bankroll("../Documents/Balance_Slither.xlsx", "Balance Stake", "K3")
log = LogerFucker()

def prob_btts(home_avg: float, away_avg: float) -> float:
    """ Calcula probabilidad de que ambos equipos marquen (BTTS)
        usando promedio de goles y distribución Poisson.
    """
    p_home_0 = math.exp(-home_avg)
    p_away_0 = math.exp(-away_avg)

    # Probabilidad de que al menos uno no marque
    p_no_btts = p_home_0 + p_away_0 - (p_home_0 * p_away_0)

    return 1 - p_no_btts

lambda_total = (2.04+ 0.71  + 2.05)/2
limites = [1.25, 3.75]

probabilidad_marcar = prob_btts(1.56, 1.34)
probabilidad_con_goles = max(prob_goles(lambda_total, limites[0], "over"), prob_goles(lambda_total, limites[1], "under"))
probabilidad_real =  0.8325870746 * 0.814422388781

ap = Apuesta(
    evento="",
    mercado="Ganador" ,
    equipo="" ,
    cuota=1.27 ,
    probabilidad_real= probabilidad_con_goles,
    bankroll=bankroll, 
    date="23/10/25"
)

log.table({
    "Promedio goles": lambda_total,
    f"{limites[0]} over": f"{prob_goles(lambda_total, limites[0], 'over'):.4f}",
    f"{limites[1]} under": f"{prob_goles(lambda_total, limites[1], 'under'):.4f}"
}, title="Probabilidad con goles")

log.table({
    "Apuesta con valor": ap.es_apuesta_con_valor(),
    "Stake": f"{ap.stake:.2f}",
    "Utilidad": f"{ap.calcular_utilidad():.2f}",
    "Probabilidad": f"{ap.probabilidad_real:.4f}",
    "Edge": f"{ap.calcular_edge():.4f}"
}, title="Informacion sobre apuesta")

log.separator()
