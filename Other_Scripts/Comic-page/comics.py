from collections import OrderedDict, defaultdict
from rarfile import RarFile as rf
from PIL import Image
from path import Path

class Series():
    def __init__(self, folder):
        self.num = defaultdict(int)
        self.comics = defaultdict(list)
        self.subfolder = defaultdict(dict)
        self.toplayer_thumbs = OrderedDict()
        self.subfolder = False
        self.subfolder_thumbs = []
        self.folder = Path(folder)
        self.active_comic = None
        self.act_fold_id = 0
        self.check_folders()

    def numerate(self, typ):
        self.num[typ] += 1
        return self.num[typ]

    def check_folders(self):
        folder_id = self.numerate("folder")
        for fil in self.folder.files('*.cbr'):
            comic = Comic(fil)
            comic.id = self.numerate("issue")
            comic.folder_id = folder_id
            self.comics[0].append(comic)
            self.toplayer_thumbs[comic.id] = comic.get_image(0)
        for sub in self.folder.dirs():
            if ".cbr" in sub.files():
                f_id = self.numerate("folder")
                for f in sub.files("*.cbr"):
                    c = Comic(f)
                    c.id = self.numerate("issue")
                    c.folder_id = f_id
                    self.comics[c.folder_id].append(c)
                    self.subfolder[f_id][c.id] = c.get_image(0)
                    if f_id not in self.subfolder:
                        self.toplayer_thumbs[c.id] = c.get_image(0)


    def set_thumbs(self, fold):
        mydict = OrderedDict()
        for com in self.comics[fold]:
            mydict[com.id] = com.get_image(0)
        if fold == 0:
            mydict[self.comics[fold][0].folder_id] = self.comics[fold][0].get_image(0)
        self.layer = fold
        self.thumbs = mydict

    def set_active(self, cid):
        for folder_id in self.comics:
            for c in self.comics[folder_id]:
                if cid == c.id:
                    self.active_comic = c
                    if folder_id != 0:
                        self.act_fold_id = folder_id
                        self.subfolder = True
                    else:
                        self.subfolders = False
                    break

class Comic():
    def __init__(self, comic):
        self.comic = comic
        self.comic_dict = {}
        self.rarfile = rf(self.comic, "r")
        name = self.rarfile.rarfile.replace(".cbr", "")
        img_list = sorted(self.rarfile.namelist())
        self.img_list = [im for im in img_list if ".jpg" in im]
        self.comic_dict["lastpage"] = len(self.img_list)
        self.folder = Path("./{}".format(name))
        if not self.folder.exists(): self.folder.mkdir()
        self.name = self._check_name(name)

    def _check_name(self, name):
        found = []
        name = name.replace("./static/comics", "")
        name = name.strip("\\")
        for num, letter in enumerate(name):
            if letter == "\\":
                found.append(num)
        if found != []:
            name = name[found[-1]+1:]
        return name

    def _rem_folder(self, fn):
        for n, f in enumerate(fn):
            if f == "\\":
                return Path(fn[n+2:])
        return Path(fn)

    def extract_image(self, index):
        name = self.img_list[index]
        img_file = self.rarfile.open(name)
        fname = Path("{}{}{}".format(self.folder, "/", self._rem_folder(name)))
        if not fname.exists():
            Image.open(img_file).save(fname)
        self.comic_dict["page " + str(index)] = fname

    def extract_images(self):
        for num, _ in enumerate(self.img_list):
            self.extract_image(num)

    def get_image(self, page=0):
        strpage = "page {}".format(page)
        lastpage = self.comic_dict["lastpage"]
        if page <= lastpage:
            if strpage not in self.comic_dict:
                self.extract_image(page)
            image = self.comic_dict[strpage]
            return image.replace("./static/comics/", "")
        else:
            if strpage not in self.comic_dict:
                self.extract_image(page)
            image = self.comic_dict["page {}".format(lastpage)]
            return image.replace("./static/comics/", "")
