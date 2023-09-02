# TODO

def main():
    n = 0
    # taking the input
    while (n < 1 or n > 8):
        try:
            n = int(input("Height: "))
        except ValueError:
            n = 0

    draw(n)


# drawing shape of heiight n
def draw(n):
    for i in range(n):
        for j in range(n-i-1):
            print(' ', end="")
        for j in range(i+1):
            print('#', end="")
        print("")


main()