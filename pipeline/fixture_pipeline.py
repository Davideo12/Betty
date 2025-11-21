from utils.loger_fucker import LogerFucker

class FixturePipeline:

    def __init__(self, steps:list):
        self.steps = steps
        self.log = LogerFucker()

    def run(self, context:dict = None):
        if context is None:
            context = {}

        for step in self.steps:
            self.log.info(f"Corriendo [ {step.__class__.__name__} ]")
            context = step.run(context)

        return context
    
"""
Flujo de la cadena de responsabilidades:
1. Load API Fixtures
2. Load Scraped Fixtures
3. Normalize Names
4. Sync Fixtures
5. Get Odds
6. Calculate Bet
7. Filter Good Bets and Bad Bets
"""