from mathlib import *

def main(gi):
    total = 0
    for i in gi.data:
        total += float(i[3])*float(i[3])
    print(total/31)
