import unittest
from TriplePair import *


class MyTestCase(unittest.TestCase):
    def test_01(self):
        a: TriplePair = TriplePair(1, 2, 3)
        b: TriplePair = TriplePair(4, 5, 6)
        c: TriplePair = a.zip(b)
        self.assertEquals(c, TriplePair((1, 4), (2, 5), (3, 6)))

    def test_02(self):
        a: TriplePair = TriplePair(1, 2, 3)
        b: TriplePair = TriplePair(4, 5, 6)
        c: TriplePair = a.sum(b)
        self.assertEquals(c, TriplePair(5, 7, 9))

    def test_03(self):
        x: TriplePair = TriplePair("a", "b", "c")
        y: TriplePair = TriplePair("d", "e", "f")
        z: TriplePair = x.zip(y)
        self.assertEquals(z, TriplePair(("a", "d"), ("b", "e"), ("c", "f")))


if __name__ == '__main__':
    unittest.main()
