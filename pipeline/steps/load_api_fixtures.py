from core.services.api.odds_api import Odds_API
from pipeline.steps.setp import BaseStep

class LoadAPIFixturesStep(BaseStep):

    def __init__(self):
        self.api = Odds_API()

    def run(self, context):
        context["api_fixtures"] = []
        

        fixtures_list = self.api.get_fixtures_by_sport_id(10)   # Tomamos solo los partidos de futbol

        # Ignoramos todos los partidos que esten en vivo o que ya se jugaron
        for fixture in fixtures_list:            
            context["api_fixtures"].append(fixture)

        return context
