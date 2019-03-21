#!/usr/bin/python3
# This file generates a database of comics from .cbr file.
# The comics all need to be subfolders of a starting folder, or FOLDER.
# The Sqlite Database will be generated with the following columns:
# id, title, episode, year, series, house, filename, covererurl

from urllib.request import urlopen
from google_images_download import google_images_download
import json
import sqlite3
import re
from path import Path

def main():
	folder = "/home/aurelio/Pictures/comics/"
	filenames = find_filenames(folder)
	comic_list = []
	for num, fname in enumerate(filenames):
		if "Druuna" not in fname: 
			parsed = parse_filename(fname)
			if parsed != None:
				title, episode, year, series, house = parsed
				comic_list.append((num, title, episode, year, series, "Marvel", fname))
	gen_database(comic_list)

def find_filenames(folder):
	return _recursive_filesearch(folder, [])

def _recursive_filesearch(folder, file_list):
	file_list.extend([str(comicfile) for comicfile in Path(folder).files("*.cbr")])
	for subdir in Path(folder).dirs():
		file_list = _recursive_filesearch(subdir, file_list)
	return file_list

def parse_filename(filename):
	year_pattern = r"\(\d{4}\b\)"
	title_pattern = r"(?=\)/)(.*)(?<=\(\b(19|20)\d{2}\b\))"
	title = re.findall(title_pattern, filename)
	if title != []:
		year = re.findall(year_pattern, filename)
		year = year[0]
		title = title[0][0]
		title = title.strip(year)
		title = title.strip(")/")
		year = int(year.strip("()"))
		episode = re.findall(r"[0-9]+", title)
		if episode != []:
			episode = episode[0]
			title = title.strip()
			title = title.strip(episode)
			episode = int(episode)	
		else:
			episode = 1
		title = title.strip()
		return (title, episode, year, "", "Marvel")  # So far only works for Marvel titles.
	print(filename)
	return None

def gen_database(list_of_tuples):
	dbfile = "data/comicdb.db"
	db = sqlite3.connect(dbfile)
	cursor = db.cursor()
	cursor.execute("CREATE TABLE comics (id INTEGER PRIMARY KEY, title TEXT, episode INTEGER, year INTEGER, series TEXT, house TEXT, filename TEXT)")
	for comic in list_of_tuples:
		cursor.execute("INSERT INTO comics VALUES(?, ?, ?, ?, ?, ?, ?)", comic) 
	db.commit()
	db.close()

def add_to_database(dbfile, list_of_tuples):
	db = sqlite3.connect(dbfile)
	cursor = db.cursor()
	for comic in list_of_tuples:
		cursor.execute("INSERT INTO comics VALUES(?, ?, ?, ?, ?, ?, ?)", comic) 
	db.commit()
	db.close()

def fetch_database(dbfile):
	db = sqlite3.connect(dbfile)
	cursor = db.cursor()
	cursor.execute("SELECT * FROM comics")
	return cursor.fetchall()

def database_to_dict(dbfile):
	data = fetch_database(dbfile)
	data_dicts = []
	for i in data:
		data_dicts.append({"id":i[0], "title":i[1], "episode":i[2], "year":i[3], "series":i[4], "house":i[5], "filename":i[6]})
	return data_dicts

def database_to_dict_sorted(dbfile, cat):
	data = database_to_dict(dbfile)
	return sorted(data, key=lambda x : sort_by_cat(x, cat))

def sort_by_cat(inp, cat):
	return inp[cat]

def collect_by_cat(db_dicts, cat, key):
	collection = []
	for d in db_dicts:
		if key in d[cat]:
			collection.append(d)
	return collection

def collect_by_title_sorted(dbfile, name):
	data = database_to_dict(dbfile)
	collected = collect_by_cat(data, "title", name)
	return sorted(collected, key=lambda x: sort_by_cat(x, "title"))



def find_coverurl(title, episode, year):
	response = google_images_download.googleimagesdownload()
	arguments = {
		"keywords":"{} {} {} {}".format(title, episode, year, "cover"),
		"limit":1,
		"output_directory":"static/covers/"
	}
	image_path = response.download(arguments)
	cover = list(image_path.values())[0][0]
	cover_name = Path(cover).name
	cover_folder = Path(str(cover).replace(cover_name, ""))
	filetype = cover_name[-3:]
	with cover_folder:
		filepath = Path(cover_name).rename("{} {} {}.{}".format(title, episode, "cover", filetype))
	return str(filepath.realpath())


if __name__ == "__main__":
	#main()
	data = collect_by_title_sorted("data/comicdb.db", "The Punisher")
	print(json.dumps(data, indent=4))
