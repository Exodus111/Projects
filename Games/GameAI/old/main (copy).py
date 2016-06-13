import random

class Mob(object):
    def __init__(self, courage_rating):
        self.cr = courage_rating
        self.c_ratings = {
            "Charge":[True, 0],
            "Attack":[True, 0],
            "Defend":[True, 0],
            "Flee":[True, 0]
        }
        self.factors = {
            "hitpoints":100,
            "distance to enemy":100,
            "distance to friend":0,
            "enemy spotted":False
        }
        self.set_ratings()

    def set_ratings(self):
        self.c_ratings["Charge"][1] = self.cr/2                
        self.c_ratings["Attack"][1] = self.cr                     
        self.c_ratings["Defend"][1] = 100                         
        self.c_ratings["Flee"][1] = self.cr + (100 - self.cr)/2   


    def courage_check(self):
        decision = "Don't Know"
        roll = random.randint(0, 100)
        print roll
        if roll <= self.cr:
            decision = "Attack"
            if self.c_ratings["Charge"][0]:
                if roll < self.c_ratings["Charge"][1]:
                    decision = "Charge"
        else:
            decision = "Defend"
            if self.c_ratings["Flee"][0]:
                if roll > self.c_ratings["Flee"][1]:
                    decision = "Flee"
        return decision

class MobGroup(object):
    def __init__(self, amount, courage):
        self.amount = amount
        self.courage = courage
        self.mobs = self.generate_mobs()
        self.group_factors = {
            "in combat":False,
            "everyone alive":True,
            "only two left alive":False,
            "only one left alive":False,
            "enemy hurt":False,
            "enemy critted on":False,
            "enemy running away":False,
            "member hurt":False,
            "member critted on":False,
            "member running away"False
        }

    def generate_mobs(self):
        mobs = []
        for mob in xrange(self.amount):
            mob = Mob(self.courage)
            mobs.append(mob)
        return mobs








