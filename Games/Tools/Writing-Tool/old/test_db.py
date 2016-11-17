from db import DataBase

data_dict = {
    "Heidi":[{"node1":{"text":"What the hell?", "tags":["test1", "test2"]}},
            {"node2":{"text":"What in the hell is this?", "tags":["test3", "test4"]}},
            {"node3":{"text":"You cannot be here.", "tags":["test5", "test6"]}}],
    "Donald":[{"node1":{"text":"cuz your dead.", "tags":["test7", "test8"]}},
            {"node2":{"text":"This can't be.", "tags":["test9", "test10"]}},
            {"node3":{"text":"Im dreaming.", "tags":["test11", "test12"]}}]
}

def write_to_db(data, db):
    for name in data.keys():
        db.add_npc(name)
        db.add_nodes(name, data[name])
        for n in data[name]:
            node = [i for i in n.keys()][0]
            db.add_text(name + node, n[node]["text"])

if __name__ == "__main__":
    db = DataBase()

    # Save info to files.
    write_to_db(data_dict, db)
    db.save()

    # Load info from files.
    #db.load()
    #print(db.text.values())
