from hy_conroller import Controller
from hy_simulator import Simulator
from hy_state import MyState
import time

if __name__ == "__main__":
    cont = Controller()
    sim = Simulator()
    state = MyState(10)

    cont.attach(sim)
    sim.attach(state)
    sim.attach(cont)

    cont.update(sim)