from hy_observer import Observer
from hy_subject import Subject
from typing import List

class Controller(Observer, Subject):
    def __init__(self):
        
        self.index = -1
        self._Finished_Actions = False
        self._observers: List[Observer] = []
        
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
        if self.index >= len(self.actions): #TODO FIXME h & y - נראלי סבבה, רק צריך לבדוק את הפעולה האחרונה, אם היא מודפסת (שלא מפספסים)
            self._Finished_Actions = True
        self.notify()
        
    
# אירוע שכל ההורים שלו סיימו - אפשר לדחות.
# אבל צריך לבדוק מבחינת זמן, אם זה מסתדר שם.
# אירוע שההורים שלו לא סיימו - אי אפשר לדחות אותו, וצריך לדחות הורה?
if __name__ == "__main__":    
    pass     