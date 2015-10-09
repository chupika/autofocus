import autofocus as af
from tkinter import *


widthpixels = 393
heightpixels = 350
af.checkcreatefile()
db = af.copydb()

root = Tk()
root.geometry('{}x{}'.format(widthpixels, heightpixels))

lbox = Listbox(root, height=20, width=50)

def turn_the_page_gui(db):
    if len(db["active"]):
        if db["isdone"]:
            db["isdone"] = False
            db["active"] = db["active"][1:] + [db["active"][0]]
        elif db["pages"][db["active"][0]] is not db["pages"][-1]:
            if messagebox.askyesno(
                "Warning!",
                "If you turn the page, all uncompleted tasks will be demolished.\
                Are you sure you want to turn the page?"):
                for task in db["pages"][db["active"][0]]:
                    task[1] = 1
                del db["active"][0]
        else:
            messagebox.showwarning(
                "Warning!",
                "You cannot turn the last page without completing something!")
        return db           

def filllb():
    lbox.delete(0, END)
    i = 0
    if db["active"]:
        for task in db["pages"][db["active"][0]]:
            lbox.insert(i, task[0])
            if task[1]:
                lbox.itemconfig(i, bg='indigo', fg='white')
            i += 1

def pushadd():
    msg = entry_add.get().strip()
    if msg:
        af.add(msg, db)
        af.savedb(db, "tasks.pkl")
        filllb()
    entry_add.delete(0, END)
    
def pushturn():
    global db
    db = turn_the_page_gui(db)
    af.savedb(db, "tasks.pkl")
    filllb()

def pushdone():
    if lbox.curselection():
        af.complete(lbox.curselection()[0], db)
        af.savedb(db, "tasks.pkl")
        filllb()

def pushcont():
    if lbox.curselection():
        af.continue_later(lbox.curselection()[0], db)
        af.savedb(db, "tasks.pkl")
        filllb()

filllb()

lbox.grid(rowspan=3, sticky=W+E)

entry_add = Entry(root)
entry_add.grid(row=3, column=0, sticky=W+E)
entry_add.bind('<Return>', lambda event: pushadd())

button_add = Button(root, text='Add new task', command=pushadd)
button_add.grid(row=3, column=1, sticky=W+E)

button_done = Button(root, text='Done!\nF2', command=pushdone)
button_done.grid(row=0, column=1, sticky=N+W+E+S)

button_cont = Button(root, text='Continue later\nF3', command=pushcont)
button_cont.grid(row=1, column=1, sticky=N+W+E+S)

button_turn = Button(root, text='Turn the Page!\nF4', command=pushturn)
button_turn.grid(row=2, column=1, sticky=N+W+E+S)

root.resizable(width=FALSE, height=FALSE)
root.bind('<F2>', lambda event: pushdone())
root.bind('<F3>', lambda event: pushcont())
root.bind('<F4>', lambda event: pushturn())
root.mainloop()
af.backup(db)
