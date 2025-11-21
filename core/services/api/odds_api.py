from utils.loger_fucker import LogerFucker
from datetime import date, timedelta
import config.config as config
import requests


class Odds_API:

    def __init__(self):
        self.url = config.ODDS_API_URL
        self.api_key = config.ODDS_API_KEY 
        self.bookmaker = "stake"  # Obtenido de la API. Hardcodeado para no hacer requests de mas
        self.headers = {}
        self.from_date = date.today().strftime("%Y-%m-%d") # Obtiene la fecha de hoy
        self.to_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d") # Obtiene la fecha de mañana
        self.sport_id = 10

        self.log = LogerFucker()

    def get_tournaments_by_sport(self, sport_id:int = 10) -> list:
        """Obtenemos la lista de torneos | sport_id = 10 (futbol)"""
        self.sport_id = sport_id

        try:
            req = requests.get(
                f"{self.url}/v4/tournaments", 
                headers= self.headers,
                params= { 
                    "apiKey": self.api_key,
                    "sportId": sport_id,
                    "language": "en"
                }
            )

            return req.json()
        
        except requests.exceptions.ConnectionError:
            self.log.error(f"Error conectando a la API ({self.url})")

        except Exception as e:
            self.log.error("No se logro obtener informacion de /fixtures con la API")
            self.log.error(e)

    def get_fixtures_by_tournament_id(self, tournament_id:int) -> list:
        """Obtenemos los partidos que habra a usando el id del torneo"""

        try:
            req = requests.get(
                f"{self.url}/v4/fixtures", 
                headers= self.headers,
                params= {
                    "apiKey": self.api_key,
                    "tournamentId": tournament_id,
                    "sportId": self.sport_id,
                    "from": self.from_date,
                    "to": self.to_date
                }
            )

            return req.json()
        
        except requests.exceptions.ConnectionError:
            self.log.error(f"Error conectando a la API ({self.url})")

        except Exception as e:
            self.log.error("No se logro obtener informacion de /fixtures con la API")
            self.log.error(e)

    def get_fixtures_by_participant_id(self, participant_id:int) -> list:
        """Obtenemos los partidos de un equipo especifico"""
        try:
            req = requests.get(
                f"{self.url}/v4/fixtures", 
                headers= self.headers,
                params= {
                    "apiKey": self.api_key,
                    "participantId": participant_id,
                    "sportId": self.sport_id,
                    "from": self.from_date,
                    "to": self.to_date
                }
            )

            return req.json()
        
        except requests.exceptions.ConnectionError:
            self.log.error(f"Error conectando a la API ({self.url})")

        except Exception as e:
            self.log.error("No se logro obtener informacion de /fixtures con la API")
            self.log.error(e)

    def get_fixtures_by_sport_id(self, sport_id:int) -> list:
        """Obtenemos los partidos de un deporte especifico"""
        self.sport_id = sport_id

        try:
            req = requests.get(
                f"{self.url}/v4/fixtures", 
                headers= self.headers,
                params= {
                    "apiKey": self.api_key,
                    "sportId": sport_id,
                    "from": self.from_date,
                    "to": self.to_date
                }
            )
            
            return req.json()
        
        except requests.exceptions.ConnectionError:
            self.log.error(f"Error conectando a la API ({self.url})")

        except Exception as e:
            self.log.error("No se logro obtener informacion de /fixtures con la API")
            self.log.error(e)

    def get_odds_by_fixture_id(self, fixture_id:str):
        """ Obtenemos las cuotas de un partido usando su id"""
        try:
            req = requests.get(
                    f"{self.url}/v4/odds", 
                    headers= self.headers,
                    params={
                        "apiKey": self.api_key,
                        "fixtureId":fixture_id,
                        "bookmakers":self.bookmaker,
                    }
                )
            
            return req.json()
        
        except requests.exceptions.ConnectionError:
            self.log.error(f"Error conectando a la API ({self.url})")

        except Exception as e:
            self.log.error("No se logro obtener informacion de /fixtures con la API")
            self.log.error(e)

    def get_past_fixture_result_by_id(self, fixture_id:str):
        """ Obtenemos los resultados de liquidacion para todos los mercados disponibles en un evento especifico"""
        try:
            req = requests.get(
                    f"{self.url}/v4/settlements", 
                    headers= self.headers,
                    params={
                        "apiKey": self.api_key,
                        "fixtureId":fixture_id
                    }
                )
            
            return req.json()
        
        except requests.exceptions.ConnectionError:
            self.log.error(f"Error conectando a la API ({self.url})")

        except Exception as e:
            self.log.error("No se logro obtener informacion de /fixtures con la API")
            self.log.error(e)
        




"""
Get toutnaments
{
    "tournamentId": 329,
    "tournamentSlug": "copa-del-rey",
    "tournamentName": "Copa del Rey",
    "categorySlug": "spain",
    "categoryName": "España",
    "futureFixtures": 0,
    "upcomingFixtures": 12,
    "liveFixtures": 18
}

get fixtures by sport id
{
    "fixtureId": "id1003238364983156",
    "participant1Id": 702067,
    "participant2Id": 702081,
    "sportId": 10,
    "tournamentId": 32383,
    "seasonId": null,
    "statusId": 2,
    "hasOdds": false,
    "startTime": "2025-10-30T14:00:00.000Z",
    "trueStartTime": "2025-10-30T14:02:04.165Z",
    "trueEndTime": "2025-10-30T15:55:05.090Z",
    "updatedAt": "2025-10-30T15:55:05.090Z",
    "externalProviders": {
        "betradarId": 64983156,
        "mollybetId": null,
        "opticoddsId": null,
        "lsportsId": null,
        "txoddsId": null,
        "sofascoreId": null,
        "betgeniusId": null,
        "flashscoreId": null,
        "pinnacleId": null,
        "oddinId": null
    },
    "participant1Name": "SE Palmeiras SP SRL",
    "participant2Name": "LDU Quito SRL",
    "sportName": "Soccer",
    "tournamentSlug": "copa-libertadores-srl",
    "categorySlug": "simulated-reality-league",
    "categoryName": "Simulated Reality League",
    "tournamentName": "Copa Libertadores SRL"
}
"""