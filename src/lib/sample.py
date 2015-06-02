#coding=utf8
import random
import sys

def ran_sample(n,bo):
    go = 0
    if bo == 1:
        n -= 1
        if n == 0:
            n = 1
        go = 1 
    else:
        q = random.randint(1,n)
        if q == 1:
            go = 1
            n += 1
    return (go,n)


def main():
    n = 1
    index = 1
    while True:
        line = sys.stdin.readline()
        if not line:break
        line = line.strip()
        if line == "1":
            (go,n) = ran_sample(n,1)
            if go == 1:
                print str(index),line
        else:
            (go,n) = ran_sample(n,0)
            if go == 1:
                print str(index),line
        index += 1
if __name__ == "__main__":
    main()
