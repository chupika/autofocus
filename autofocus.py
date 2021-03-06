###############################################################################
import tkinter as tk
from tkinter import messagebox
#For working with getting instance WritingPad and Entry from pickle file
from autofocuso import WritingPad, Entry
import autofocuso as af

class Autofocus:
    
    def __init__(self, db, root):
        self.db = db
        self.root = root
        self.root.title("Autofocus")
        self.main = MainWin(self.root, self, db)
        Autofocus.wincenter(self.root)
        
    def choose(self):
        if self.db.chosen == -1:
            self.slave = tk.Toplevel(self.root)
            self.slave.grab_set()
            self.secwin = ChooseWin(self.slave, self, self.db)
            Autofocus.wincenter(self.slave)

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

    def __init__(self, master, parent, db):
        self.master = master
        self.parent = parent
        self.db = db
        self.shift_active = []
        self.master.resizable(width=tk.FALSE, height=tk.FALSE)

        self.lbox      = tk.Listbox(self.master, height=20, width=50,
                                    activestyle = 'none', bg='#FFD699', font='Consolas')
        self.inputbox  = tk.Entry(self.master)
        self.inputrefbox  = tk.Entry(self.master)
        self.btchoose  = tk.Button(self.master, text='Choose!',
                                   command=parent.choose,
                                   bg='#BBB', fg = 'black', width=15)
        self.btchooseq = tk.Button(self.master, text='Choose quick!',
                                   command=self.push_chooseq,
                                   bg='#777', fg = 'white')
        self.btdone    = tk.Button(self.master, text='Done!',
                                   command=self.push_done,
                                   bg='#777', fg = 'white')
        self.btcont    = tk.Button(self.master, text='Continue later',
                                   command=self.push_contin_later,
                                   bg='#777', fg = 'white')
        self.btturn    = tk.Button(self.master, text ='Turn the page!',
                                   command=self.push_turn,
                                   bg='#444', fg = 'white')
        self.btadd     = tk.Button(self.master, text='Add',
                                   command=self.push_add,
                                   bg='#777', fg = 'white')
        self.btpgnext  = tk.Button(self.master, text=">",
                                   command=lambda: self.shift_page(where='next'))
        self.btpgprev  = tk.Button(self.master, text="<",
                                   command=lambda: self.shift_page(where='prev'))
        self.btpgcur   = tk.Button(self.master, text="^",
                                   command=lambda: self.shift_page(where='curr'))
        self.status    = tk.Label(self.master, text="", bd=1,
                                  relief=tk.SUNKEN, anchor=tk.W)
        
        self.lbox.grid     (rowspan=6, column=0, sticky=tk.W+tk.E,
                            padx=5, pady=5)
        self.inputbox.grid (row=6, column=0, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        self.inputrefbox.grid (row=7, column=0, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        
        self.btpgprev.grid (row=5, column=1, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        self.btpgcur.grid  (row=5, column=2, sticky=tk.W+tk.E+tk.N+tk.S,
                            pady=5)
        self.btpgnext.grid (row=5, column=3, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        
        self.btchoose.grid (row=0, column=1, columnspan=3,
                            sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        self.btchooseq.grid(row=4, column=1, columnspan=3,
                            sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        self.btdone.grid   (row=2, column=1, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        self.btcont.grid   (row=3, column=1, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        self.btturn.grid   (row=1, column=1, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        self.btadd.grid    (row=6, column=1, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S,
                            padx=5, pady=5)
        self.status.grid(row=8, columnspan=4, sticky=tk.W+tk.E)
        self.inputbox.bind('<Return>', lambda event: self.push_add())
        self.lbox.bind('<Double-1>', lambda event: self.copy_ref())
        self.filllb()

    def filllb(self, ipage=None):
        self.lbox.delete(0, tk.END)
        if ipage != None:
            index = ipage
        elif self.db.active:
            index = self.db.active[0]
        else:
            index = 0
        if self.db.active:
                for i, task in enumerate(self.db.pages[index]):
                    if (task.reference):
                        self.lbox.insert(i, '{: <.44}  ref'.format(task.text))
                    else:
                        self.lbox.insert(i, task.text)
                    if i == self.db.chosen and (ipage == None or ipage == self.db.active[0]):
                        self.lbox.itemconfig(i, bg='#317332', fg='white')
                    else:
                        if task.status:
                            self.lbox.itemconfig(i, bg='#FFD699', fg='white')
                        else:
                            self.lbox.itemconfig(i, bg='#FFD699', fg='black')
        self.status.config(text=str("{}/{}".format(index, len(self.db.pages))))


    def push_chooseq(self):
        if self.lbox.curselection():
            self.db.choose(self.lbox.curselection()[0])
        self.filllb()

    def push_done(self):
        if self.db.chosen > -1:
            self.db.do()
            self.db.chosen = -1
            self.filllb()

    def push_contin_later(self):
        if self.db.chosen > -1:
            self.db.contin_later()
            self.db.chosen = -1
            self.filllb()

    def push_turn(self):
        if (len(self.db.active) != 1 and self.db.chosen == -1):
            if db.status:
                self.db.turn_the_page()
                self.filllb()
            else:
                if tk.messagebox.askyesno("Warning!", af.MSG_CAN_KILL):
                    self.kill_page()
                    self.db.turn_the_page()
                    self.filllb()
        else:
            tk.messagebox.showwarning("Warning!", af.MSG_CANT_TURN)

    def push_add(self):
        msg = self.inputbox.get().strip()
        ref = self.inputrefbox.get().strip()
        if msg:
            self.db.add(msg, ref)
            af.backup(db)
            self.filllb()
        self.inputbox.delete(0, tk.END)
        self.inputrefbox.delete(0, tk.END)

    def shift_page(self, where="next"):
        """
        where arg can be 'next', 'prev', 'curr'
        """
        if not self.db.active:
            return
        if where == 'curr':
            self.shift_active[:] = []
            self.filllb()
            return
        if not self.shift_active:
            self.shift_active[:] = self.db.active
        if where == 'next':
            self.shift_active.append(self.shift_active.pop(0))
        else:
            self.shift_active.insert(0, self.shift_active.pop())
        self.filllb(ipage=self.shift_active[0])

    def copy_ref(self):
        if self.lbox.curselection():
            index_selected_task_on_page = self.lbox.curselection()[0]
            if self.shift_active:
                index_showed_page = self.shift_active[0]
                ref_selected_task = self.db.pages[index_showed_page][index_selected_task_on_page].reference
            else:
                ref_selected_task = self.db.pages[self.db.active[0]][index_selected_task_on_page].reference
            
            self.master.clipboard_clear()
            self.master.clipboard_append(ref_selected_task)


class ChooseWin:
    
    def __init__(self, master, parent, db):
        self.master = master
        self.parent = parent
        self.db = db
        self.act_ts = self.db.get_act_ts()
        self.i = 0
        self.labchoose = tk.Label(self.master, text='', width=50, height=5,
                                  font=("Helvetica", 16))
        self.btchooseit = tk.Button(self.master, text='Choose it', width=20,
                            command=self.push_chooseit, state = tk.DISABLED)
        self.btnext_task = tk.Button(self.master, text='Next', width=20,
                            command=self.push_next, state = tk.DISABLED)
        self.labchoose.grid(columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        self.btchooseit.grid(row=1, column=0, sticky=tk.W+tk.E, padx=5, pady=2)
        self.btnext_task.grid(row=1, column=1, sticky=tk.W+tk.E,
                              padx=5, pady=2)
        self.master.resizable(width=tk.FALSE, height=tk.FALSE)
        self.show_tasks()


    def show_tasks(self):
        if self.act_ts:
            msg = self.act_ts.pop(0)[1]
            self.labchoose.config(text=msg)
            self.master.after(1000, self.show_tasks)
        else:
            self.act_ts = self.db.get_act_ts()
            msg = self.act_ts[0][1]
            self.labchoose.config(text=msg)
            self.choose_task()

    def choose_task(self):
        self.btchooseit.config(state = tk.NORMAL)
        self.btnext_task.config(state = tk.NORMAL)

    def push_next(self):
        self.i = (self.i + 1) % len(self.act_ts)
        msg = self.act_ts[self.i][1]
        self.labchoose.config(text=msg)

    def push_chooseit(self):
        self.db.choose(self.act_ts[self.i][0])
        self.parent.main.filllb()
        self.master.destroy()
        

af.checkcreatefile()
root = tk.Tk()
db = af.copydb()
app = Autofocus(db, root)
root.mainloop()
af.backup(db)
