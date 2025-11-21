from utils.loger_fucker import LogerFucker
from abc import ABC, abstractmethod

class BaseStep(ABC):

    def __init__(self):
        self.log = LogerFucker()

    @abstractmethod
    def run():
        pass