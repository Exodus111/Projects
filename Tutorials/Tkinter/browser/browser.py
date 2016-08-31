from tkinter import Tk, Text
from tkinter.ttk import Frame, Label, Entry, Button
from bs4 import BeautifulSoup as bs
import requests
import re

class Main(Frame):
    """Main class for our browser.
        Note that we inherit from Frame, making this a Frame object.
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Browser")
        self.header = {"User-Agent":"Tkinter Browser 0.1"}

        # Here we make our widgets.
        self.top_frame = Frame(self)
        self.url_frame = Frame(self.top_frame)
        self.url_label = Label(self.url_frame, text="Url: ", anchor="n")
        self.url_entry = Entry(self.url_frame, width=80)
        self.url_button = Button(self.url_frame, text="Go", command=self.go_button)
        self.bottom_frame = Frame(self)
        self.text_field = Text(self.bottom_frame)

        #Here we pack our widgets.
        self.top_frame.pack(side="top", padx=15, pady=15)
        self.url_frame.pack(anchor="center")
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)
        self.text_field.pack(side="bottom", fill="both", expand=True)
        self.url_label.pack(side="left")
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_button.pack(side="left", padx=5)
        self.text_field.config(state="disabled", padx=5, pady=5)

    def go_button(self):
        url = self.url_entry.get()
        if url:
            if "http://" not in url:
                url = "http://"+url
            page_text = self.get_page(url)
            self.text_field.config(state="normal")
            self.text_field.delete(1.0, "end")
            self.text_field.insert("end", page_text)
            self.text_field.config(state="disable")

    def get_page(self, url):
        s = requests.Session()
        resp = s.get(url, headers=self.header)
        data = resp.text
        soup = bs(data, "html.parser")
        page_text = soup.find_all(text=True)
        page_text = filter(self.visible, page_text)
        return "".join([str(i)+'\n' for i in page_text])


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
