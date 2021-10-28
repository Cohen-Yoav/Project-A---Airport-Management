from hy_observer import Observer
from hy_subject import Subject
import heapq
from hy_events import events
from typing import List

class Simulator(Observer, Subject):
    def __init__(self):
        self.heap = []
        self.finished_node = None
        self.curr_node = None
        self.signals = events()
        self.observers: List[Observer] = []
                
    def update(self, subject):
        # get the current node from the begining of the list
        self.curr_node = self.signals.get_event_val("sa")
        # get the value of the interrupt
        duration = self.signals.get_event_val("rand")
        
        # check if there is a node and an interrupt 
        if duration != False and self.curr_node != False:
            print("Added {} time units to action {}".format(duration, self.curr_node))
            self.curr_node.sorted_time += duration
            self.signals.set_event("rand", False)
        
        # if there was a clock event, reduce time unit from each node    
        if self.signals.get_event_val("cena") == False:
            for node in self.heap:
                node.sorted_time -= subject.epsilon
        
        # insert new nodes to the heap    
        while self.curr_node != False:
            heapq.heappush(self.heap, self.curr_node)
            print("Simulator started - {}, time is - {}".format(self.curr_node, subject.value))
            self.notify(self) # update state
            self.curr_node = self.signals.get_event_val("sa")
        
        
        if len(self.heap) == 0:
            if self.signals.get_event_val("cd") == True:
                print("Simulator Done")
                self.signals.set_event("sd", True)
            return
        
        while self.heap[0].sorted_time <= subject.zero:
            self.finished_node = heapq.heappop(self.heap)
            self.notify(self) # update state
            self.signals.set_event("fa", self.finished_node)
            self.signals.set_event("cfa", True)
            print("action done - {}, time is - {}".format(self.finished_node, subject.value))
            if len(self.heap) == 0:
                break
            
        self.signals.set_event("cena", False)
        
    def Clear(self):
        self.heap.clear()
        self.finished_node = None
        

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
            
if __name__ == "__main__":    
    pass     