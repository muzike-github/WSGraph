count = 0


def test():
    global count
    for i in range(0, 10):
        count = count + 1


test()
print(count)
