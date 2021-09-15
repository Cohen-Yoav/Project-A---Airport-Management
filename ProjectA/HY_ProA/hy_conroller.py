from hy_observer import Observer
from hy_subject import Subject
from typing import List
from hy_Node import Graph
from hy_clock import Clock
import heapq

class Controller(Observer, Subject):
    
    def __init__(self):
        
        self._Finished_Actions = False
        self._observers: List[Observer] = []
        self.clock = Clock()
        self.stn_graph = Graph()
        self.heap = list(self.stn_graph.vert_dict.values())
        heapq.heapify(self.heap)
        
        self.curr_node = None
        self.signal = None
        
        # check with graph if the action parents are done - TODO Hַ&Y
        # in this point we finished the current action and we need to update the graph 
    
    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        self._observers.append(observer)
    
    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        pass

    def notify(self):
        """
        Notify all observers about an event.
        """
        for observer in self._observers:
            observer.update(self)     
    
    def update(self, subject):
        # if len(self.heap) == 0:
        #       self._Finished_Actions = True
        # elif self.heap[0].sorted_time >= clock.get_cur_time() && self.heap[0].check_if_pearnts_done():
        #       self.curr_node = pop self.heap[0]
        #       raise signal start action "sa" / self.signal = EventToIntger("sa")
        # elif self.heap[0].sorted_time >= clock.get_cur_time() && not self.heap[0].check_if_pearnts_done():
        #       self.heap[0].sorted_time += 1  #TODO maybe add delay to children
        #       heapq.heapify(self.heap)
        self.notify()
        
        
    def IntgerToEvent(argument):
        switcher = {
            0: "sa" ,     # Controller sent action to simulator 
            1: "ra" ,     # Simulator recieved action from conroller
            2: "sta",     # Simulator starting action
            3: "fa" ,     # Simulator finished action
            4: "raf",     # Controller recieved action finished from simulator
        }
        return switcher.get(argument, "nothing")
    
    def EventToIntger(argument):
        switcher = {
            "sa"  : 0,      # Controller sent action to simulator 
            "ra"  : 1,      # Simulator recieved action from conroller
            "sta" : 2,      # Simulator starting action
            "fa"  : 3,      # Simulator finished action
            "raf" : 4,      # Controller recieved action finished from simulator
        }
        return switcher.get(argument, -1)
    
if __name__ == "__main__":    
    mycont = Controller()
    print(mycont.heap)     