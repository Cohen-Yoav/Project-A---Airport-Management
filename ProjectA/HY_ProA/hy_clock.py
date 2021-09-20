import time
from hy_observer import Observer
from typing import List
from threading import Lock
from hy_subject import Subject
from hy_observer import Observer

class SingletonMeta(Subject, Observer, type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Clock(metaclass=SingletonMeta):
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, events) :
        # value - how many time units has passed - int
        self.value = -1
        # epsilon - this is the time unit - float
        self.epsilon = 0.001
        # observers - list of followeres
        self.observers: List[Observer] = []
        # Done - bollean to say if conroller and simulator are done
        self.Done = False
        # 
        self.zero = self.epsilon / 100
        #
        self. signals = events
        
    def sleep_epsilon(self):
        time.sleep(self.epsilon)
    
    def run_clock(self):
        while True:
            # if no action is done in this cycle 
            if self.signals.get_event_val("cfa") == False:
                self.value += 1
                self.sleep_epsilon()
            # if there was an action
            else:
                self.signals.set_event("cfa", False)
                self.signals.set_event("cena", True)
                
            if self.Done == True:
                print("all done :)")
                break
            self.notify()
        
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
        self.Done = True

if __name__ == "__main__":
    pass