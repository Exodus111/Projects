import random
import time

class Mob(object):
    def __init__(self, mobtype, name, courage, hp, group):
        self.type = mobtype
        self.name = name
        self.hp = hp
        self.group = group
        self.courage = courage

    def courage_check(self):
        charge = self.courage /2
        attack = self.courage
        defense = 100 - self.courage
        danger = random.randint(0, 100)
        if danger < charge:
            return "charge"
        elif danger < attack:
            return "attack"
        elif danger < defense:
            return "defend"
        else:
            return "flee"

    def damaged(self, amount, target):
        self.group.broadcast("{} takes {} amount of damage.".format(self.name, amount))
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.group.broadcast("{} is dead.".format(self.name))
        else:
            check = self.courage_check()
            if check == "flee":
                self.flee(target)



    def circle_dist_check(self, target):
        chance = random.randint(0, 100)
        if chance <= 30:
            self.group.broadcast("{} is within range of {}".format(self.name, target))
        else:
            self.group.broadcast("{} is not within range of {}".format(self.name, target))            


    def raycast_col_check(self, target):
        chance = random.randint(0, 100)
        if chance <= 50:
            self.group.broadcast("{} has view of {}".format(self.name, target))        
        else:
            self.group.broadcast("{} cannot see {}".format(self.name, target))        

    def move_to_point(self, point):
        self.group.broadcast("{} moves to {}".format(self.name, point))    

    def follow(self, target):
        self.group.broadcast("{} is following {}".format(self.name, target.name))        

    def check_for_enemy(self):
        chance = random.randint(0, 100)
        if chance <= 30:
            self.group.broadcast("{} sees an enemy".format(self.name))
            self.group.group_events["Enemy_spotted"][0] = True
            self.group.group_events["Enemy_spotted"][2] = [self, self]
        else:        
            self.group.broadcast("{} sees nothing".format(self.name))

    def patrol_area(self):
        self.group.broadcast("{} starts to patrol the area")

    def flee(self, target):
        self.group.broadcast("{} runs away from {}".format(self.name, target.name))


    def stand_ground(self):
        self.group.broadcast("{} stands his ground".format(self.name))


    def attack_melee(self, target):
        self.group.broadcast("{} attacks {} up close.".format(self.name, target.name))


    def attack_range(self, target):
        self.group.broadcast("{} attacks {} from range.".format(self.name, target.name))

    def surround(self, target, num):
        self.group.broadcast("{} surrounds {}".format(self.name, target.name))


    def shout(self, message):
        self.group.broadcast("{} says: {}".format(self.name, message))

class Log(object):
    def __init__(self):
        self.token = 0
        self.log = {}
        self.empty = True

    def record(self, message):
        if self.empty: self.empty = False
        self.token += 1
        thetime = time.strftime("%R:%S")
        self.log[self.token] = {"time":thetime, "msg":message }

    def output(self):
        for l in self.log:
            print self.log[l]["time"], self.log[l]["msg"]

class Strategies(object):
    def __init__(self, mobs):
        self.mobs = mobs

    def enemy_spotted(self, args):
        leader = args[0]
        target = args[1]
        leader.shout("{}!! There, there is {}!!".format(target.name, target.name))
        for mob in self.mobs:
            react = mob.courage_check()
            if react == "attack" or react == "charge":
                mob.attack_melee(target)
            elif react == "defend" or react == "flee":
                mob.stand_ground()

    def surround_enemy(self, args):
        leader = args[0]
        target = args[1]
        leader.shout("Surround him! Surround the {}".format(target.name))
        num = 0
        for mob in self.mobs:
            num += 1
            react = mob.courage_check()
            if react == "attack" or react == "charge" or react == "defend":
                mob.surround(target, num)
            elif react == "flee":
                mob.flee(target)



class GroupThink(object):
    def __init__(self, amount, mtype):
        self.mobs = self.gen_mobs(amount, mtype)
        self.strategies = Strategies(self.mobs)
        self.log = Log()
        self.group_events = {
        "Enemy_spotted":[False, self.strategies.enemy_spotted, []],
        "Surround_enemy":[False, self.strategies.surround_enemy, []]
        }

    def selection():
        pass

    def gen_mobs(self, amount, mtype):
        if mtype == "Goblin":
            courage = 25
        elif mtype == "Orc":
            courage = 50
        elif mtype == "Ogre":
            courage = 75

        mobs = []
        num = 1
        for m in xrange(amount):
            mobs.append(Mob(mtype, "{}{}".format(mtype, num), courage, 50, self))
            num += 1
        return mobs


    def update(self):
        self.update_events()

    def update_events(self):
        for event in self.group_events:
            if self.group_events[event][0]:
                args = self.group_events[event][2]
                self.group_events[event][1](args)
                self.group_events[event][0] = False

    def broadcast(self, mssg):
        self.log.record(mssg)
        print mssg



