from typing import List


def find(arr: List, num, ndec ,pos):
    ris = -1
    for x in arr:
        try:
            if(round(x[pos], ndec)==num and ris != -1):
                ris = len(arr)
            elif(round(x[pos], ndec)==num):
                ris = arr.index(x)
        except IndexError:
            pass

    return ris
        

def frange(start, stop, step=1.0):
    if(start > stop):
        step *= -1
    curr = float(start)
    tmp = []
    while curr > stop:
        tmp.append(round(curr, 8))
        curr += step
    tmp.append(float(stop))
    return tmp


def plot(iny: List, ystep=1, lowlim=None, highlim=None, car='*'):
    ndec = 0
    if isinstance(ystep, float):
        ndec = len(str(ystep).split(".")[1])
            
    if lowlim == None:
        lowlim = round(min(iny), ndec)-ystep
    if highlim == None:
        highlim = round(max(iny), ndec)+ystep
        

    for y in frange(highlim, lowlim, ystep):
        if(y >= 0):
            print(f' {abs(y)}|', end="")
        else:
            print(f'{y}|', end="")

        if(y == 0):
            for x in iny:
                if(round(x, ndec) == y):
                    print(car, end="")
                else:
                    print("--", end="")
        else:
            for x in iny:
                if(round(x, ndec) == y):
                    print(car, end="")
                else:
                    print("  ", end="")
        print("")

    print()


def mplot(iny: List, ystep=1, lowlim=None, highlim=None, car: List = ['*', '#', '@'], labels:List=None):

    ndec = 0
    if isinstance(ystep, float):
        ndec = len(str(ystep).split(".")[1])

    if lowlim == None:
        for serie in iny:
            if(iny[0] == serie):
                mymin = min(serie)
            elif(min(serie) < mymin):
                mymin = min(serie)
            lowlim = round(mymin, ndec) - ystep
    if highlim == None:
        for serie in iny:
            if(iny[0] == serie):
                mymax = max(serie)
            elif(max(serie) > mymax):
                mymax = max(serie)
            highlim = round(mymax,ndec) + ystep
            
    for serie in iny:
        if(iny[0]== serie):
            xdim = len(serie)
        elif(len(serie) > xdim):
            xdim = len(serie)

    for y in frange(highlim, lowlim, ystep):
        if(y >= 0):
            print(f' {abs(y)}|', end="")
        else:
            print(f'{y}|', end="")

       
        if(y == 0):
            for x in range(xdim):
                if(find(iny, y, ndec ,x) != -1):
                    print(car[find(iny, y, ndec ,x)], end=" ")
                else:
                    print("--", end="")
            
        else:
            for x in range(xdim):
                if(find(iny, y, ndec ,x) != -1):
                    print(car[find(iny, y, ndec ,x)], end=" ")
                else:
                    print("  ", end="")
        print("")

    print()
        
    if (labels != None):
        for label in labels:
            print(f'{car[labels.index(label)]}: {label}')
        print(f'{car[-1]}: overlaps')

    