from hy_observer import Observer
import heapq
from hy_events import events

class Simulator(Observer):
    def __init__(self):
        self.heap = []
        self.finished_node = None
        self.signals = events()
                
    def update(self, subject):
        curr_node = self.signals.get_event_val("sa")
        duration = self.signals.get_event_val("rand")
        
        if duration != False and curr_node != False:
            print("Added {} time units to action {}".format(duration, curr_node))
            curr_node.sorted_time += duration
            self.signals.set_event("rand", False)
            
        if self.signals.get_event_val("cena") == False:
            for node in self.heap:
                node.sorted_time -= subject.epsilon
            
        while curr_node != False:
            heapq.heappush(self.heap, curr_node)
            print("Simulator started - {}, time is - {}".format(curr_node, subject.value))
            curr_node = self.signals.get_event_val("sa")
        
        
        if len(self.heap) == 0:
            if self.signals.get_event_val("cd") == True:
                print("Simulator Done")
                self.signals.set_event("sd", True)
            return
        
        while self.heap[0].sorted_time <= subject.zero:
            self.finished_node = heapq.heappop(self.heap)
            self.signals.set_event("fa", self.finished_node)
            self.signals.set_event("cfa", True)
            print("action done - {}, time is - {}".format(self.finished_node, subject.value))
            if len(self.heap) == 0:
                break
            
        self.signals.set_event("cena", False)
        
    def Clear(self):
        self.heap.clear()
        self.finished_node = None
            
if __name__ == "__main__":    
    pass     