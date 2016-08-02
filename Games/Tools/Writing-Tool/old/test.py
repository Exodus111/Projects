from Tkinter import Tk, Canvas, Menu, Toplevel, Text, Scrollbar, Listbox

class Writer(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self)
        self.parent = parent
        self.row = 0
        self.maxsize(650, 850)
        self.resizable(0,0)
        self.scroll = Scrollbar(self)
        self.scroll.pack(side="right", fill="y", expand=True)
        self.frame = Listbox(self, yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.frame.yview)
        self.frame.pack()

        self.init_ui()


    def init_ui(self):

        name = self.insert_entry_field("Name")
        events = self.insert_entry_field("Events")
        location = self.insert_entry_field("Location")
        statement = self.insert_text_field("Statement")
        reply1 = self.insert_text_field("Reply1")
        reply2 = self.insert_text_field("Reply2")
        reply3 = self.insert_text_field("Reply3")
        reply4 = self.insert_text_field("Reply4")


        buttonframe = Frame(self)
        button1 = Button(buttonframe, text="Ok")
        button2 = Button(buttonframe, text="Cancel")
        button2.pack(side="right", anchor="s", padx=5, pady=5)
        button1.pack(side="right", anchor="s", pady=5)
        buttonframe.pack(side="bottom", anchor="e")

    def insert_entry_field(self, txt):
        frame = Frame(self.frame)
        frame.grid(row=self.row, column=0)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Entry(frame)
        entry.pack(fill="x", padx=5, pady=5, expand=True)
        entryfield = [frame, label, entry]

        return entryfield

    def insert_text_field(self, txt):
        frame = Frame(self.frame)
        frame.grid(row=self.row, column=0)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Text(frame)
        entry.pack(fill="both", pady=5, padx=5, expand=True)
        textfield = [frame, label, entry]
        return textfield
