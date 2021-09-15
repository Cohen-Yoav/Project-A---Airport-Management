from hy_conroller import Controller
from hy_simulator import Simulator
from hy_state import MyState
import time

"""
This is the main test that activate the Controller, Simulator and State modules
"""

if __name__ == "__main__":
    cont = Controller()
    sim = Simulator()
    state = MyState(10)

    cont.attach(sim)
    sim.attach(state)
    sim.attach(cont)

    print(cont.clock.get_cur_time())
    time.sleep(5)
    print(sim.clock.get_cur_time())
    cont.update(sim)