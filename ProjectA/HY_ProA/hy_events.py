from hy_clock import SingletonMeta
from hy_observer import Observer
from typing import List

class events(metaclass=SingletonMeta):
    events = []
    def __init__(self):
        self.events = [False for i in range(8)]
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
            0: "sa"  ,     # Controller sent action to simulator 
            1: "ra"  ,     # Simulator recieved action from conroller
            2: "sta" ,     # Simulator starting action
            3: "fa"  ,     # Simulator finished action
            4: "raf" ,     # Controller recieved action finished from simulator
            5: "cd"  ,     # Controller done
            6: "sd"  ,     # Simulator done
            7: "rand",     # Random noise
        }
        return switcher.get(argument, "nothing")
    
    @staticmethod
    def EventToIntger(argument):
        switcher = {
            "sa"  : 0,      # Controller sent action to simulator 
            "ra"  : 1,      # Simulator recieved action from conroller
            "sta" : 2,      # Simulator starting action
            "fa"  : 3,      # Simulator finished action
            "raf" : 4,      # Controller recieved action finished from simulator
            "cd"  : 5,      # Controller done
            "sd"  : 6,      # Simulator done
            "rand": 7,      # Random noise
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
    
if __name__ == "__main__":
    pass