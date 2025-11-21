from core.services.scraper.scrapper_forebet import Scrapper_Forebet
from datetime import date
import config.config as config
import json


class ScraperFactory:

    def __init__(self):
        self.forebet_base_url = "https://www.forebet.com"
        self.scraped_data_path = config.SCRAPED_DATA_PATH

    def _eval_saved_data(self):
        
        with open(self.scraped_data_path, 'r') as file:
            data = json.load(file)

        if data["last_update"] == date.today().strftime("%Y-%m-%d"):
            return data["data"]
        else:   

            scrapper_forebet = Scrapper_Forebet(self.forebet_base_url, req_limit=300)

            data["last_update"] = date.today().strftime("%Y-%m-%d")
            data["data"] = scrapper_forebet.run()

            with open(self.scraped_data_path, 'w') as file:
                json.dump(data, file, indent=4)

            return data["data"]

    def get_data(self):

        return self._eval_saved_data()