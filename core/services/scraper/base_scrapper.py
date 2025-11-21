from abc import ABC, abstractmethod
from config.config import REQUEST_HEADERS
from utils.loger_fucker import LogerFucker

class Base_Scrapper(ABC):

    def __init__(self, url, req_limit):
        self.base_url = url
        self.headers = REQUEST_HEADERS
        self.log = LogerFucker()
        self.limit = req_limit

    @abstractmethod
    def fetch_data(self):
        """ Obtiene todos los datos de la url"""
        pass

    @abstractmethod
    def parse_data(self, raw_data):
        """ Procesa y estructura los datos obtenidos """
        pass

    def run(self):
        
        raw_data = self.fetch_data()
        
        return self.parse_data(raw_data)
    