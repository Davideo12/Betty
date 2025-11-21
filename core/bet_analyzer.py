from typing import List, Dict
import math

class BetAnalyzer3000:
    """
    Analiza apuestas individuales o múltiples para determinar si son 'buenas opciones'
    basándose en valor esperado (EV), edge y criterio de Kelly.
    """

    def __init__(self, min_ev: float = 0.05, name: str = "BetAnalyzer3000"):
        self.name = name
        self.min_ev = min_ev  # Umbral mínimo de EV% para considerar 'buena apuesta'

    def _calc_risk(self, odd: float, p_real: float) -> Dict[str, float]:
        """Calcula varianza, desviación estándar y coeficiente de variación."""
        gain = odd - 1
        loss = -1
        ev = self._calc_ev(odd, p_real)
        var = p_real * (gain ** 2) + (1 - p_real) * (loss ** 2) - ev ** 2
        sigma = math.sqrt(var)
        cv = sigma / abs(ev) if ev != 0 else float("inf")
        return {"Var": round(var, 4), "Sigma": round(sigma, 4), "CV": round(cv, 2)}

    def _calc_ev(self, odd: float, p_real: float) -> float:
        """Valor esperado en términos absolutos (no porcentaje)."""
        return (p_real * (odd - 1)) - (1 - p_real)

    def _calc_edge(self, odd: float, p_real: float) -> float:
        """Ventaja porcentual sobre la casa."""
        p_casa = 1 / odd
        return ((p_real - p_casa) / p_casa) * 100

    def _kelly_fraction(self, odd: float, p_real: float) -> float:
        """Criterio de Kelly para fracción óptima de banca."""
        f = ((odd - 1) * p_real - (1 - p_real)) / (odd - 1)
        return max(0, round(f, 4))  # No apostar si es negativo

    def analyze_bet(self, bet: Dict) -> Dict:
        """
        Analiza una sola apuesta.
        bet debe contener: {"event": str, "odd": float, "p_real": float}
        """
        odd = bet["odd"]
        p_real = bet["p_real"]
        ev = self._calc_ev(odd, p_real)
        ev_percent = ev * 100
        edge = self._calc_edge(odd, p_real)
        kelly = self._kelly_fraction(odd, p_real)
        risk = self._calc_risk(odd, p_real)

        classification = True if ev_percent >= (self.min_ev * 100) else False

        return {
            "event": bet.get("event", "Unknown Event"),
            "odd": odd,
            "p_real": round(p_real, 3),
            "EV%": round(ev_percent, 2),
            "Edge%": round(edge, 2),
            "Kelly%": round(kelly * 100, 2),
            "Sigma": risk["Sigma"],
            "CV": risk["CV"],
            "is_worth": classification,
        }

"""
Una apuesta “buena y segura” debería cumplir:
✅ EV% ≥ +5%
✅ Edge > 0
✅ Kelly% > 0
✅ CV < 3 (riesgo moderado)
✅ EV_min (escenario pesimista) > 0

"""
