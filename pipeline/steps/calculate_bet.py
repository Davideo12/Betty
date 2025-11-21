from pipeline.steps.setp import BaseStep
from utils.probilidad_goles import prob_goles
from utils.prob_btts import prob_btts
from core.services.excel.excel_data import obtener_bankroll
from core.bet_analyzer import BetAnalyzer3000

class CalculateBetStep(BaseStep):

    def __init__(self):
        super().__init__()
        self.bankroll = obtener_bankroll("../Documents/Balance_Slither.xlsx", "Balance Stake", "K3")
        self.ap = BetAnalyzer3000()
    
    def _mejor_apuesta_totales(self, totales: dict, lambda_total: float):
        """
        A partir del diccionario de cuotas 'totales' y el valor esperado de goles (lambda_total),
        devuelve la apuesta con mayor probabilidad de acierto (mayor probabilidad real).
        """
        mejor_opcion = None
        mejor_prob = float("-inf")

        for clave, cuota in totales.items():
            # Separar el límite y el tipo (over/under)
            partes = clave.split()
            if len(partes) != 2:
                continue  # seguridad ante datos mal formados

            limite = float(partes[0])
            tipo = partes[1].lower()

            # Calcular probabilidad teórica según Poisson
            prob = prob_goles(lambda_total, limite, tipo)

            # Guardar la opción con mayor probabilidad
            if prob > mejor_prob:
                mejor_prob = prob
                mejor_opcion = {
                    "mercado": clave,
                    "probabilidad": round(prob, 3),
                    "cuota": cuota
                }

        return mejor_opcion


    def run(self, context):
        context["good_bets"] = []

        fixtures_list = context["fixtures"]

        for fixture in fixtures_list:
            event = fixture["event"]
            odds_1x2 = fixture["odds"]["1X2"]
            avg_goals = fixture["predictions"]["avg_goals"]

            # --- Apuestas de 1X2 ---
            pred = fixture["predictions"]["prediction"]
            equipos = {
                "1": fixture["home_team"],
                "X": "Draw",
                "2": fixture["away_team"]
            }
            probabilidades = {
                "1": fixture["probabilities"]["home_win"],
                "X": fixture["probabilities"]["draw"],
                "2": fixture["probabilities"]["away_win"]
            }

            if pred in equipos:
                data = self.ap.analyze_bet({"event":event, "odd":odds_1x2[pred], "p_real":probabilidades[pred]})
                if data["is_worth"]:

                    data["mercado"] = "1 x 2"
                    data["equipo"] = pred
                    fixture["bet_data"] = data

                    context["good_bets"].append(fixture)

            # --- Apuestas de totales (Over/Under) ---
            mejor_apuesta = self._mejor_apuesta_totales(fixture["odds"]["totales"], lambda_total=avg_goals)

            if mejor_apuesta:  # Validar que no sea None
                data = self.ap.analyze_bet({"event":event, "odd":mejor_apuesta["cuota"], "p_real":mejor_apuesta["probabilidad"]})
                if data["is_worth"]:
                    
                    data["mercado"] = mejor_apuesta["mercado"]
                    data["equipo"] = ""
                    fixture["bet_data"] = data

                    context["good_bets"].append(fixture)

            # --- Apuestas BTTS ---

        return context  