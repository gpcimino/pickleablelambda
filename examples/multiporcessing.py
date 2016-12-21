from multiprocessing import Process
from pickablelambda import pickable

if __name__ == '__main__':
    L = lambda x: [print(y) for y in range(int(x))]
    p = Process(target=pickable(L), args=(int(1e4),))
    p.start()
    print("process started...")
    p.join()
    print("process finished")