import math, random

def generar_normal(media,desv):
    random1 = random.random()
    random2 = random.random()
    n1 = ((math.sqrt(-2 * math.log(random1)) * math.cos(2 * math.pi * random2)) * desv) + media
    n2 = ((math.sqrt(-2 * math.log(random1)) * math.sin(2 * math.pi * random2)) * desv) + media
    if n1 < 0:
        n1 = n1 * (-1)
    return round(n1,4)

def generar_uniforme():
    return round((4+random.random()*2), 4)

def generar_exponencial():
    media=50/60
    return round((-media*math.log(1 - random.random())), 4)


def generar_estadoinicial():
    rnd=random.random()
    if rnd<0.60:
        return "EC"
    elif rnd<0.90:
        return "ES"
    else:
        return "P"