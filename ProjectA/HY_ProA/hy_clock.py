from threading import Lock, Thread
import time

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Clock(metaclass=SingletonMeta):
    value = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self) :
        self.value = time.time()

    def set_curr_time(self):
        self.value = time.time()
    
    def get_cur_time(self):
        return time.time() - self.value


def test_singleton(value: str) -> None:
    clock = Clock()
    print(clock.value)
    time.sleep(5)
    clock.set_curr_time()
    print(clock.value)


if __name__ == "__main__":
    # The client code.

    print("If you see the same value, then singleton was reused (yay!)\n"
          "If you see different values, "
          "then 2 singletons were created (booo!!)\n\n"
          "RESULT:\n")

    process1 = Thread(target=test_singleton, args=("1",))
    # process2 = Thread(target=test_singleton, args=("2",))
    process1.start()
    # process2.start()