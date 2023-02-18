# Python program showing
# abstract base class work
 
from abc import ABC, abstractmethod
 
class Nodos(ABC):
 
    @abstractmethod
    def GetAllNodos(self):
        pass

    @abstractmethod
    def SaveNodo(self):
        pass

    @abstractmethod
    def GetNodoById(self):
        pass

    @abstractmethod
    def UpdateNodo(self):
        pass    