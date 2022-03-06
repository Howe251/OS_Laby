from tkinter import *
import threading
from time import sleep, time
from random import randint
from tkinter import messagebox

start_time = time()
philosophers = 5
forks_count = philosophers
stop = False

forks = []
for i in range(forks_count):
    forks.append(threading.Lock())


def check_thread():
    work = False
    global procs
    for proc in procs:
        if proc.is_alive():
            work = True
    return work


def eat(left, right, i):
    p = True
    while p:
        while left.locked() or right.locked():
            sleep(1)
        if not left.locked() and not right.locked():
            left.acquire()
            right.acquire()
            try:
                print(f"{threading.currentThread().name} {i+1} ест \n", end="")
                sleep(randint(5, 10))
                print(f"{threading.currentThread().name} {i+1} закончил есть \n", end="")
            finally:
                left.release()
                right.release()
                sleep(1)
        if time() - start_time > 30 or stop:#5 * 60:
            p = False
            print(f"{threading.currentThread().name} {i+1} Процесс завершен")
            if not stop:
                window.c.itemconfigure(window.phil[i], text=f"   {threading.currentThread().name} {i+1} завершен",
                                       fill="#652828")


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('300x180')
        self.title("Философы")
        self.btn = []
        self.phil = []
        self.c = Canvas(width=280, height=100)
        self.c.place(x=0, y=70)
        for i in range(philosophers):
            self.btn.append(Button(self, text="           ", bg="green", activebackground="green"))
            self.btn[i].grid(row=1, column=i)
            self.phil.append(self.c.create_text((85, 10 + i * 20), text=f"Философ №{i} запущен", fill="#652828"))
        self.lbl = Label(self, text="")
        self.lbl.place(x=2, y=40)
        self.update()
        self.after(1, self.updater)

    def updater(self):
        self.u = threading.Thread(target=self.upd, name="Update")
        self.u.daemon = True
        self.u.start()

    def upd(self):
        while check_thread():
            for i, fork in enumerate(forks):
                if fork.locked():
                    self.btn[i].configure(bg='red')
                else:
                    self.btn[i].configure(bg='green')
                self.update()
            sleep(0.5)
        if threading.main_thread().is_alive():
            self.lbl.configure(text="Философы наелись. Окно можно закрыть")

    def on_close(self):
        if check_thread():
            if messagebox.askokcancel("Выйти", "Философы не закночили есть.\nДействительно выйти?"):
                self.lbl.configure(text="Ожидание завершения потоков")
                self.update()
                global stop
                stop = True
                while check_thread():
                    pass
                self.destroy()
        else:
            self.destroy()


if __name__ == "__main__":
    procs = []
    window = Window()
    for i in range(philosophers):
        procs.append(threading.Thread(target=eat, name="Философ №", args=(forks[i], forks[(i+1)%philosophers], i)))
    for proc in procs:
        proc.start()
    window.protocol("WM_DELETE_WINDOW", window.on_close)
    window.mainloop()
