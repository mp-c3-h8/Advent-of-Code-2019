import os.path
import os
from timeit import default_timer as timer


'''
part2 adapted from:
 - https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbwp0r0/
 - https://topaz.github.io/paste/#XQAAAQAgBQAAAAAAAAAzHIoib6pENkSmUIKIED8dy140D1lKWSMhNhZz+hjKgIgfJKPuwdqIBP14lxcYH/qI+6TyUGZUnsGhS4MQYaEtf9B1X3qIIO2JSejFjoJr8N1aCyeeRSnm53tWsBtER8F61O2YFrnp7zwG7y303D8WR4V0eGFqtDhF/vcF1cQdZLdxi/WhfyXZuWC+hs8WQCBmEtuId6/G0PeMA1Fr78xXt96Um/CIiLCievFE2XuRMAcBDB5We73jvDO95Cjg0CF2xgF4yt3v4RB9hmxa+gmt6t7wRI4vUIGoD8kX2k65BtmhZ7zSZk1Hh5p1obGZ6nuuFIHS7FpuSuv1faQW/FuXlcVmhJipxi37mvPNnroYrDM3PFeMw/2THdpUwlNQj0EDsslC7eSncZQPVBhPAHfYojh/LlqSf4DrfsM926hSS9Fdjarb9xBYjByQpAxLDcmDCMRFH5hkmLYTYDVguXbOCHcY+TFbl+G/37emZRFh/d+SkeGqbFSf64HJToM2I7N2zMrWP7NDDY5FWehD5gzKsJpEg34+sG7x2O82wO39qBlYHcYg1Gz4cLBrH1K1P+KWvEdcdj/NBtrl6yftMlCu6pH4WTGUe9oidaiRuQZOGtw71QsTQUuhpdoWO4mEH0U9+CiPZCZLaQolFDSky1J9nDhZZHy3+ETcUeDOfSu+HI3WuKC0AtIRPdG8B9GhtxZQKAx+5kyi/ek7A2JAY9SjrTuvRADxx5AikbHWXIsegZQkupAc2msammSkwY8dRMk0ilf5vh6kR0jHNbSi0g0KJLCJfqggeX24fKk5Mdh8ULZXnMfMZOmwEGfegByYbu91faLijfW4hoXCB1nlsWTPZEw2PCZqqhl9oc1q25H2YkkvKLxEZWl6a9eFuRzxhB840I1zdBjUVgfKd9/V4VdodzU2Z2e+VEh7RbJjQNFC/rG8dg==
key insights: 
 - linear modular equations
 - fast modular exponentiation (pow does it)
 - modular inverse (fermat)
'''


def part2(data: str) -> int:
    n = 119315717514047
    c = 2020

    a, b = 1, 0
    for line in data.splitlines():
        words = line.split()
        if words[0] == "cut":  # cut
            num = int(words[-1])
            la, lb = 1, -num
        elif words[1] == "with":  # increment
            num = int(words[-1])
            la, lb = num, 0
        else:  # new stack
            la, lb = -1, -1
        a = (la * a) % n
        b = (la * b + lb) % n

    M = 101741582076661

    # Fermat's little theorem
    def inv(a, n): return pow(a, n-2, n)

    Ma = pow(a, M, n)
    Mb = (b * (Ma - 1) * inv(a-1, n)) % n

    return ((c - Mb) * inv(Ma, n)) % n


def shuffle(data: str, decksize: int) -> int:
    deck = [*range(decksize)]

    for line in data.splitlines():
        words = line.split()
        if words[0] == "cut":  # cut
            num = int(words[-1])
            deck = deck[num:] + deck[:num]
        elif words[1] == "with":  # increment
            temp = [0]*decksize
            num = int(words[-1])
            for i in range(decksize):
                temp[i*num % decksize] = deck[i]
            deck = temp
        else:  # new stack
            deck = deck[::-1]
    return deck.index(2019)


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


print("Part 1:", shuffle(data, 10007))
print("Part 2:", part2(data))


e = timer()
print(f"time: {e-s}")
