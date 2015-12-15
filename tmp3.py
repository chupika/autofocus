import tkinter as tk

class App:
    
    def __init__(self):
        self.root = tk.Tk()
        self.main = MainWin(self.root)
        self.main.btchoose.bind("<Button-1>", self.choose)
        App.wincenter(self.root)
        self.root.mainloop()
        
    def choose(self, event):
        self.slave = tk.Toplevel(self.root)
        self.slave.grab_set()
        self.secwin = ChooseWin(self.slave)
        App.wincenter(self.slave)

    def wincenter(win):
        win.update_idletasks()
        w = win.winfo_screenwidth()
        w = win.winfo_screenwidth()
        h = win.winfo_screenheight()
        size = tuple(int(_) for _ in win.geometry().split('+')[0].split('x'))
        x = int(w / 2 - size[0] / 2)
        y = int(h / 2 - size[1] / 2)
        win.geometry("{}x{}+{}+{}".format(size[0], size[1], x, y))

        
class MainWin:
    
    def __init__(self, master):
        self.master = master
        self.width = 500
        self.height = 500
        self.master.geometry('{}x{}'.format(self.width, self.height))
        self.btchoose = tk.Button(self.master, text='Choose!')
        self.btchoose.pack()


class ChooseWin:
    
    def __init__(self, master):
        self.master = master
        self.width = 800
        self.height = 200
        self.master.geometry('{}x{}'.format(self.width, self.height))


app = App()