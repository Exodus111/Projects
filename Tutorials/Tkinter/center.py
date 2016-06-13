
from Tkinter import Tk, Frame, BOTH

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.parent.title("Centered Window")
        self.pack(fill=BOTH, expand=1)
        self.center_window()


    def center_window(self):

        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry("{}x{}+{}+{}".format(w, h, x, y))

def main():

    root = Tk()
    ex = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()
