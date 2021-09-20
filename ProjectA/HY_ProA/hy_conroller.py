from hy_observer import Observer
from typing import List
from hy_subject import Subject
from hy_Node import Graph
from hy_config import config_file
from hy_events import events
import heapq

action_duration: int = 10
action_ending: float = 0.001

class Controller(Observer, Subject):
    
    def __init__(self):
        
        # check with graph if the action parents are done - TODO Hַ&Y
        # in this point we finished the current action and we need to update the graph    
        self.stn_graph = Graph()
        self.config = config_file('ProjectA/BT_ProA/configs/config0.txt', 'r')

        self.heap = list(self.stn_graph.vert_dict.values())
        heapq.heapify(self.heap)
        
        self.curr_node = None
        self.signals = events()
        
        self.observers: List[Observer] = []
        
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
        # check if conroller is done
        if len(self.heap) == 0:
            self.signals.set_event("cd", True)
            return
        
        # check for finished actions from the simulator
        finished_node = self.signals.get_event_val("fa")
        while finished_node != False:
            id = finished_node.id
            self.stn_graph.vert_dict[id].action_ended = True
            finished_node = self.signals.get_event_val("fa")
        
        # check for next action if ready
        while int(self.heap[0].sorted_time) <= subject.value and self.heap[0].check_if_parents_done():
            self.curr_node = heapq.heappop(self.heap)
            print("Current Node - {}, time is - {}".format(self.curr_node, subject.value))
            self.SetNodeRunTime(subject.epsilon)
            self.signals.set_event("sa", self.curr_node)
            self.notify()
            if len(self.heap) == 0:
                break
                
        for node in self.heap:
            if int(node.sorted_time) <= subject.value and not node.check_if_parents_done():
                node.sorted_time += subject.epsilon
        
        heapq.heapify(self.heap)
            
        # tmp_node = self.signals.get_event_val("fa")
        # while tmp_node != False:
        #     self.stn_graph.vert_dict[tmp_node.id].action_ended = True
        #     tmp_node = self.signals.get_event_val("fa")
        #     self.signals.set_event("raf", True)
        
        
        # # check if we finished all actions
        # # check if simulator recieved an action
        # if self.signals.get_event_val("ra") == True:
        #     self.signals.set_event("ra", False)
        #     if len(self.heap) == 0:
        #         self.signals.set_event("cd", True)
        #         print("Done - {}".format(self.clock.get_cur_time()))
                
        #     # check if heap[0] time has passed and all parents are done 
        #     elif float(self.heap[0].sorted_time) <= self.clock.get_cur_time() and self.heap[0].check_if_parents_done():
        #         self.curr_node = heapq.heappop(self.heap)
        #         print("Current Node - {}, time is - {}".format(self.curr_node, self.clock.get_cur_time()))
        #         self.SetNodeRunTime()
        #         #raise signal start action "sa"
        #         self.signals.set_event("sa", True) 
                
        #     # check if heap[0] time has passed and not all parents are done 
        #     elif float(self.heap[0].sorted_time) <= self.clock.get_cur_time() and not self.heap[0].check_if_parents_done():
        #         print("Added {} time to heap[0] {}".format(self.clock.epsilon, self.heap[0]))
        #         self.heap[0].sorted_time += self.clock.epsilon  #TODO maybe add delay to children
        #         self.clock.sleep_epsilon()
        #         heapq.heapify(self.heap)
                  
    def SetNodeRunTime(self, skew):
        if self.curr_node.action == "sm":
            pl_number = int(self.curr_node.pl_num)
            self.curr_node.sorted_time = int(self.config.config_line_lst[pl_number].mission_duration) * skew
        elif self.curr_node.action[0] == "e":
            self.curr_node.sorted_time = action_ending * skew
        else:
            self.curr_node.sorted_time = action_duration * skew
        
if __name__ == "__main__":    
    pass