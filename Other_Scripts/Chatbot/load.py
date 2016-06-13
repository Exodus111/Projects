import codecs
import json

def write(name):
    vars = rs.get_uservars(name)
    fh = codecs.open("vars.json", "w", "utf-8")
    fh.write(json.dumps(vars))
    fh.close()

def read(name):
    fh = codecs.open("vars.json", "r", "utf-8")
    vars = json.loads(fh.read())
    fh.close()
    for key, value in vars.items():
        rs.set_uservars(name, key, value)