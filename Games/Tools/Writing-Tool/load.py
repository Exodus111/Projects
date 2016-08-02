from tkinter import Tk, Toplevel, Text, Message
from tkinter.ttk import Frame, Label, Entry, Button


class Node(Toplevel):
    """ This class is a catchall for all popup windows."""
    def __init__(self, parent, name, pos=(0,0)):
        Toplevel.__init__(self)
        self.parent = parent
        self.name = name
        self.pos = pos
        self.entries = {"Entry":{}, "Text":{}}
        self.resizable(0,0)
        self.frame = Frame(self)
        self.frame.pack(side="right", fill="y", expand=True)

    def save(self):
        for i in self.entries["Entry"]:
            self.entries["Entry"][i] = self.entries["Entry"][i].get()
        for i in self.entries["Text"]:
            self.entries["Text"][i] = self.entries["Text"][i].get("1.0", "end-1c")
        self.parent.save_info(self.name, self.entries, self.pos)
        self.destroy()

    def ok_cancel_buttons(self):
        button_frame = Frame(self.frame)
        ok_button = Button(button_frame, text="Ok", command=self.save)
        cancel_button = Button(button_frame, text="Cancel", command=self.destroy)
        button_frame.pack(fill="x")
        cancel_button.pack(side="right", padx=5, pady=5)
        ok_button.pack(side="right")

    def insert_entry_field(self, txt):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Entry(frame)
        entry.pack(fill="x", padx=5, pady=5, expand=True)
        self.entries["Entry"][txt] = entry

    def insert_text_field(self, txt):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Text(frame)
        entry.pack(fill="both", pady=5, padx=5, expand=True)
        self.entries["Text"][txt] = entry

class Text2(Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.height = height
        self.width = width
        self.master = master
        Frame.__init__(self, master, width=self.width, height=self.height)
        self.text_widget = Text(self, **kwargs)
        self.text_widget.pack(expand=True, fill="both")

    def insert(self, *args, **kwargs):
        self.text_widget.insert(*args, **kwargs)

    def config(self, *args, **kwargs):
        self.text_widget.config(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.text_widget.get(*args, **kwargs)

    def bind(self, *args, **kwargs):
        self.text_widget.bind(*args, **kwargs)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)

class Sticker(Frame):
    def __init__(self, parent, size, textdict):
        Frame.__init__(self, parent)
        self.parent = parent
        self.text = textdict
        self.id = None
        self.rect_id = None
        self.pack(expand=True)
        self.parent.title = "test"
        self.size = size
        self.dragging = False
        self.init_ui()

    def init_ui(self):
        xblock = self.size[0] - 52
        yblock = self.size[1]/6
        head_h = foot_h = yblock
        body_h = yblock * 4
        self.make_message_box(xblock, head_h, self.text["header"])
        self.make_message_box(xblock, body_h, self.text["body"])
        self.make_message_box(xblock, foot_h, self.text["footer"])


    def make_message_box(self, w, h, txt):
        box = Text2(self, width=w, height=h)
        box.insert("1.0", txt)
        box.config(state="disabled")
        box.pack(expand=True)
        box.bind("<ButtonPress-1>", self.drag_start_stop)
        box.bind("<B1-Motion>", self.drag)
        box.bind("<ButtonRelease-1>", self.drag_start_stop)

    def drag_start_stop(self, _event):
        self.dragging = not self.dragging

    def drag(self, pos):
        if self.dragging:
            x, y = (pos.x, pos.y)
            self.parent.canvas.move(self.id, x, y)
            self.parent.canvas.move(self.rect_id, x, y)


if __name__ == "__main__":
    txtdict = {"header":"Test1","body":"Test2","footer":"Test3"}
    root = Tk()
    sticky = Sticker(root, (200, 200), txtdict)
    root.mainloop()
