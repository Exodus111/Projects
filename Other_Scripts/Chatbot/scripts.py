
def read(rs):
    import codecs, json, os
    if os.path.exists("../vars.json"):
        name = rs.current_user()       
        fh = codecs.open("../vars.json", "r", "utf-8")
        vars = json.loads(fh.read())
        fh.close()
        for key, value in vars.items():
            rs.set_uservars(name, key, value)


def write(rs):
    import codecs, json
    name = rs.current_user()
    vars = rs.get_uservars(name)
    fh = codecs.open("vars.json", "w", "utf-8")
    fh.write(json.dumps(vars))
    fh.close()

def wiki(data, short):
    import wikipedia
    result = wikipedia.summary(data)
    if short:
        index = 0
        for letter in result:
            index += 1
            if letter == ".":
                break
        return result[0:index]
    else:
        return result




