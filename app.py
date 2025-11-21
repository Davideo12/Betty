from pipeline.fixture_pipeline import FixturePipeline
from pipeline.steps.load_api_fixtures import LoadAPIFixturesStep
from pipeline.steps.load_scraper_data import LoadScraperDataStep
from pipeline.steps.normalize_names import NormalizeNamesStep
from pipeline.steps.sync_fixtures import SyncFixturesStep
from pipeline.steps.get_api_odds import GetOddsAPIStep
from pipeline.steps.format_fixtures import FormatFixtureStep
from pipeline.steps.calculate_bet import CalculateBetStep
from pipeline.steps.save_data import SaveDataStep
from pipeline.steps.create_pdf_report import CreatePDFReport
from utils.loger_fucker import LogerFucker
import time

log = LogerFucker()
log.set_debug(False)

log.print_banner()

def build_fixture_pipeline():
    return FixturePipeline([
        LoadAPIFixturesStep(),
        LoadScraperDataStep(),
        NormalizeNamesStep(),
        SyncFixturesStep(),
        GetOddsAPIStep(limit_requests=100),
        FormatFixtureStep(),
        CalculateBetStep(),
        SaveDataStep(),
        CreatePDFReport()
    ])

log.info("Ejecutando Pipeline...")
time.sleep(5)

pipeline = build_fixture_pipeline()
result = pipeline.run()