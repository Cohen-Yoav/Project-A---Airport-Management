from hy_observer import Observer
from hy_subject import Subject
import time
from typing import List
from hy_clock import Clock


class Simulator(Subject, Observer):
    def __init__(self):
        self._timer = 0
        self._current_start_time = 0.0
        self._current_action = ""
        self._current_plane = 0
        self._current_action_duration = 0
        self._Finished_Actions = False
        self._start_sim = True
        self._observers: List[Observer] = []
        self._pause_flag = False
        self.clock = Clock()

        
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
            if time.time() - self._timer >= self._current_start_time:# + action_duration/ mission_duration:
                # print(f'time - ', time.time() - self._timer)
                # print(f'action - ', self._current_action)
                # print(f'plane num - ', self._current_plane)
                # print(f'action start time - ', self._current_start_time)
                # print("")
                
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
            self._current_start_time = float(subject.start_time_ws[subject.index]) / float(subject.skew)
            self._current_action = subject.actions[subject.index]
            self._current_plane = int(subject.pl_number_no_ws[subject.index])
            
            # print(self._current_action)
            # print(self._current_plane)
            # print(self._current_action + str(self._current_plane))
            
            
        if self._start_sim == True:
            self._start_sim = False
            self.run_simulator()
            
if __name__ == "__main__":    
    pass     