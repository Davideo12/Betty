from pipeline.steps.setp import BaseStep
from core.services.api.odds_api import Odds_API
import time

class GetOddsAPIStep(BaseStep):

    def __init__(self, limit_requests:int = 0):
        super().__init__()
        self.api = Odds_API()
        self.limit_requests = limit_requests


    def run(self, context):
        context["fixtures_with_odds"] = []

        time_to_wait = (len(context["sync_teams"]) * 4) / 60

        self.log.info(f"Obteniendo cuotas de {len(context['sync_teams'])} equipos. ({time_to_wait:.2f} min)")

        for fixture in context["sync_teams"][:self.limit_requests or None]:
            try:
                odds = self.api.get_odds_by_fixture_id( fixture["fixtureId"] )
                odds = odds["bookmakerOdds"]["stake"]

                fixture['odds'] = odds.get("markets")

                context["fixtures_with_odds"].append(fixture)
            except Exception as e:
                self.log.debug(f"From {self.__class__.__name__} : Error : {e}")

            time.sleep(3)   # Tiempo de espera entre request definido por la API

        return context

    
"""
Market code:

101:                1X2
    101 : Home wins
    102 : Draw
    103 : Away wins



104:                Ambos marcan
    104 : Si
    105 : No




106:                Totales
    106 : 0.5 over
    107 : 0.5 under

10162:
    10162 : 1 over
    10163 : 1 under

10164:
    10164 : 1.25 over
    10165 : 1.25 under

108:
    108 : 1.5 over
    109 : 1.5 under

10166:
    10166 : 1.75 over
    10167 : 1.75 under

10168:
    10168 : 2 over
    10169 : 2 under

10170:
    10170 : 2.25 over 
    10171 : 2.25 under

10172:
    10172: 2.75 over
    10173: 2.75 under

1010:
    1010 : 2.5 over
    1011 : 2.5 under

10174:
    10174 : 3 over
    10175 : 3 under

1012:
    1012 : 3.5 over
    1013 : 3.5 under

1014:
    1014 : 4.5 over
    1015 : 4.5 under


1060:               Handicap
    1060 : -1.5 Home
    1061 : 1.5  Away

1068:
    1068 : -0.5 Home
    1069 : 0.5  Away

1076:
    1076 : 0.5  Home
    1077 : -0.5 Away


"101": {
    "outcomes": {
    "101": {
        "players": {
        "0": {
            "active": true,
            "betslip": null,
            "bookmakerOutcomeId": null,
            "changedAt": "2025-11-06T14:56:53.738451+00:00",
            "limit": null,
            "playerName": null,
            "price": 1.81,
            "exchangeMeta": {}
        }
        }
    },
    "102": {
        "players": {
        "0": {
            "active": true,
            "betslip": null,
            "bookmakerOutcomeId": null,
            "changedAt": "2025-11-06T14:56:53.738451+00:00",
            "limit": null,
            "playerName": null,
            "price": 3.05,
            "exchangeMeta": {}
        }
        }
    },
    "103": {
        "players": {
        "0": {
            "active": true,
            "betslip": null,
            "bookmakerOutcomeId": null,
            "changedAt": "2025-11-06T14:41:54.749076+00:00",
            "limit": null,
            "playerName": null,
            "price": 4.1,
            "exchangeMeta": {}
        }
        }
    }
    },
    "bookmakerMarketId": null
},



"""