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
            print("")
            print("Added {} time units to action {}".format(duration, curr_node))
            print("")
            curr_node.sorted_time += duration
            self.signals.set_event("rand", False)
            
        for node in self.heap:
            node.sorted_time -= subject.epsilon
            
        while curr_node != False:
            heapq.heappush(self.heap, curr_node)
            print("Simulator started - {}, time is - {}".format(curr_node, subject.value))
            curr_node = self.signals.get_event_val("sa")
        self.signals.set_event("ra", True)
        
        
        if len(self.heap) == 0:
            if self.signals.get_event_val("cd") == True:
                print("Simulator Done")
                print("")
                self.signals.set_event("sd", True)
            return
        
        while self.heap[0].sorted_time <= subject.zero:
            self.finished_node = heapq.heappop(self.heap)
            self.signals.set_event("fa", self.finished_node)
            print("action done - {}, time is - {}".format(self.finished_node, subject.value))
            print("") 
            if len(self.heap) == 0:
                break
        
        
        # while self.heap[0].sorted_time <= 0:
        #     self.finished_node = heapq.heappop(self.heap)
        #     self.signals.set_event("fa", self.finished_node)
        #     print("action done - {}, time is - {}".format(self.finished_node, subject.value))
        #     print("")
        #     if len(self.heap) == 0:
        #         break
        
        
        # print("sim")
        # # update all actions - V
        # # insert new action - V
        # # pop finished action and raise signal - V
        # # call notify - V
        
        # if self.signals.get_event_val("sa") == 1:
        #     heapq.heappush(self.heap, subject.curr_node)
        #     self.signals.set_event("sa", False)
        #     self.signals.set_event("ra", True)
            
            
        # for node in self.heap:
        #     node.sorted_time -= self.clock.epsilon
        # # self.signals.set_event("sta", True)
        # self.clock.sleep_epsilon()
        
        # if len(self.heap) == 0:
        #     if self.signals.get_event_val("cd") == True:
        #         print("Simulator Done")
        #         self.signals.set_event("sd", True)
        #         self.notify()
        
        # elif self.heap[0].sorted_time <= 0 and self.signals.get_event_val("raf") == True:
        #     self.finished_node = heapq.heappop(self.heap)
        #     self.signals.set_event("fa", self.finished_node.id)
        #     self.signals.set_event("raf", False)
        
        # self.notify()
            
if __name__ == "__main__":    
    pass     