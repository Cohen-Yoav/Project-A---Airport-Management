from hy_events import events
from hy_clock import Clock
from hy_conroller import Controller
from hy_simulator import Simulator
from hy_state import MyState
from hy_Interrupt import Interrupt
import time

"""
This is the main test that activate the Controller, Simulator and State modules
"""

if __name__ == "__main__":
    clock = Clock()
    cont = Controller()
    sim = Simulator()
    state = MyState(10)
    signals = events()
    inter = Interrupt()

    clock.attach(cont)
    clock.attach(sim)
    # clock.attach(state)
    signals.attach(clock)
    cont.attach(inter)

    # print(cont.clock.get_cur_time())
    # time.sleep(5)
    # print(sim.clock.get_cur_time())
    clock.run_clock()