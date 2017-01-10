"""
Test for sending lambda to another interpreter with multiprocessing.
"""

from multiprocessing import Process

from pickleablelambda import pickleable   # pylint: disable=import-error


if __name__ == '__main__':

    def test():
        """Lambda send as pickled object."""
        lam = lambda x: [print(y) for y in range(int(x))]
        proc = Process(target=pickleable(lam), args=(int(1e4),))
        proc.start()
        print("process started...")
        proc.join()
        print("process finished")

    test()
