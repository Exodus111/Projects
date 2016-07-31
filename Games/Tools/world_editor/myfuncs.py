from path import Path

def set_dir(file_path):
    here = Path(file_path).parent
    here.chdir()


def check_dir(file_name):
    this = Path(".")
    print(this.abspath())
    if file_name not in this.files():
        myglob = this.glob("*/**/{}".format(file_name))
        myfile = myglob[0]
        myfolder = myfile.parent
        myfolder.chdir()

mytimers = {}

def mytimer(name, seconds, dt, first=True):
    global mytimers
    if name in mytimers.keys():
        if mytimers[name] < dt:
            mytimers[name] = dt + seconds
            return True
        else:
            return False
    else:
        mytimers[name] = dt + seconds
        if first:
            return True
        else:
            return False

def remove_timer(name):
    if name in mytimers.keys():
        mytimers.pop(name, None)


def tuple_add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def tuple_sub(t1, t2):
    return (t1[0] - t2[0], t1[1] - t2[1])

def tuple_mult(t1, n):
    return (t1[0]*n, t1[1]*n)

def tuple_div(t1, n):
    return (t1[0]/n, t1[1]/n)

def extract_images(filename, out_folder, group_name="mapfile"):
    from PIL import Image
    im = Image.open(filename)
    size = im.size
    b = 64
    x_size = int(size[0]/b)
    y_size = int(size[1]/b)
    num = 1
    for y in xrange(y_size):
        for x in xrange(x_size):
            l = x*b
            u = y*b
            r = l+b
            d = u+b
            a = im.crop((l,u,r,d))
            a.save("{}{}{}.png".format(out_folder, group_name, num))
            num += 1



if __name__ == "__main__":
    extract_images("./img/magecity_64p.png", "./tiles/sheet_images/")
