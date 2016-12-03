# WebComic App by Exodus111
# www.github.com/exodus111
# Use freely, but credit me.

from collections import OrderedDict, defaultdict
from rarfile import RarFile as rf
from PIL import Image
from path import Path

class Series():
    """
    This class makes our Object controller.
    It manages all the Comic Objects, and the communication with Flask.
    """
    def __init__(self, folder):
        """
        Our Initializer.
        `folder` : (string) The folder where our comic files are stored.
        """
        self.num = defaultdict(int)
        self.comics = defaultdict(list)
        self.subfolder_thumbs = defaultdict(OrderedDict)
        self.toplayer_thumbs = OrderedDict()
        self.first = False
        self.folder = Path(folder)
        self.active_comic = None
        self.act_fold_id = 0
        self.check_folders()

    def numerate(self, typ):
        """
        We use this function to create unique IDs for our Comics.
        typ : (string) The name of the ID, gets placed with a / before the number.
        We use two types, `issue` and `folder`, the result being `/issue1` or `/folder1` which is our ID.
        """
        self.num[typ] += 1
        return "/{}{}".format(typ, self.num[typ])

    def check_folders(self):
        """
        We walk through our Folders looking for comics and subfolders with comics.
        Here we instantiate all our comic objects, and giving them their ids.
        They are then saved in the `self.comics` defaultdict under their respective folders.
        The `/folder0` id is made manually, and represents our top folder where the TPBs go.
        This method is run by the __init__ method.
        """
        folder_id = self.numerate("folder")
        for fil in self.folder.files('*.cbr'):
            comic = Comic(fil)
            comic.id = self.numerate("issue")
            comic.folder_id = folder_id
            self.comics["/folder0"].append(comic)
            self.toplayer_thumbs[comic.id] = comic.get_image(0)
        for sub in self.folder.dirs():
            f_id = self.numerate("folder")
            self._find_files(sub, f_id)

    def _find_files(self, fold, f_id):
        """
        A recursive method to find .cbr files in any and all subfolders.
         'fold' : (Path object) The path.py object of the folder.
        """
        for f in fold.files("*.cbr"):
            c = Comic(f)
            c.id = self.numerate("issue")
            c.folder_id = f_id
            self.comics[c.folder_id].append(c)
            if f_id not in self.subfolder_thumbs.keys():
                self.toplayer_thumbs[f_id] = c.get_image(0)
            self.subfolder_thumbs[f_id][c.id] = c.get_image(0)
        if fold.dirs() != []:
            for sub in fold.dirs():
                fid = self.numerate("folder")
                self._find_files(sub, fid)

    def set_active_issue(self, c_id):
        """
        Here we move the viewers selection into the self.active_comic holder.
        `c_id` : (int) the id number of the selected comic.
        This method is activated from a Flask function.
        """
        cid = "/issue"+str(c_id)                #<---Recreating the actual ID.
        for folder_id in self.comics:
            for c in self.comics[folder_id]:
                if cid == c.id:
                    self.active_comic = c
                    break

    def set_active_folder(self, f_id):
        """
        This method is run when the viewer selects one of the subfolders.
        `f_id` : (int) The ID number of the selected folder.
        """
        folder_id = "/folder"+str(f_id)          #<---Recreating the actual ID.
        return self.subfolder_thumbs[folder_id]

class Comic():
    """
    Our Comic class.
    Every file gets to be one object.
    """
    def __init__(self, comic):
        """
        Our initalizer.
        `comic` : (Path Obj) The filepath and filename of the comic file, wrappend in a Path object.
        We start with the path to our file, and open it with Rarfile.
        We then extract the image names, and sort them alphabetically.
        We also set a value for the last page to avoid out of range errors.
        We then create a folder for the file for extracting the images, if such a folder does not already exist.
        """
        self.comic = comic
        self.comic_dict = {}
        self.rarfile = rf(self.comic, "r")
        name = self.rarfile.rarfile.replace(".cbr", "")
        img_list = sorted(self.rarfile.namelist())
        self.img_list = [im for im in img_list if ".jpg" in im]
        self.comic_dict["lastpage"] = len(self.img_list)
        self.folder = Path("./{}".format(name))
        if not self.folder.exists(): self.folder.mkdir()

    def _rem_folder(self, fn):
        """
        This cleans the subfolder name out of a file name.
        `fn` : (string) The name of the file.
        This private method is run from the `extract_image` method.
        """
        for n, f in enumerate(fn):
            if f == "\\":
                return Path(fn[n+2:])
        return Path(fn)

    def extract_image(self, index):
        """
        To read an image it has to be extracted to Disk first.
        This method does that, after checking if the file already exists.
        `index` : (int) The page number to be extracted.
        This method is run from the `get_image` method.
        """
        name = self.img_list[index]
        img_file = self.rarfile.open(name)
        fname = Path("{}{}{}".format(self.folder, "/", self._rem_folder(name)))
        if not fname.exists():
            Image.open(img_file).save(fname)
        self.comic_dict["page " + str(index)] = fname

    def extract_images(self):
        """
        This method will extract all the images in a comic at once.
        """
        for num, _ in enumerate(self.img_list):
            self.extract_image(num)

    def get_image(self, page=0):
        """
        Gets the page the viewer requested.
        `page` : (int) The page number requested.
        Here the user has requested a page. If that page is out of range, we simply return the last page of the comic.
        We return the image path, removing the folders that Flask will add automatically.
        """
        strpage = "page {}".format(page)
        lastpage = self.comic_dict["lastpage"]-1
        l_strpage = "page {}".format(lastpage)
        if page < lastpage:
            if strpage not in self.comic_dict:
                self.extract_image(page)
            image = self.comic_dict[strpage]
            return image.replace("./static/comics/", "")
        else:
            print("Page: {}\n LastPage: {}".format(page, lastpage))
            if l_strpage not in self.comic_dict:
                self.extract_image(lastpage)
            image = self.comic_dict[l_strpage]
            return image.replace("./static/comics/", "")
