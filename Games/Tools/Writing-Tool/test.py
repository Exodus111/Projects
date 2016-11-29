#!/usr/bin/python3
from tkinter.ttk import Frame
from tkinter import Tk, Listbox

class Dialog(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.list = Listbox(self, selectmode="extended")
        self.list.pack(fill="both", expand=1)
        self.current = None
        self.poll() # start polling the list

    def poll(self):
        now = self.list.curselection()
        if now != self.current:
            self.list_has_changed(now)
            self.current = now
        self.after(250, self.poll)

    def list_has_changed(self, selection):
        print("selection is", selection)

if __name__ == "__main__":   #<---Boilerplate code to run tkinter.
    root = Tk()
    app = Dialog(root)
    root.mainloop()
