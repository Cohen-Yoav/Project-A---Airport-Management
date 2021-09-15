import time
from hy_observer import Observer
from hy_config import config_file
from hy_clock import Clock

"""
A State describe the current conditions of all the planes and lanes in the problem.
State is a mutable object.
"""
class MyState(Observer):
    
    """
    c`tor of State
        @requires fuel_delta != None
        @modifies 
        @effects Creates a new State with self.fuel_delta
    """
    def __init__(self, fuel_delta):
        
        self.config = config_file('ProjectA/BT_ProA/configs/config0.txt', 'r')
        self.num_of_planes = int(self.config.num_of_planes)
        self.num_of_lanes = int(self.config.num_of_lanes)
        self.planes_vector = [0 for i in range(self.num_of_planes)]
        self.lanes_vector = [-1 for i in range(self.num_of_lanes)]
        self.airspace = False
        self.fuel_delta = fuel_delta
        self.current_taken_lanes = 0
        self.clock = Clock()
        
    def print_state(self):
        
        print(f'num of planes:', self.num_of_planes)
        # print(f'Plane List:', self.planes_vector[:])
        action_list = [self.IntgerToAction(element) for element in self.planes_vector ]
        print(f'Plane List:', action_list[:])
        
        print(f'num of lanes:', self.num_of_lanes)
        print(f'Lane List:', self.lanes_vector[:])
        print(f'AirSpace is:',self.airspace)
    
    def UpdateState(self, PlaneIndex, action):
                
        if action == "sctto" or action == "sl":
            for i in range(self.num_of_lanes):
                if self.lanes_vector[i] == -1:
                    self.lanes_vector[i] = PlaneIndex
                    self.current_taken_lanes += 1
                    break;
                    #curr_plane_taken counter!!!
                    
        if action == "eto" or action == "et":
            for i in range(self.num_of_lanes):
                if self.lanes_vector[i] == PlaneIndex:
                    self.lanes_vector[i] = -1
                    self.current_taken_lanes -= 1
                    break;
                    
        if action == "sto" or action=="sl":
            self.airspace = True
        
        if action == "sm" or action=="st":
            self.airspace = False
                    
        self.planes_vector[PlaneIndex] = self.ActionToIntger(action)
        
        return self
        
    @staticmethod
    def IntgerToAction(argument):
        switcher = {
            0: "idle",      # Start State  
            1: "sctto",     # Start clear to take off
            2: "ectto",     # End clear to take off
            3: "sto",       # Start take off
            4: "eto",       # End take off
            5: "sm",        # Start Mission 
            6: "em",        # End Mission 
            7: "sl",        # Start Landing
            8: "el",        # End Landing
            9: "st",        # Start Taxi
            10: "et",       # End Taxi
            11: "done",     # Final state
        }
        return switcher.get(argument, "nothing")
    
    @staticmethod
    def ActionToIntger(argument):
        switcher = {
            "idle"  : 0,        # Start State  
            "sctto" : 1,        # Start clear to take off
            "ectto" : 2,        # End clear to take off
            "sto"   : 3,        # Start take off
            "eto"   : 4,        # End take off
            "sm"    : 5,        # Start Mission 
            "em"    : 6,        # End Mission 
            "sl"    : 7,        # Start Landing
            "el"    : 8,        # End Landing
            "st"    : 9,        # Start Taxi
            "et"    : 10,       # End Taxi
            "done"  : 11,       # Final state
        }
        return switcher.get(argument, -1)
    
    def StateToConfig(self):
        # how do we take the time in to account?
        
        new_config = open('ProjectA/BT_ProA/configs/config1.txt','w')
        new_config.write('number_of_planes = ' + str(self.num_of_planes) + '\n')
        new_config.write('number_of_lanes = ' + str(self.num_of_lanes) + '\n')
        new_config.write('max_run_time = ' + str(self.config.max_run_time) + '\n')
        
        for i in range(self.num_of_planes):
            status = self.planes_vector[i]
            start_day_min = self.config.config_line_lst[i].start_day_min
            start_day_max = self.config.config_line_lst[i].start_day_max
            mission_duration = self.config.config_line_lst[i].mission_duration
            max_fuel = self.config.config_line_lst[i].max_fuel
            end_day = self.config.config_line_lst[i].end_day
        
            if self.planes_vector[i] < 4:
                status = 1
            elif self.planes_vector[i] > 7:
                # to be continued- 42 :)
                continue
            else:
                status = 5
                
            new_config.write('plane' + str(i) + '    ' + start_day_min + '   ' + start_day_max + '   ' + 
                             mission_duration + '   ' + max_fuel + '   ' + end_day + '   ' + str(status) + '\n')
        
        new_config.close()
        
    def update(self, subject):
        self.UpdateState(subject._current_plane, subject._current_action)
        # self.print_state()
        # self.StateToConfig()
        # print("")
        
if __name__ == "__main__":
    pass
    # ms = MyState(5)
    # ms.print_state()
