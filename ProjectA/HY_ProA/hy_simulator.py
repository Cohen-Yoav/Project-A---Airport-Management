from hy_observer import Observer
from hy_subject import Subject
import time
from typing import List
from hy_Node import Graph

class Simulator(Subject, Observer):
    def __init__(self):
        self._timer = 0
        self._current_start_time = 0.0
        self._current_action = ""
        self._current_plane = 0
        self._Finished_Actions = False
        self._start_sim = True
        self._observers: List[Observer] = []
        self._pause_flag = False
        self.stn_graph = Graph()                # This line was written by Hodaya Cohen Adiv Kavod !
        
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
            
    def run_simulator(self):
        self._timer = time.time()
        
        while True:            
            if time.time() - self._timer >= self._current_start_time:
                # print(f'time - ', time.time() - self._timer)
                # print(f'action - ', self._current_action)
                # print(f'plane num - ', self._current_plane)
                # print(f'action start time - ', self._current_start_time)
                # print("")
                
                # in this point we finished the current action and we need to update the graph 
                self.stn_graph.vert_dict[self._current_action + str(self._current_plane)].action_ended = True
                self.notify()
                
            if self._Finished_Actions == True:
                return
            while self._pause_flag == True:
                pass
                
    def update(self, subject):
        
        # print(f'Simulator update - timer = ', self._timer)
        # print("")
        
        self._Finished_Actions = subject._Finished_Actions
        if self._Finished_Actions == False:
            self._current_start_time = float(subject.start_time_ws[subject.index])
            self._current_action = subject.actions[subject.index]
            self._current_plane = int(subject.pl_number_no_ws[subject.index])
            
            # check with graph if the action parents are done
            # only then we can start doing the action
            print(self._current_action)
            print(self._current_plane)
            print(self._current_action + str(self._current_plane))
            print(self.stn_graph.vert_dict[self._current_action + str(self._current_plane)])
            self.stn_graph.vert_dict[self._current_action + str(self._current_plane)].check_if_parents_done()
            
            
        if self._start_sim == True:
            self._start_sim = False
            self.run_simulator()
            
if __name__ == "__main__":    
    pass     