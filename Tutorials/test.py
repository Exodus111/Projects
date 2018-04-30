mydict = {"test1":"Hey", "Test2":"Wassuuuuuuuup!"}
message = "Nothing"*("test0" not in mydict.keys()) or mydict["test1"]
print(message)