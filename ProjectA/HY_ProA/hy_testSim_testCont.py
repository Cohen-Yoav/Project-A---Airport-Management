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
    signals = events()
    clock = Clock(signals)
    sim = Simulator()
    signals.attach(clock)
    
    sorted_files = []
    config_path = "ProjectA/BT_ProA/configs/"
    log_path = "ProjectA/BT_ProA/logs/"
    
    configs = os.listdir(config_path)
    logs = os.listdir(log_path)
    idx_num = [int(i[6:-4]) for i in configs]
    
    for i in range(len(configs)):
        config_name = str(configs[i])
        log_name = str(logs[i])
        config_file_path = os.path.join(config_path, config_name)
        log_file_path = os.path.join(log_path, log_name)
        if os.stat(log_file_path).st_size != 0:
            sorted_files.append([configs[i], config_file_path, logs[i], log_file_path, idx_num[i]])
    sorted_files = sorted(sorted_files, key=lambda x: x[4])
        
    for (cfg, log) in zip([i[1] for i in sorted_files], [i[3] for i in sorted_files]):
        print(cfg, end="\n\n")
        config = config_file(cfg, 'r')
        cont = Controller(config, log)
        state = MyState(10, config)
        inter = Interrupt()

        clock.attach(cont)
        clock.attach(sim)
        clock.attach(state)
        cont.attach(inter)

        clock.run_clock()
        
        # clean up at aisle 6
        clock.Clear()
        sim.Clear()
        signals.Clear()