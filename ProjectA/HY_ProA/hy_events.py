from hy_clock import SingletonMeta
from hy_observer import Observer
from typing import List

class events(metaclass=SingletonMeta):
    events = []
    def __init__(self):
        self.events = [False for i in range(9)]
        self.events[self.EventToIntger("sa")] = []
        self.events[self.EventToIntger("fa")] = []
        self.observers: List[Observer] = []
        
    def set_event(self, name, val):
        if name == "sa":
            self.events[self.EventToIntger(name)].append(val)
        elif name == "fa":
            self.events[self.EventToIntger(name)].append(val)
        else:
            self.events[self.EventToIntger(name)] = val
            
        if self.events[self.EventToIntger("cd")] == True and self.events[self.EventToIntger("sd")] == True:
            self.notify()
    
    def get_event_val(self, name):
        if name == "sa" and len(self.events[self.EventToIntger(name)]) != 0:
            return self.events[self.EventToIntger(name)].pop(0)
        elif name == "sa" and len(self.events[self.EventToIntger(name)]) == 0:
            return False
        elif name == "fa" and len(self.events[self.EventToIntger(name)]) != 0:
            return self.events[self.EventToIntger(name)].pop(0)
        elif name == "fa" and len(self.events[self.EventToIntger(name)]) == 0:
            return False
        return self.events[self.EventToIntger(name)]
    
    @staticmethod    
    def IntgerToEvent(argument):
        switcher = {
            0: "sa"         ,     # Controller sent action to simulator 
            1: "cena"       ,     # Clock event no action
            2: "cfa"        ,     # Simulator Clock finished action
            3: "fa"         ,     # Simulator finished action
            4: "cd"         ,     # Controller done
            5: "sd"         ,     # Simulator done
            6: "rand"       ,     # Random noise
            7: "rp"         ,     # Replaning - False is no replaning, number mean replaning
            8: "test"       ,     # Test done - True mean test is done, False mean regurlar test, number mean replaning
        }
        return switcher.get(argument, "nothing")
    
    @staticmethod
    def EventToIntger(argument):
        switcher = {
            "sa"    : 0,      # Controller sent action to simulator 
            "cena"  : 1,      # Clock event no action
            "cfa"   : 2,      # Simulator Clock finished action
            "fa"    : 3,      # Simulator finished action
            "cd"    : 4,      # Controller done
            "sd"    : 5,      # Simulator done
            "rand"  : 6,      # Random noise
            "rp"    : 7,      # Replaning
            "test"  : 8,      # Test done - True mean test is done, False mean regurlar test, number mean replaning
        }
        return switcher.get(argument, -1)
    
    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        self.observers.append(observer)
    
    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        pass

    def notify(self):
        """
        Notify all observers about an event.
        """
        for observer in self.observers:
            observer.update(self) 
    
    def update(self, subject):
        """
        Receive update from subject.
        """
        pass
    
    def Clear(self):
        self.events = [False for i in range(9)]
        self.events[self.EventToIntger("sa")] = []
        self.events[self.EventToIntger("fa")] = []
        
if __name__ == "__main__":
    pass