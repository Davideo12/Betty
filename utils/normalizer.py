import unicodedata
import re

# Palabras comunes que no aportan valor al nombre del equipo
STOPWORDS = {"fc", "cf", "se", "srl", "sp", "ac", "sc", "u23", "u20", "jr", "club", "team", "deportes", "sport", "athletic", "athletico", "rj", "mg"}

def normalize_team_name(team_name: str) -> str:
    """Normaliza el nombre de un equipo"""
    
    # lowercase
    name = team_name.lower()

    # remove accents
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')

    # remove punctuation
    name = re.sub(r"[^a-z0-9\s]", "", name)

    # tokenize
    tokens = name.split()

    # remove stopwords
    tokens = [t for t in tokens if t not in STOPWORDS]

    # return normalized string
    return " ".join(tokens).strip()
