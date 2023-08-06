import random
import sys


def prob():
    n_times = int(sys.argv[1])
    choices = sys.argv[2:]
    di = {}
    for _ in range(n_times):
        choice = random.choice(choices)
        di[choice] = di.get(choice, 0) + 1

    for k, v in di.items():
        print(f'{k}: {v}')

    print("*"*25, end=' ')
    print(f"THE WINNER is {max(di, key=di.get)}", end=' ')
    print("*"*25)
