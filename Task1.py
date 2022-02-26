import threading
from time import sleep
from random import randint


def eat(right, left):
    forks[right].acquire()
    forks[left].acquire()
    print(f"{threading.currentThread().name} {right+1} ест \n", end="")
    sleep(randint(5, 10))
    print(f"{threading.currentThread().name} {right+1} закончил есть \n", end="")
    forks[left].release()
    forks[right].release()


philosophers = 5
forks_count = philosophers

forks = []
for i in range(forks_count):
    forks.append(threading.Lock())

procs = []
for i in range(philosophers):
    left_hand = i
    right_hand = (i+1) % philosophers
    proc = threading.Thread(target=eat, name="Философ №", args=(left_hand, right_hand))
    procs.append(proc)
    proc.start()