from hy_events import events
from hy_clock import Clock
from hy_conroller import Controller
from hy_simulator import Simulator
from hy_state import MyState
from hy_Interrupt import Interrupt
from hy_config import config_file
import os
import sys


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from BT_ProA import Main as mbt

"""
This is the main test that activate the Controller, Simulator and State modules
"""

def make_log_path(index):
    here = os.path.dirname(os.path.realpath(__file__))
    subdir = "Logs"
    log_path = here + "\\" + subdir        
    log_name = "log_output" + str(index) + ".txt"
    filepath = os.path.join(log_path, log_name)
    
    return filepath

def Clear_replan_files():
    config_path = "ProjectA/BT_ProA/configs/"
    log_path = "ProjectA/BT_ProA/logs/"
    configs = os.listdir(config_path)
    logs = os.listdir(log_path)
    for cfg in configs:
        lst = cfg.split(".")
        if len(lst) > 2:
            config_file_path = os.path.join(config_path, cfg)
            os.remove(config_file_path)
    for log in logs:
        lst = log.split(".")
        if len(lst) > 2:
            log_file_path = os.path.join(log_path, log)
            os.remove(log_file_path)

if __name__ == "__main__":
    
    # create the Clock, events and simulator modules
    signals = events()
    clock = Clock(signals)
    sim = Simulator()
    # subscribe the clock module to the events - clock is listening on events
    signals.attach(clock)
    
    Clear_replan_files()
    
    # create a list of all config and log files
    sorted_files = []
    config_path = "ProjectA/BT_ProA/configs/"
    log_path = "ProjectA/BT_ProA/logs/"
    
    # import all config and log files created by B&T module
    configs = os.listdir(config_path)
    logs = os.listdir(log_path)
    idx_num = [int(i[6:-4]) for i in configs]
    
    # go over all config and log files - if log file is empty skip (B&T didn't find solution)
    for i in range(len(configs)):
        config_name = str(configs[i])
        log_name = str(logs[i])
        config_file_path = os.path.join(config_path, config_name)
        log_file_path = os.path.join(log_path, log_name)
        if os.stat(log_file_path).st_size != 0:
            sorted_files.append([configs[i], config_file_path, logs[i], log_file_path, idx_num[i]])
    sorted_files = sorted(sorted_files, key=lambda x: x[4])
    
    # for each config and log file that has a valid plan run our project
    for (cfg, log, index) in zip([i[1] for i in sorted_files], [i[3] for i in sorted_files], [i[4] for i in sorted_files]):
        if index != 0:
            continue
        print(index)
        
        while True:
            
            # check if test is done or replaning is needed
            Test = signals.get_event_val("test")
            if Test == True:
                break
            elif Test != False: # replaning using the offline program
                index = Test
                print("Started Replaning for config file {} !".format(index))
                
                mbt.main(index) # running the offline program with the new config file
                cfg = os.path.join(config_path, "config" + str(index) + ".txt")       
                log = os.path.join(log_path, "log_output_" + str(index) + ".txt") 
                
                if os.stat(log_file_path).st_size == 0: # replaning failed
                    print("Replaning Failed !")
                    break
                    
                # clean up at aisle 6
                clock.Clear()
                sim.Clear()
                signals.Clear()     
                        
            
            # open log_file for our program
            filepath = make_log_path(str(index))

            new_log = open(filepath,'w')
            config = config_file(cfg, str(index), 'r')
            state = MyState(0.1, config)
            cont = Controller(config, log, state)
            inter = Interrupt()

            clock.attach(cont)
            clock.attach(sim)
            sim.attach(state)
            cont.attach(inter)

            cont.SetLogFile(new_log)
            sim.SetLogFile(new_log)
            state.SetLogFile(new_log)

            clock.run_clock()
        
        # clean up at aisle 6
        clock.Clear()
        sim.Clear()
        signals.Clear()
    
    
