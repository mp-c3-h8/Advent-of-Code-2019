import os.path
import os
from timeit import default_timer as timer


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


e = timer()
print(f"time: {e-s}")
