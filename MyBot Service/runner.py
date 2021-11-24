import multiprocessing
import os
def executemain():
    os.system('python MyBot.py')

def manage_mod():
    os.system('python manage-mod.py')

def memes():
    os.system('python memes.py')

def musicPlayer():
    os.system('python musicPlayer.py')

def interface():
    os.system('python interface.py')

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=executemain)
    p2 = multiprocessing.Process(target=manage_mod)
    p3 = multiprocessing.Process(target=memes)
    p4 = multiprocessing.Process(target=musicPlayer)
    p5 = multiprocessing.Process(target=interface)

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
