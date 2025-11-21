from pipeline.steps.setp import BaseStep
from config.config import BETS_JSON_PATH
from datetime import datetime
import json

class SaveDataStep(BaseStep):

    def run(self, context):
        fixture_list = context["good_bets"]

        try:
            filename = f"apuestas_{datetime.now().strftime('%Y-%m-%d')}.json"
            with open(f"{BETS_JSON_PATH}{filename}", "w", encoding="utf-8") as file:
                json.dump(fixture_list, file, indent=4, ensure_ascii=False)
                file.close()

                self.log.success(f"Apuestas almacenadas en {BETS_JSON_PATH}{filename}.json")

        except Exception as e:
            self.log.error("No se logro escribir el archivo")
            self.log.error(e)

        return context