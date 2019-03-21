#!/usr/bin/python3
from contextlib import contextmanager
import sys, os, time
from rarfile import RarFile
from path import Path
import patoolib

class FolderManager:
	def __init__(self, folder, target):
		self.folder = folder
		self.target = target
		self.series = None
		self.folderdict = self.gen_folders()

	def gen_folders(self):
		folderdict = {}
		for i, f in enumerate(Path(self.folder).dirs()):
			if len(f.files("*.cbr")) > 0:
				folderdict["folder"+str(i)] = str(f)
		return folderdict


	def pick_folder(self, fid):
		folder = self.folderdict["folder"+str(fid)]
		self.series = ComicFiles(folder, self.target) 

class ComicFiles:
	def __init__(self, folder, target):
		self.folder = folder
		self.target = target
		self.cover_folder = "./static/covers/"
		self.current_comic = None
		self.comicdict = {}
		self.ids = {}
		self.walk_dirs(Path(self.folder))
		self.coverdict = self.get_covers()

	def get_covers(self):
		Path(self.cover_folder).mkdir_p()
		coverdict = {}
		for folder in self.comicdict.keys():
			print("Opening Folder: " + folder)
			for comic in self.comicdict[folder]:
				print("Opening Comic: " + comic)
				self.extract(comic)
				cover = sorted([f for f in Path(self.target).files("*.jpg")])[0]
				cover.move(self.cover_folder + cover.basename())
				coverdict[self.find_id(comic)] = self.cover_folder + cover.name
		self.empty_folder(self.target)
		return coverdict

	def walk_dirs(self, folder):
		print("Walking through: " + folder)
		comics = self.find_comics_in_folder(folder)
		self.walk_comics(comics)
		self.comicdict[self.gen_id(folder, "folder")] = comics
		for subdir in folder.dirs():
			self.walk_dirs(subdir)

	def find_id(self, issue):
		for _id in self.ids.keys():
			if issue == self.ids[_id]:
				return _id
		raise Exception("Comic ID not found. This should not have happened.")

	def gen_id(self, name, t):
		num = len(self.ids) + 1
		comic_id = t+str(num)
		self.ids[comic_id] = name
		return comic_id

	def walk_comics(self, comics):
		for comic in comics:
			self.gen_id(comic, "issue")

	def find_comics_in_folder(self, folder):
		return sorted([f for f in Path(folder).files("*.cbr")])

	def set_active_folder(self, fid):
		self.extract(self.comicdict[fid])
		page = sorted([f for f in Path(self.target).files("*.jpg")])[0]

	def set_current(self, num):
		comic = self.ids[num]
		self.extract(comic)

	def get_image(self, num):
		images = sorted([f for f in Path(self.target).files("*.jpg")])
		if num+1 > len(images):
			num = 0
		return images[num]

	def empty_folder(self, target):
		if Path(target).isdir():
			if len(Path(target).files()) != 0:
				for f in Path(target).walk():
					if not f.isdir():
						f.remove_p()

	def flatten_target(self, target):
		for folder in Path(target).dirs():
			for f in folder.files():
				f.move(target)
			folder.rmdir_p()

	def extract(self, filename):
		self.empty_folder(self.target)
		self._patoolib_extraction(filename, self.target)
		self.flatten_target(self.target)

	def _patoolib_extraction(self, filename, target):
		Path(target).makedirs_p(mode=511)
		patoolib.extract_archive(filename, verbosity=-1, outdir=target)

def display_comics(comics):
	num = 0
	for key in comics.comicdict.keys():
		for comic in comics.comicdict[key]:
			num += 1
			print(num, ":  ", str(Path(comic).basename()).strip(".cbr"))

def extract_comic(comics, num):
	count = 0
	for key in comics.comicdict.keys():
		for comic in comics.comicdict[key]:
			count += 1
			if count == num:
				return comic

def inting(text):
	try:
		return int(text)
	except:
		return False

@contextmanager
def supress_stdout():
	with open(os.devnull, "w") as devnull:
		old_stdout = sys.stdout
		sys.stdout = devnull
		try:
			yield
		finally:
			sys.stdout = old_stdout

if __name__ == "__main__":
	pass

