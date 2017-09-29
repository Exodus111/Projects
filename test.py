secret = ['ers', 'rap', 'amet']
bartender = {"request":{"your drink":print("{}{}{}".format(secret[1][::-1], secret[2], secret[0]))}}
bartender["request"]["your drink"]
