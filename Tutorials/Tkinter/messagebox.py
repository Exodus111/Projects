from ttk import Frame, Button
from Tkinter import Tk, BOTH
import tkMessageBox as mbox

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Message Boxes")
        self.pack()

        error = Button(self, text="Error", command=self.onError)
        error.grid(padx=5, pady=5)

        warning = Button(self, text="Warning", command=self.onWarn)
        warning.grid(row=1, column=0)

        question = Button(self, text="Question", command=self.onQuest)
        question.grid(row=0, column=1)

        inform = Button(self, text="Information", command=self.onInfo)
        inform.grid(row=1, column=1)

    def onError(self):
        mbox.showerror("Error!", "Could NOT open File!")

    def onWarn(self):
        mbox.showwarning("Warning!", "Deprecated function call!!")

    def onQuest(self):
        mbox.askquestion("Question", "Are you sure you want to quit?")

    def onInfo(self):
        mbox.showinfo("Information", "Download Complete.")

def main():
    root = Tk()
    ex = Example(root)
    root.geometry("300x150+300+300")
    root.mainloop()

main()
