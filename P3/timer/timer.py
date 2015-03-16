from time import time

class Timer:
    def __init__(self):
        self.start = time()
        self.acumulado = 0
    def finalizar(self):
        return self.acumulado + time() - self.start
    def pausar(self):
        self.acumulado += time() - self.start
    def continuar(self):
        self.start = time()
    def comenzar(self):
        self.start = time()
        self.acumulado = 0


# if __name__ == "__main__":
#     T = Timer();
#     v = 1;
#     for i in range(90000):
#         v = v * i
#     print T.finalizar()
