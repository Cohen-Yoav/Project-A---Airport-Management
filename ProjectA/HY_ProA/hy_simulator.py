from hy_observer import Observer
from hy_subject import Subject
import heapq
from hy_events import events
from typing import List

class Simulator(Observer, Subject):
    def __init__(self):
        self.heap = []
        # self.finished_node = None
        self.curr_node = None
        self.action_started = False # False action finished, True action started
        self.signals = events()
        self.observers: List[Observer] = []
        self.log_file = None
                
    def update(self, subject):
        # get the current node from the begining of the list
        self.curr_node = self.signals.get_event_val("sa")
        # get the value of the interrupt
        duration = self.signals.get_event_val("rand")
        
        # check if there is a node and an interrupt 
        if duration != False and self.curr_node != False:
            self.log_file.write("Simulator: Added {} time units to action {}\n".format(duration / subject.epsilon, self.curr_node))
            self.curr_node.sorted_time += duration
            self.signals.set_event("rand", False)
        
        # if there was a clock event, reduce time unit from each node    
        if self.signals.get_event_val("cena") == False:
            for node in self.heap:
                node.sorted_time -= subject.epsilon
                # add one time unit to the air time of the plane
                if node.action == "sm":
                    node.air_time += 1 #TODO should this be +epsilon?
                    
        
        # insert new nodes to the heap    
        while self.curr_node != False:
            heapq.heappush(self.heap, self.curr_node)
            self.log_file.write("Simulator: started - {}, time is - {}\n".format(self.curr_node, subject.value))
            self.action_started = True
            self.notify() # update state
            self.curr_node = self.signals.get_event_val("sa")
        
        
        if len(self.heap) == 0:
            if self.signals.get_event_val("cd") == True:
                # self.log_file.write("Simulator Done\n")
                self.signals.set_event("sd", True)
            return
        
        while self.heap[0].sorted_time <= subject.zero:
            self.curr_node = heapq.heappop(self.heap)
            self.action_started = False
            self.notify() # update state
            self.signals.set_event("fa", self.curr_node)
            self.signals.set_event("cfa", True)
            self.log_file.write("Simulator: action done - {}, time is - {}\n".format(self.curr_node, subject.value))
            if len(self.heap) == 0:
                break
            
        self.signals.set_event("cena", False)
        
    def Clear(self):
        self.heap.clear()
        self.observers.clear()
        self.curr_node = None
        

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
            
    def SetLogFile(self, log):
        self.log_file = log
            
if __name__ == "__main__":    
    pass     