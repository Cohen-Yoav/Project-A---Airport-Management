from hy_observer import Observer
from hy_subject import Subject
from typing import List
from hy_Node import Graph

class Controller(Observer, Subject):
    
    """
    send event to sim - sim respon with event stated
    afte x sec - send event action done
    disturbed - random number
    add PQ by time
    """
    def __init__(self, skew):
        
        self.index = -1
        self._Finished_Actions = False
        self._observers: List[Observer] = []
        
        # check with graph if the action parents are done - TODO Hַ&Y
        # in this point we finished the current action and we need to update the graph 
        self.stn_graph = Graph()                # This line was written by Hodaya Cohen Adiv Kavod !
        self.skew = skew
        
        ### get all the actions from the plan into a list
        log = open('log_output.txt', 'r')
        self.actions = [line.split('_')[1:2][0] for line in log]
        log.close()
        
        ### get all the planes numbers into a list
        log = open('log_output.txt', 'r')
        pl_number = [line.split(':')[0:1] for line in log]
        pl_number_con = [pn[0].split('_')[2:3][0] for pn in pl_number]
        self.pl_number_no_ws = [pnc.replace(" ", "") for pnc in pl_number_con]
        log.close()
        
        ### get all the start time of each action into a list
        log = open('log_output.txt', 'r')
        start_time = [line.split(':')[1:2][0] for line in log]
        self.start_time_ws = [st.strip() for st in start_time]
        log.close()   
    
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
        # print(f'Controller update - index = ', self.index)
        self.index += 1
        if self.index >= len(self.actions): 
            self._Finished_Actions = True
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
    
# אירוע שכל ההורים שלו סיימו - אפשר לדחות.
# אבל צריך לבדוק מבחינת זמן, אם זה מסתדר שם.
# אירוע שההורים שלו לא סיימו - אי אפשר לדחות אותו, וצריך לדחות הורה?
if __name__ == "__main__":    
    pass     