from pipeline.steps.setp import BaseStep

class FormatFixtureStep(BaseStep):

    def _format_odds(self, odds):
        formatted_odds = {
            "1X2": {},
            "totales": {},
            "BTTS": {}
        }

        # --- Helper para obtener precios ---
        def get_price(section, outcome):
            try:
                return odds[section]["outcomes"][outcome]["players"]["0"]["price"]
            except KeyError:
                return None

        # --- 1X2 ---
        outcomes_1x2 = {
            "1": ("101", "101"),
            "X": ("101", "102"),
            "2": ("101", "103"),
        }
        for label, (section, outcome) in outcomes_1x2.items():
            price = get_price(section, outcome)
            if price is not None:
                formatted_odds["1X2"][label] = price

        # --- totales ---
        totals_map = {
            "0.5": "106",
            "1": "10162",
            "1.25": "10164",
            "1.5": "108",
            "1.75": "10166",
            "2": "10168",
            "2.25": "10170",
            "2.5": "1010",
            "2.75": "10172",
            "3": "10174",
            "3.5": "1012"
        }

        for line, section in totals_map.items():
            over = get_price(section, section)
            under = get_price(section, str(int(section) + 1))
            if over: 
                formatted_odds["totales"][f"{line} over"] = over
            if under: 
                formatted_odds["totales"][f"{line} under"] = under

        # --- BTTS ---
        btts_section = "104"
        formatted_odds["BTTS"]["Yes"] = get_price(btts_section, "104")
        formatted_odds["BTTS"]["No"] = get_price(btts_section, "105")

        return formatted_odds



    def run(self, context):
        context["fixtures"] = []

        for fixture in context["fixtures_with_odds"]:
            odds = fixture["odds"]

            try:
                parsed_data = {
                    "fixture_id": fixture.get("fixtureId"),
                    "event": fixture.get("event"),
                    "league": fixture.get("league"),
                    "fixture_path": odds.get("fixturePath"),
                    "start_time": fixture.get("startTime"),

                    "home_team": fixture.get("participant1Name").title(),
                    "away_team": fixture.get("participant2Name").title(),

                    "predictions": {
                        "avg_goals": float(fixture.get("avg_goals")),
                        "expected_score": fixture.get("expected_score"),
                        "prediction": fixture.get("prediction")
                    },

                    "probabilities": {
                        "home_win": float(fixture.get("home_win")),
                        "draw": float(fixture.get("draw")),
                        "away_win": float(fixture.get("away_win"))
                    },
                    
                    "odds": self._format_odds(odds),
                }

                context["fixtures"].append(parsed_data)
            except Exception as e:
                self.log.debug(f"From {self.__class__.__name__} : Error : {e}")

        return context
            

"""

from services.api.odds_api import Odds_API
from utils.loger_fucker import LogerFucker
import time

class GetOddsAPIStep:

    def __init__(self):
        self.api = Odds_API()
        self.log = LogerFucker()

    def _format_odds(self, odds):
        def safe_get(path, default=None):
            try:
                for key in path:
                    odds_section = odds_section[key]
                return odds_section
            except Exception:
                return default

        formatted_odds = {
            "1X2": {},
            "totales": {},
            "BTTS": {}
        }

        # --- Helper para obtener precios ---
        def get_price(section, outcome):
            try:
                return odds[section]["outcomes"][outcome]["players"]["0"]["price"]
            except KeyError:
                return None

        # --- 1X2 ---
        outcomes_1x2 = {
            "1": ("101", "101"),
            "X": ("101", "102"),
            "2": ("101", "103"),
        }
        for label, (section, outcome) in outcomes_1x2.items():
            price = get_price(section, outcome)
            if price is not None:
                formatted_odds["1X2"][label] = price

        # --- totales ---
        totals_map = {
            "0.5": "106",
            "1": "10162",
            "1.25": "10164",
            "1.5": "108",
            "1.75": "10166",
            "2": "10168",
            "2.25": "10170",
            "2.5": "1010",
            "2.75": "10172",
            "3": "10174",
            "3.5": "1012"
        }

        for line, section in totals_map.items():
            over = get_price(section, section)
            under = get_price(section, str(int(section) + 1))
            if over: 
                formatted_odds["totales"][f"{line} over"] = over
            if under: 
                formatted_odds["totales"][f"{line} under"] = under

        # --- BTTS ---
        btts_section = "104"
        formatted_odds["BTTS"]["Yes"] = get_price(btts_section, "104")
        formatted_odds["BTTS"]["No"] = get_price(btts_section, "105")

        return formatted_odds

    def run(self, context):
        context["fixtures"] = []

        time_to_wait = (len(context["sync_teams"]) * 8) / 60
        self.log.info(f"Obteniendo cuotas de {len(context['sync_teams'])} equipos. ({time_to_wait:.2f} min)")

        for fixture in context["sync_teams"]:
            try:
                odds = self.api.get_odds_by_fixture_id( fixture["fixtureId"] )
                odds = odds["bookmakerOdds"]["stake"]
            except Exception as e:
                self.log.debug(e)

            try:
                parsed_data = {
                    "fixture_id": fixture.get("fixtureId"),
                    "event": fixture.get("event"),
                    "league": fixture.get("leage"),
                    "fixture_path": odds.get("fixturePath"),
                    "start_time": fixture.get("startTime"),

                    "home_team": fixture.get("participant1Name"),
                    "away_team": fixture.get("participant2Name"),

                    "avg_goals": fixture.get("avg_gol"),
                    "expected_score": fixture.get("ex_sc"),
                    "prediction": fixture.get("pred"),

                    "probabilities": {
                        "home_win": fixture.get("home_team_prob"),
                        "draw": fixture.get("draw_prob"),
                        "away_win": fixture.get("away_team_prob"),
                    },
                    
                    "odds": self._format_odds(odds.get("markets")),
                }

                context["fixtures"].append(parsed_data)
            except Exception as e:
                self.log.debug(e)
                self.log.debug(odds)

            time.sleep(4)

        return context

"""