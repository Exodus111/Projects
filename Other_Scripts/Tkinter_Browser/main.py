from tkinter import Tk, Frame, Label, Entry, Text, Button
from bs4 import BeautifulSoup as bs4
import requests
import re

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.top_frame = Frame(self)
        self.url_frame = Frame(self.top_frame)
        self.url_label = Label(self.url_frame, text="Url: ", anchor="n")
        self.url_entry = Entry(self.url_frame, width=80)
        self.url_button = Button(self.url_frame, text="Go", command=self.go_button)

        self.bottom_frame = Frame(self)
        self.textfield = Text(self.bottom_frame)

        self.top_frame.pack(side="top", padx=15, pady=30)
        self.url_frame.pack(anchor="center")
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)
        self.textfield.pack(side="bottom", fill="both", expand=True)
        self.url_label.pack(side="left")
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_button.pack(side="left")
        self.textfield.config(state="disabled", padx=5, pady=5)

    def go_button(self):
        url = self.url_entry.get()
        if url:
            if "http://" not in url:
                url = "http://"+url
            resp = requests.get(url)
            data = resp.text
            soup = bs4(data, "html.parser")
            page_text = soup.find_all(text=True)
            page_text = filter(self.visible, page_text)
            page_text = "".join([i for i in page_text])
            self.textfield.config(state="normal")
            self.textfield.delete(1.0, "end")
            self.textfield.insert("end", page_text)
            self.textfield.config(state="disabled")

    def visible(self, e):
        if e.parent.name in ('style', 'script', '[document]', 'head', 'title'):
            return False
        elif re.match('<!--.*-->', str(e.encode('utf-8'))):
            return False
        return True

if __name__ == "__main__":
    root = Tk()
    app = Main(root).pack(fill="both", expand=True)
    root.mainloop()
