from pipeline.steps.setp import BaseStep
from utils.normalizer import normalize_team_name

class NormalizeNamesStep(BaseStep):

    def run(self, context):
        
        for fixture in context["scraped_fixtures"]:
            try:
                fixture["participant1Name"] = normalize_team_name(fixture["participant1Name"])
                fixture["participant2Name"] = normalize_team_name(fixture["participant2Name"])
            except:
                continue

        for fixture in context["api_fixtures"]:
            try:
                fixture["participant1Name"] = normalize_team_name(fixture["participant1Name"])
                fixture["participant2Name"] = normalize_team_name(fixture["participant2Name"])
            except:
                continue

        return context
