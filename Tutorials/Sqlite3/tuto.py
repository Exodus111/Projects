import sqlite3
from path import Path

def check_for_db(dbfile):
	if Path(dbfile):
		return True
	return False

def gen_db(dbfile,  id_list, name_list):
	print("Generating DB")
	connection = sqlite3.connect(dbfile)
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE names (id INTEGER PRIMARY KEY, name TEXT, sex TEXT, agegroup TEXT)")
	for _id in id_list:
		n = name_list[_id-1]
		if n[-1] == "a" or n[-1] == "y":
			sex = "female"
		else:
			sex = "male"
		if _id <= 3 or (_id >= 7 and _id <= 9):
			agegroup = "Old"
		else:
			agegroup = "Young"  
		cursor.execute("INSERT INTO names VALUES(?, ?, ?, ?)", (_id, n, sex, agegroup))
	connection.commit()
	connection.close()

def fetch_by_id(dbfile, _id):
	print("Fetching by ID")
	connection = sqlite3.connect(dbfile)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM names WHERE id=?", (_id, ))
	return cursor.fetchone()

def fetch_by_key(dbfile, column, key):
	print("Fetching from {} for {}".format(column, key))
	connection = sqlite3.connect(dbfile)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM names WHERE {coi}='{key}'".format(coi=column, key=key))
	return cursor.fetchall()

def fetch_by_two_keys(dbfile, column1, column2, key1, key2):
	print("Fetching from {} and {} for {} and {}".format(column1, column2, key1, key2))
	connection = sqlite3.connect(dbfile)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM names WHERE {coi1}='{key1}' AND {coi2}='{key2}'".format(coi1=column1, coi2=column2, key1=key1, key2=key2))
	return cursor.fetchall()

def main():
	id_list = [i+1 for i in range(10)]
	name_list = ["Djonsiscus", "Jarold", "Tylda", "Riff", "Sheila", "Thack", "Johes", "Duren", "Donald", "Trinity"]

	dbfile = "sqlite3_tutorial.db"
	if not check_for_db(dbfile):
		gen_db(dbfile, id_list, name_list)

	#row = fetch_by_id(dbfile, 4)
	#singledata = fetch_by_key(dbfile, "agegroup", "Young")
	data = fetch_by_two_keys(dbfile, "agegroup", "sex", "Old", "male")
	print(data)

if __name__ == "__main__":
	main()
