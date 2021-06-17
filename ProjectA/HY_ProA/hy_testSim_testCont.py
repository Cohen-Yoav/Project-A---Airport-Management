from hy_conroller import Controller
from hy_simulator import Simulator

cont = Controller()
sim = Simulator()

cont.attach(sim)
sim.attach(cont)

cont.update(sim)