

def wiki_content(data):
    import wikipedia
    result = wikipedia.summary(data)
    index = 0
    for letter in result:
        index += 1
        if letter == ".":
            break
    print(result[0:index])

    #a = wikipedia.page(data)
    #print(a.content)

def reddit_titles(sub):
    from praw import Reddit
    r = Reddit(user_agent="my_useragent")
    news = r.get_subreddit(sub).get_hot(limit=10)
    news = list(news)
    #num = 3
    for i in news:
        print(i.title)
        #print("{}{}{}{}".format("\033[1;3", num, "m", i.title, "\033[1;m"))
        #num += 1
        #if num > 6:
        #    num = 3
#reddit_titles("worldnews")

for num in range(199):
    print(num)
    print("{}{}{}".format("\033[{}m".format(num),"Testing", "\033[0m"))


