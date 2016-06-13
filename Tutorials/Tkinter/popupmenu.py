from Tkinter import Tk, Frame, Menu

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Popup Menu")
        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Beep", command=self.bell())
        self.menu.add_command(label="Exit", command=self.onExit)

        self.parent.bind("<Button-3>", self.showmenu)
        self.pack()

    def showmenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.quit()

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()

if __name__ == "__main__":
    main()
