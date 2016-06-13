"""Figuring out noise.
This code is lifted from:
    http://freespace.virgin.net/hugo.elias/models/m_perlin.htm
See also:
    http://mrl.nyu.edu/~perlin/doc/oscar.html
    http://www.noisemachine.com/talk1
    http://webstaff.itn.liu.se/~stegu/TNM022-2005/perlinnoiselinks/perlin-noise-math-faq.html
"""

import math



def noise(x, y):
    n = x + y * 57
    n = (n<<13) ^ n
    return 1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0   

# def smoothed_noise(x, y):
#     corners = (noise(x-1, y-1) + noise(x+1, y-1) + noise(x-1, y+1) + noise(x+1, y+1)) / 16
#     sides = (noise(x-1, y) + noise(x+1, y) + noise(x, y-1) + noise(x, y+1)) /  8
#     center = noise(x, y) / 4
#     return corners + sides + center

# def smoothed_noise(x, y):
#     corners = (noise(x-1, y-1) + noise(x+1, y-1) + noise(x-1, y+1) + noise(x+1, y+1)) / 16
#     sides = (noise(x-1, y) + noise(x+1, y) + noise(x, y-1) + noise(x, y+1)) /  8
#     center = noise(x, y) / 8
#     return corners + sides + center

def smoothed_noise(x, y):
    corners = (noise(x-1, y-1) + noise(x+1, y-1) + noise(x-1, y+1) + noise(x+1, y+1)) / 16
    sides = (noise(x-1, y) + noise(x+1, y) + noise(x, y-1) + noise(x, y+1)) /  12
    center = noise(x, y) / 8
    return corners + sides + center

def interpolate(a, b, x):
    """The Cosine Interpolation from:
    
    http://freespace.virgin.net/hugo.elias/models/m_perlin.htm
    """
    ft = x * math.pi
    f = (1 - math.cos(ft)) * .5
    return  a*(1-f) + b*f

def interpolated_noise(x, y):
    integer_X = int(x)
    fractional_X = x - integer_X
    
    integer_Y = int(y)
    fractional_Y = y - integer_Y
    
    v1 = smoothed_noise(integer_X, integer_Y)
    v2 = smoothed_noise(integer_X+1, integer_Y)
    v3 = smoothed_noise(integer_X, integer_Y+1)
    v4 = smoothed_noise(integer_X+1, integer_Y+1)
    
    i1 = interpolate(v1, v2, fractional_X)
    i2 = interpolate(v3, v4, fractional_X)    
    return interpolate(i1, i2, fractional_Y)

def perlin(x, y, octaves, persistence):
    total = 0

    for i in range(octaves):
        frequency = 2**i
        amplitude = persistence**i

        total += interpolated_noise(x*frequency, y*frequency) * amplitude

    return total