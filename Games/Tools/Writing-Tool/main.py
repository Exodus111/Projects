from tkinter import Tk, Canvas, Menu, Toplevel, Text, Scrollbar, Listbox
from tkinter.ttk import Frame, Label, Entry, Button, Style

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry("1400x900+150+150")
        self.init_ui()

    def init_ui(self):
        self.parent.title("Node Writer")
        self.style = Style()
        self.style.theme_use("alt")
        self.pack(fill="both", expand=True)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        menubar.add_command(label="New", command=self.onNew)
        menubar.add_command(label="Load")
        menubar.add_command(label="Exit", command=self.quit)

        canvas = Canvas(self, background="white")
        canvas.pack(fill="both", expand=1)

    def onNew(self):
        new = Node(self)
        labels = new.insert_entry_field("Labels")
        labels2 = new.insert_entry_field("Labels2")
        text = new.insert_text_field("Text")
        new.ok_cancel_buttons()

class Node(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self)
        self.parent = parent
        self.resizable(0,0)
        self.frame = Frame(self)
        self.init_ui()
        self.frame.pack(side="right", fill="y", expand=True)

    def init_ui(self):
        pass

    def ok_cancel_buttons(self):
        button_frame = Frame(self.frame)
        ok_button = Button(button_frame, text="Ok", command=self.save)
        cancel_button = Button(button_frame, text="Cancel", command=self.destroy)
        button_frame.pack(fill="x")
        cancel_button.pack(side="right", padx=5, pady=5)
        ok_button.pack(side="right")


    def save(self):
        pass

    def insert_entry_field(self, txt):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Entry(frame)
        entry.pack(fill="x", padx=5, pady=5, expand=True)
        entryfield = [frame, label, entry]
        return entryfield

    def insert_text_field(self, txt):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Text(frame)
        entry.pack(fill="both", pady=5, padx=5, expand=True)
        textfield = [frame, label, entry]
        return textfield

def main():
    root = Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
