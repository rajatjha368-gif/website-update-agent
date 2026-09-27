from abc import ABC,abstractmethod
class BaseMonitor(ABC):
 @abstractmethod
 def scan(self,site):...
