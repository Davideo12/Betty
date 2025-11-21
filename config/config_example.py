# CONFIG FILE

DEBUG = True

# Stored API and scraped data route
SCRAPED_DATA_PATH   = "/data/scraped_data.json"
API_DATA_FILE       = "/data/api_data.json"
BETS_JSON_PATH      = "/JSON/"
BETS_PDF_PATH       = "/PDF/"

# API Config

## ODDSPAPI
# https://oddspapi.io/es
ODDS_API_URL    = "https://api.oddspapi.io"     
ODDS_API_KEY    = ""

# Requests config
REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",  # Do Not Track
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}

# Proxy Config
## BrightData
#https://brightdata.com/
# Formato de archivo: username,password,host,port
PROXY_FILE_LIST = ""
TEST_URL        = "https://httpbin.org/ip"