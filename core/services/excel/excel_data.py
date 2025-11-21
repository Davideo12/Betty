from openpyxl import load_workbook

def obtener_bankroll(nombre_archivo: str, hoja:str, celda:str) -> float:
    """
    Devuelve el bankroll a partir de los datos de excel
    """
    wb = load_workbook(nombre_archivo, data_only=True)
    
    hoja = wb[hoja]

    return hoja[celda].value

