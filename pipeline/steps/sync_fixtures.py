from pipeline.steps.setp import BaseStep
from utils.teams_sync import TeamSync
from datetime import datetime
from zoneinfo import ZoneInfo

class SyncFixturesStep(BaseStep):

    def _eliminar_repetidos_por_evento(self, lista_diccionarios):
        """
        Elimina elementos repetidos en una lista de diccionarios 
        usando la clave 'evento' como identificador único.
        """
        vistos = set()
        resultado = []
        for item in lista_diccionarios:
            evento = item.get("event")
            if evento not in vistos:
                vistos.add(evento)
                resultado.append(item)
        return resultado

    def run(self, context):
        ahora_cdmx = datetime.now(ZoneInfo("America/Mexico_City"))

        api_data = context["api_fixtures"]
        scraped_data = context["scraped_fixtures"]

        context["sync_teams"] = []

        if len(api_data) <= 1:
            self.log.error(f"No hay datos de la API: len = {len(api_data)}")
            exit()

        for i in range(len(api_data)):
            compared_fixture = api_data[i]
            for current_fixture in scraped_data:
                ts = TeamSync(current_fixture, compared_fixture)
                data = ts.sync()

                if data is not None and data["hasOdds"] == True:
                    # Convertir de ISO 8601 (UTC)
                    fecha_utc = datetime.fromisoformat(data.get("startTime").replace("Z", "+00:00"))
                    # Convertir a hora local de Ciudad de México
                    fecha_cdmx = fecha_utc.astimezone(ZoneInfo("America/Mexico_City"))
                    data["startTime"] = str(fecha_cdmx)

                    if fecha_cdmx > ahora_cdmx:
                        context["sync_teams"].append(data)
                    else:
                        continue
                    
                    context["sync_teams"].append(data)
                    

        context["sync_teams"] = self._eliminar_repetidos_por_evento(context["sync_teams"])

        if len(context["sync_teams"]) > 1:
            return context
        else:
            self.log.warning("No hay partidos proximos")
            exit()