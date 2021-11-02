from hy_events import events
from hy_clock import Clock
from hy_conroller import Controller
from hy_simulator import Simulator
from hy_state import MyState
from hy_Interrupt import Interrupt
from hy_config import config_file
import os

"""
This is the main test that activate the Controller, Simulator and State modules
"""

if __name__ == "__main__":
    
    # create the Clock, events and simulator modules
    signals = events()
    clock = Clock(signals)
    sim = Simulator()
    # subscribe the clock module to the events - clock is listening on events
    signals.attach(clock)
    
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
        print(cfg, end="-------------------\n")
        config = config_file(cfg, str(index), 'r')
        state = MyState(0.001, config)
        cont = Controller(config, log, state)
        inter = Interrupt()

        clock.attach(cont)
        clock.attach(sim)
        sim.attach(state)
        cont.attach(inter)

        clock.run_clock()
        
        # clean up at aisle 6
        clock.Clear()
        sim.Clear()
        signals.Clear()