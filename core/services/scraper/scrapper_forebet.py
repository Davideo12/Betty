from bs4 import BeautifulSoup
from core.services.scraper.base_scrapper import Base_Scrapper
from core.services.proxy.proxy_knight import ProxyKnight

class Scrapper_Forebet(Base_Scrapper):

    def _get_match_data(self, url:str) -> dict:        
        try: 
            data = {}   # En este diccionario se va guardando toda la informacion scrapeada
            res = self.knight.get(self.base_url + url)

            if res is not None:
                if res.status_code == 200:
                    html = res.text
                else:
                    self.log.error(f"Error GET Status: {res.status_code} - {url}")
            else:
                self.log.error(f"No se pudo completar la solicitud a {url}")

            soup = BeautifulSoup(html, "html.parser")

            # Obtenemos el nombre del partido (Los equipos enfrentados)
            name = soup.find("h1").get_text()
            data["event"] = str(name)

            # Obtenemos el promedio de goles de cada partido
            avg_gol = soup.select_one(".rcnt .avg_sc").get_text()
            data["avg_goals"] = float(avg_gol)

            # Obtenemos la seguridad de la prediccion 
            pred = soup.select_one(".predict").get_text()
            data["prediction"] = pred

            # Obtenemos marcador exacto
            ex_sc = soup.select_one(".rcnt .ex_sc").get_text()
            data["expected_score"] = ex_sc

            # Obtenemos la liga
            leage = soup.select_one(".leagpred_btn").get_text()
            data["league"] = str(leage)

            prob_1x2 = str(soup.select_one(".rcnt .fprc").get_text())
            
            data["home_win"] =  int( prob_1x2[:2])/100
            data["draw"] =  int( prob_1x2[2:4])/100
            data["away_win"] =  int( prob_1x2[4:])/100

            # Registramos el equipo local y el visitante usando el nombre del evento
            data["participant1Name"], data["participant2Name"] = [t.strip() for t in name.split("-")]

            return data
        
        except Exception as e:
            self.log.debug(f"Error {e}")
    

    def fetch_data(self) -> dict:
        self.log.info("Obteniendo informacion de Forebet...")

        url = self.base_url + "/es/predicciones-para-hoy"
        self.knight = ProxyKnight()
        res = self.knight.get(url)

        html = ""
        if res.status_code == 200:
            html = res.text
        else:
            self.log.error(f"Error GET Status: {html.status_code} - {url}")

        soup = BeautifulSoup(html, "html.parser")

        # Obtenemos la url de cada evento
        matches_url_list = []

        rows = soup.select(".rcnt .tnmscn")
        
        count = 0
        for element in rows:
            text = element['href']
            try:
                if count < self.limit or None:
                    matches_url_list.append(str(text))
                    count += 1 
            except ValueError:
                continue  # Ignora si no se puede convertir   

        data_list = []

        time_to_wait = float(( len(matches_url_list) * 5 ) /60)

        self.log.info(f"Se obtendran {len(matches_url_list)} elementos... ({time_to_wait:.2f} min)")
        for url in matches_url_list:
            match_data = self._get_match_data(url)
            data_list.append(match_data)

        return data_list

    
    def parse_data(self, raw_data:dict) -> dict:
        return raw_data
            