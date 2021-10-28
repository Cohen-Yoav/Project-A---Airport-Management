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
    
    def __init__(self, config, log_output, state):
           
        self.stn_graph = Graph(log_output)
        self.config = config

        self.heap = list(self.stn_graph.vert_dict.values())
        heapq.heapify(self.heap)
        
        self.curr_node = None
        self.signals = events()
        
        self.observers: List[Observer] = []
        self.state = state
        
    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        self.observers.append(observer)
    
    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        self.observers.remove(observer)

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
        
        # check for all actions that are ready and remove from the heap
        for node in self.GetNodes(subject):
            self.curr_node = node
            self.heap.remove(node)
            # print("Current Node - {}, time is - {}".format(self.curr_node, subject.value))
            print("")
            self.SetNodeRunTime(subject.epsilon)
            
            # add a call to legal function
            # if illeagal then we need to replan, else continue
            if self.state.is_leagal(self.curr_node) == False:
                pass
                # add re-planing option here - state_to_config is called here?
                        
            self.signals.set_event("sa", self.curr_node)
            self.notify()
        
        # add time penalty to unfinished nodes
        for node in self.heap:
            if int(node.sorted_time) <= subject.value and not node.check_if_parents_done():
                node.sorted_time += subject.epsilon
        
        heapq.heapify(self.heap)
            
                  
    def SetNodeRunTime(self, skew):
        if self.curr_node.action == "sm":
            pl_number = int(self.curr_node.pl_num)
            self.curr_node.sorted_time = int(self.config.config_line_lst[pl_number].mission_duration) * skew
        # elif self.curr_node.id == "sctto0":
        #     self.curr_node.sorted_time = 50 * skew
        elif self.curr_node.action[0] == "e":
            self.curr_node.sorted_time = action_ending * skew
        else:
            self.curr_node.sorted_time = action_duration * skew
    
    # find all ready nodes to be sent to the simulator        
    def GetNodes(self, subject):
        nodes = []
        for i in range(len(self.heap)):
            if int(self.heap[i].sorted_time) <= subject.value and self.heap[i].check_if_parents_done():
                nodes.append(self.heap[i])
        return nodes
        
if __name__ == "__main__":    
    pass