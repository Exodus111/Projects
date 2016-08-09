from collections import defaultdict
from functools import partial
from tkinter import Tk, Toplevel, Text, Message, Canvas, Menu
from tkinter.ttk import Frame, Label, Entry, Button

def numerate(num, pre):
    """ A function for making unique IDs
        `num` : defaultdict(int)
        'pre' : string
        Returns a string combining the prefix
            with a unique number.
    """
    num[pre] += 1
    return "{}{}".format(pre, num[pre])


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
            entry = self.entries["Entry"][i].get()
            entr_list = entry.split(",")
            self.entries["Entry"][i] = entr_list
        for i in self.entries["Text"]:
            self.entries["Text"][i] = self.entries["Text"][i].get("1.0", "end-1c")
        self.destroy()
        self.parent.save_info(self.name, self.entries, self.pos)

    def update_box(self):
        if "Header" in self.entries["Entry"]:
            txt = self.entries["Entry"]["Header"].get()
            txt = txt.split(",")
            sticky = [i for i in self.parent.stickies if i.name == self.origin]
            box = [b for b in sticky[0].boxes.values() if b.sid == "head"]
            box[0].config(state="normal")
            box[0].insert("end", txt)
            self.parent.info[self.origin]["Entry"]["Header"] = txt
        elif "Footer" in self.entries["Entry"]:
            txt = self.entries["Entry"]["Footer"].get()
            txt = txt.split(",")
            self.parent.info[self.origin]["Entry"]["Footer"] = txt
        else:
            txt = self.entries["Text"]["Body"].get("1.0", "end-1c")
            self.parent.info[self.origin]["Text"]["Body"] = txt
            self.destroy()
            return
        self.destroy()
        self.parent.check_relation_single(self.origin)

    def ok_cancel_buttons(self, call=None):
        if not call:
            call = self.save
        button_frame = Frame(self.frame)
        ok_button = Button(button_frame, text="Ok", command=call)
        cancel_button = Button(button_frame, text="Cancel", command=self.destroy)
        button_frame.pack(fill="x")
        cancel_button.pack(side="right", padx=5, pady=5)
        ok_button.pack(side="right")

    def insert_entry_field(self, txt, default=None):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Entry(frame)
        entry.pack(fill="x", padx=5, pady=5, expand=True)
        if default:
            entry.insert("end", default)
        self.entries["Entry"][txt] = entry

    def insert_text_field(self, txt, default=None):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Text(frame)
        entry.pack(fill="both", pady=5, padx=5, expand=True)
        if default:
            entry.insert("end", default)
        self.entries["Text"][txt] = entry

