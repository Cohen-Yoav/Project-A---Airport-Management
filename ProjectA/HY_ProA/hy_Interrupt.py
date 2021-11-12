import random
from hy_observer import Observer
from hy_events import events
from hy_clock import Clock

class Interrupt(Observer):
    def __init__(self):
        # number of actions to count before doing intterupt
        self.action_count = 0
        self.duration = 0
        self.signals = events()
        self.clock = Clock()
        self.shuffle()
    
    def update(self, subject):
        if subject.curr_node.id == "sto0":
            self.signals.set_event("rand", 131.54 * self.clock.epsilon)
            return
        self.action_count -= 1
        if self.action_count == 0:
            action_duration = subject.curr_node.sorted_time
            self.duration = random.uniform(action_duration / 2, action_duration)
            # print("------------interrupt duration is {}".format(self.duration))
            self.signals.set_event("rand", self.duration)
            self.shuffle()
            
    def shuffle(self):
        self.action_count = random.randrange(1,4)