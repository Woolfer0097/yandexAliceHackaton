import time


def main():
    SQAURES = list(map(lambda x: {x: x * x}, range(1, 100)))
    print(SQAURES, SQAURES)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print((time.time() - start_time))