class Text2(Frame):
    def __init__(self, master, width=0, height=0, sid=None, **kwargs):
        Frame.__init__(self, master, width=width, height=height)
        self.master = master
        self.width = width
        self.height = height
        self.sid = sid
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
    def __init__(self, parent, name,  pos, size, textdict):
        Frame.__init__(self, parent)
        self.parent = parent
        self.text = textdict
        self.name = name
        self.pos = pos
        self.line_en_ids = []
        self.line_ex_ids = []
        self.pack(expand=True)
        self.parent.title = "test"
        self.size = size
        self.dragging = False
        self.num = defaultdict(int)
        self.b_edit = defaultdict(bool)
        self.boxes = {}
        self.init_ui()

    def init_ui(self):
        all_l = self.size[0] - 52
        xblock = self.size[0]/6
        yblock = self.size[1]/6
        body_h = yblock * 4
        self.make_message_box(all_l, yblock, self.text["header"], "head")
        self.make_message_box(all_l, body_h, self.text["body"], "body")
        self.make_message_box(all_l, yblock, self.text["footer"], "foot")
        self.entr_dot = (self.pos[0] - ((xblock*3)-15), self.pos[1] - (yblock*2))
        self.exit_dot = (self.pos[0] + ((xblock*3)-15), self.pos[1] + (yblock*2))

    def make_message_box(self, w, h, txt, sid):
        box = Text2(self, width=w, height=h, sid=sid)
        box.insert("1.0", txt)
        box.config(state="disabled")
        box.pack(expand=True)
        box.bind("<ButtonPress-1>", self.drag_start_stop)
        box.bind("<B1-Motion>", self.drag)
        box.bind("<ButtonRelease-1>", self.drag_start_stop)
        b_id = numerate(self.num, "box")
        box.bind("<Button-3>", lambda x: self.edit_box(b_id, x))
        self.boxes[b_id] = box


    def edit_box(self, boxid, _):
        box = self.boxes[boxid]
        pop = Node(self.parent, numerate(self.num, "edit"))
        pop.origin = self.name
        if box.sid == "head":
            txt = box.get("1.0", "end-1c")
            pop.insert_entry_field("Header", txt)
        elif box.sid == "foot":
            txt = box.get("1.0", "end-1c")
            pop.insert_entry_field("Footer", txt)
        else:
            txt = box.get("1.0", "end-1c")
            pop.insert_text_field("Body", txt)
        pop.ok_cancel_buttons(pop.update_box)
        """
        if not self.b_edit[boxid]:
            box.config(state="normal")
            self.b_edit[boxid] = True
        else:
            box.config(state="disabled")
            self.b_edit[boxid] = False
            txt = box.get("1.0", "end-1c")
            if box.sid == "head":
                txt = txt.split(",")
                self.parent.info[self.name]["Entry"]["Header"] = txt
            elif box.sid == "foot":
                txt = txt.split(",")
                self.parent.info[self.name]["Entry"]["Footer"] = txt
            elif box.sid == "body":
                self.parent.info[self.name]["Entry"]["Body"] = txt
                return
            self.parent.check_relation_single(self.name)
            """

    def drag_start_stop(self, _event):
        self.dragging = not self.dragging

    def extrapolate_rect(self):
        w = self.size[0]-45
        h = self.size[1]+10
        tl = self.pos[0] - (w/2), self.pos[1] - (h/2)
        br = self.pos[0] + (w/2), self.pos[1] + (h/2)
        return tl, br

    def drag(self, pos):
        if self.dragging:
            self.pos = (pos.x, pos.y)
            self.parent.move(self.name, self.pos[0], self.pos[1])
            self.update_dots()
            for l_id in self.line_en_ids:
                lx1, ly1, lx2, ly2 = self.parent.coords(l_id)
                lx2, ly2 = self.entr_dot
                self.parent.coords(l_id, lx1, ly1, lx2, ly2)
            for l_id in self.line_ex_ids:
                lx1, ly1, lx2, ly2 = self.parent.coords(l_id)
                lx1, ly1 = self.exit_dot
                self.parent.coords(l_id, lx1, ly1, lx2, ly2)

    def update_dots(self):
        self.entr_dot = self._get_center(self.en_id)
        self.exit_dot = self._get_center(self.ex_id)

    def _get_center(self, l_id):
        x1, y1, x2, y2 = self.parent.coords(l_id)
        rx = int((x1-x2)/2)
        ry = int((y1-y2)/2)
        return (x1-rx, y2+ry)


