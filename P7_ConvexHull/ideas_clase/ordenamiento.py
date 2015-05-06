''' A el le gustaria que existiera una clase "segmento" que encapsulara
todas las funciones de distancia punto-segmento, o comprobar si está a la dcha
del segmento, o cosas de ese estilo.

No se si realmente funcionaría, y si sería muy lento o super lento
'''

from functools import total_ordering

@total_ordering
class Point:
    def __init__(self, P):
        self.x = P[0]
        self.y = P[1]

    def __repr__(self):
        return 'Point(%s, %s)'%(self.x, self.y)

    def __eq__(self, other):
        return((self.x, self.y) == (other.x, other.y))

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x == other.x:
            return self.y > other.y
        else:
            return False



if __name__=='__main__':
    p = Point([1,2])
    q = Point([1,2])

    print p == q

    L = [[1,2],[-3,1], [-3, 2], [5,7]]

    ptos = [Point(P) for P in L]
    print sorted(ptos)
