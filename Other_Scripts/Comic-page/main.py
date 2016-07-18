from flask import Flask, render_template
from rarfile import RarFile as rf
from PIL import Image
from path import Path
import os

#This is a hack for Atom, since it doesn't run your file from the files own directory.
here = Path(__file__).abspath().parent
if here != os.getcwd():
    print("Changing dir")
    here.chdir()

class Comics():
    def __init__(self, folder):
        self.folder = folder
        self.comic_dict = {}
        self.create_images()

    def get_image(self, page=0):
        f = self.get_folder()
        last = self.comic_dict[f]["pages"]["lastpage"]
        if int(page) <= last:
            return self.comic_dict[f]["pages"]["pagename {}".format(page)]
        else:
            return self.comic_dict[f]["pages"]["pagename {}".format(last)]


    def get_folder(self):
        for folder in self.comic_dict.keys():
            return folder

    def create_images(self):
        self.comic_list = self.create_comic_list(self.folder)
        for comic in self.comic_list:
            folder_name = comic.rarfile.replace(".cbr", "")
            self.comic_dict[folder_name] = {}
            self.make_img_folder(folder_name, comic)

    def create_comic_list(self, comic_path):
        comics = Path(comic_path)
        mylist = [comic for comic in comics.files()]
        return [rf(i, "r") for i in mylist]

    def make_img_folder(self, folder_name, comic):
        this_folder = Path("./{}".format(folder_name))
        if not this_folder.exists():
            this_folder.mkdir()
            self.extract_pages(folder_name, comic)
        else:
            self.extract_pages(folder_name, comic, new=False)
            print("Folder exists, skipping extraction.")

    def extract_pages(self, folder, rar_file, new=True):
        n_list = sorted(rar_file.namelist())
        self.comic_dict[folder]["pages"] = {}
        for num, name in enumerate(n_list):
            img_file = rar_file.open(name)
            outfile = Path("{}/{}".format(folder, name))
            if new:
                Image.open(img_file).save(outfile)
            self.comic_dict[folder]["pages"]["pagename "+str(num)] = outfile
            print("Handling page {}".format(name))
        self.comic_dict[folder]["pages"]["lastpage"] = num


app = Flask(__name__, static_url_path='/static')

@app.route("/page/<page>")
def page_selector(page):
    global comics
    image = comics.get_image(page)
    return render_template("index.html", image=image, num=int(page))

@app.route("/")
def index():
    global comics
    image = comics.get_image()
    return render_template("index.html", image=image, num=0)

if __name__ == "__main__":
    comics = Comics("./static/comics")
    app.run()