class Canv(Canvas):
    def __init__(self, parent, name, size):
        Canvas.__init__(self, parent)
        self.parent = parent
        self.name = name
        self.background = "white"
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.info = defaultdict(dict)
        self.num = defaultdict(int)
        self.sticky_size = (250, 220)
        self.stickies = []
        self.lines = {}
        self.bind("<ButtonPress-1>", self.smark)
        self.bind("<B1-Motion>", self.sdrag)
        self.bind("<Button-3>", self.insert_node)

    def smark(self, pos):
        self.scan_mark(pos.x, pos.y)

    def sdrag(self, pos):
        self.scan_dragto(pos.x, pos.y, 5)

    def insert_node(self, pos):
        node = Node(self, numerate(self.num, "Node"), pos)
        node.insert_entry_field("Header")
        node.insert_text_field("Body")
        node.insert_entry_field("Footer")
        node.ok_cancel_buttons()

    def save_info(self, name, entries, pos):
        if "Node" in name:
            txtdict = {
            "header":self.csv(entries["Entry"]["Header"]),
            "body":entries["Text"]["Body"],
            "footer":self.csv(entries["Entry"]["Footer"])
            }
            self.make_sticky(name, txtdict, pos)
        self.info[name] = entries
        self.check_relation_single(name)

    def check_relation_single(self, name):
        l1 = self.info[name]["Entry"]["Header"]
        l2 = self.info[name]["Entry"]["Footer"]
        for i in self.info:
            if i != name:
                lx1 = self.info[i]["Entry"]["Header"]
                lx2 = self.info[i]["Entry"]["Footer"]
                if lx2 != ['']:
                    for j in l1:
                        if j in lx2:
                             self.draw_line(i, name)
                        else:
                            self.remove_if_needed(i, name)
                if lx1 != ['']:
                    for k in l2:
                        if k in lx1:
                            self.draw_line(name, i)
                        else:
                            self.remove_if_needed(name, i)

    def csv(self, list1):
        return "".join(i+", " for i in list1).strip(", ")

    def check_relation_all(self):
        """ This checks ALL the stickies and adds ALL the lines."""
        for i in self.info:
            for j in self.info:
                l1 = self.info[j]["Entry"]["Header"]
                l2 = self.info[i]["Entry"]["Footer"]
                if l1 != [''] and l2 != ['']:
                    for l in l1:
                        if l in l2:
                            self.draw_line(i, j)
                        else:
                            self.remove_if_needed(i, j)

    def remove_if_needed(self, name1, name2):
        stick1 = stick2 = None
        for i in self.stickies:
            if i.name == name1:
                stick1 = i
            elif i.name == name2:
                stick2 = i
        if stick1 and stick2:
            coname = "{}{}".format(stick1.name, stick2.name)
            if coname in self.lines.keys():
                l_id = self.lines[coname]
                self.delete(l_id)
                stick1.line_ex_ids = [i for i in stick1.line_ex_ids if i != l_id]
                stick2.line_en_ids = [i for i in stick1.line_en_ids if i != l_id]
                del(self.lines[coname])

    def draw_line(self, name1, name2):
        stick1 = stick2 = None
        for i in self.stickies:
            if i.name == name1:
                stick1 = i
            elif i.name == name2:
                stick2 = i
        if stick1 and stick2:
            coname = "{}{}".format(stick1.name, stick2.name)
            if coname not in self.lines.keys():
                x1, y1 = stick1.exit_dot
                x2, y2 = stick2.entr_dot
                l_id = self.create_line(x1, y1, x2, y2, fill="red", width=3)
                stick1.line_ex_ids.append(l_id)
                stick2.line_en_ids.append(l_id)
                self.lines[coname] = l_id

    def make_sticky(self, name, txt, pos):
        sticky = Sticker(self, name, (pos.x, pos.y), self.sticky_size, txt)
        self.create_window(pos.x, pos.y, window=sticky, tags=sticky.name)
        tl, br = sticky.extrapolate_rect()
        self.create_rectangle(tl, br, fill="black", tags=sticky.name)
        r = 5
        et_x, et_y = sticky.entr_dot
        ex_x, ex_y = sticky.exit_dot
        sticky.en_id = self.create_oval(et_x-r, et_y-r, et_x+r, et_y+r, fill="red", tags=sticky.name)
        sticky.ex_id = self.create_oval(ex_x-r, ex_y-r, ex_x+r, ex_y+r, fill="red", tags=sticky.name)
        self.stickies.append(sticky)

class TopMenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent
        self.newmenu = Menu(self)
        self.showmenu = Menu(self)
        self.newmenu.add_command(label="NPC", command=self.parent.onNew)
        self.newmenu.add_separator()
        self.newmenu.add_command(label="Save", command=self.parent.save)
        self.newmenu.add_command(label="Load", command=self.parent.load)
        self.showmenu.add_command(label="Info", command=self.parent.get_info)
        self.newmenu.add_separator()
        self.showmenu.add_separator()
        self.add_cascade(label="New", menu=self.newmenu)
        self.add_cascade(label="Show", menu=self.showmenu)
        self.add_command(label="Exit", command=self.parent.quit)

    def add_button(self, menu, name, call):
        func = partial(call, name)
        if menu == "new":
            self.newmenu.add_command(label=name, command=func)
        elif menu == "show":
            self.showmenu.add_command(label=name, command=func)


if __name__ == "__main__":
    pass    #<--- For testing.
