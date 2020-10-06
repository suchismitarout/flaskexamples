class C:
    def __init__(self):
        print("c constructor")

class D(C):
    def __init__(self):
        super(D, self).__init__()
        print("D constructor")

if __name__ == '__main__':
    d = D()
    