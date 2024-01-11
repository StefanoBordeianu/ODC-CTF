import z3
import math

def convert(s): 
 
    # initialization of string to "" 
    new = "" 
 
    # traverse in the string 
    for x in s: 
        new += x 
 
    # return string 
    return new 


def execution(c,seed):
    var = 0x8000000000000000

    v6 = math.sqrt(c)
    v7 = pow(c,v6)
    #print(v7)

    if(v7 >= var):
        #print("in")
        v8 = v7- var
        v8 = round(v8)
        v8 = v8 ^ 0x80000000
    else:
        v8 = round(v7)
    
    #print(hex(v8+21))
    if(seed == v8+21):
        return 1
    else:
        return 0
      

s = 0xa66fe7dd0000001c

seeds = []
seeds.append(0x1ca66fe7dd)
seeds.append(0x227357afcf8)
seeds.append(0x15)
seeds.append(0x16c5c156c54)

seeds.append(0x1ca66fe7dd)
seeds.append(0x9de93ece66)
seeds.append(0x16c5c156c54)

seeds.append(0x16c5c156c54)
seeds.append(0x756f3444241)
seeds.append(0x014660a4c5)

chars = []

for i in range(0x20,0x7f):
    chars.append(i)

r = []
for seed in seeds:
    for c in chars:
        res = execution(c,seed)
        if res ==1:
            r.append(chr(c))
            print(c)

print(convert(r))
