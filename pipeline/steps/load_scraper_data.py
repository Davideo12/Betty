from pipeline.steps.setp import BaseStep
from core.services.scraper.scraper_factory import ScraperFactory

class LoadScraperDataStep(BaseStep):

    def __init__(self):
        self.scraper = ScraperFactory()

    def run(self, context):
        fixtures = self.scraper.get_data()

        context["scraped_fixtures"] = fixtures
        return context
    