from hy_state import MyState

"""
This test check the state module
"""

def test():
    mystate = MyState(3, 2, 10)
    mystate.print_state()
    print('')
    
    mystate.UpdateState(1,0)
    mystate.print_state()
    print('')

if __name__ == "__main__":
    test()