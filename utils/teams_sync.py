from rapidfuzz import fuzz

class TeamSync():
    """ Sincronizamos objetos con los mismos equipos enfrentados y creamos un nuevo objeto fusionado"""
    def __init__(self, dict_1, dict_2):
        self.dict_1 = dict_1
        self.dict_2 = dict_2
        self.threshold = 85

    def _match_teams(self, name_1:str, name_2:str) -> bool:
        score = fuzz.token_set_ratio(name_1, name_2)
        return score >= self.threshold # mayor que el limite

    def sync(self) -> dict:
        try:
            if self._match_teams(self.dict_1["participant1Name"], self.dict_2["participant1Name"]) and self._match_teams(self.dict_1["participant2Name"], self.dict_2["participant2Name"]):
                # Combinamos los diccionarios. Si hay conflictos de claves gana el dict_2
                return {**self.dict_1, **self.dict_2} 
            else:
                return None
        except:
            pass

