#!/usr/bin/python3
from tkinter.ttk import Frame, Label
from tkinter import Tk, BOTH, Listbox, StringVar, END

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Listbox")
        self.pack(fill=BOTH, expand=1)

        acts = ["Scarlett Johansson", "Rachel Weiss", "Natalie Portman", "Jessica Alba", "Angelina jolie", "Emma Stone", "Sandra Bullock", "Julia Roberts",
        "Jennifer Lawrence", "Mila Kunis", "Jennifer Aniston", "Charlize Theron", "Cameron Diaz", "Nicole Kidman", "Meryl Streep", "Reese Witherspoon"]

        lb = Listbox(self, selectmode="multiple")
        for i in acts:
            lb.insert(END, i)

        lb.bind("<<ListboxSelect>>", self.onSelect)

        lb.pack(pady=15)

        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)
        self.label.pack()

    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.var.set(value)

def main():
    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()

main()
