import csv
import random
import requests
from utils.loger_fucker import LogerFucker
import config.config as config

class ProxyKnight():
    
    def __init__(self):
        """ Decorator para requests que usa Proxies de brightdata.com """
        self.enable_proxy = True        # Funcion aun no programada
        self.test_url = config.TEST_URL
        self.proxy_filename = config.PROXY_FILE_LIST
        self.headers = config.REQUEST_HEADERS
        self.proxies = self._load_proxies()
        self.log = LogerFucker()

    def _load_proxies(self):
        proxies = []
        with open(self.proxy_filename, newline='') as proxy_csv_file:
            filereader = csv.reader(proxy_csv_file, delimiter=',')
            for row in filereader:
                proxies.append(row)
        return proxies

    def get_random_proxy(self) -> dict:
        selected_proxy_data = self.proxies[ random.randint(0, len(self.proxies)) ] # Obtenemos un proxy de la lista con un indice aleatorio

        user = selected_proxy_data[0]
        password = selected_proxy_data[1]
        domain = selected_proxy_data[2]
        port = selected_proxy_data[3]
        
        return {
            'http': f'http://{user}:{password}@{domain}:{port}',
            'https': f'http://{user}:{password}@{domain}:{port}'
        }

    def get(self, url:str, params:dict = None, headers:dict = None) -> requests.Request:
        try:
            self.log.debug(f"Ejecutando request ({url})")
            req = requests.get(
                url, 
                headers= headers or self.headers,
                proxies= self.get_random_proxy(),
                params= params
                )
            return req
        except requests.exceptions.ProxyError:
            self.log.error("ProxyError")
        except requests.exceptions.ConnectionError:
            self.log.error("ConnectionError")
        except requests.exceptions.InvalidURL:
            self.log.error("InvalidURL")
        except:
            pass