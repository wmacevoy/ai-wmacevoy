import unittest
import math, random

from redblackbst import RedBlackBST
from typing import List
class RedBlackBSTTest(unittest.TestCase):
    def testDefault(self):
        t : RedBlackBST[int,str] = RedBlackBST[int,str]()
        testKey : int = 1
        testValue : str = "one"

        self.assertEqual(t.size,0)
        self.assertEqual(t.empty,True)
        self.assertEqual(t.contains(testKey),False)

        t.put(testKey,testValue)
        self.assertEqual(t.size,1)
        self.assertEqual(t.empty,False)
        self.assertEqual(t.contains(testKey),True)

        t.delete(testKey)

        self.assertEqual(t.size,0)
        self.assertEqual(t.empty,True)
        self.assertEqual(t.contains(testKey),False)

    def testUp(self):
        n : int = 1000
        m : float = 0.0
        t : RedBlackBST[int,str] = RedBlackBST[int,str]()
        for x in range(n):
            t.put(x,str(x))
            m = max(m, t.height/max(1.0,math.log2(t.size)))

        for x in range(n):
            self.assertTrue(t.contains(x))
        print("up m=" + str(m))
        self.assertTrue(m < 2.0)

    def testDown(self):
        n : int = 1000
        m : float = 0.0
        t : RedBlackBST[int,str] = RedBlackBST[int,str]()
        for x in range(n):
            t.put(n-x,str(x))
            m = max(m, t.height/max(1.0,math.log2(t.size)))

        for x in range(n):
            self.assertTrue(t.contains(n-x))
        print("down m=" + str(m))
        self.assertTrue(m < 2.0)

    def testRandom(self):
        n : int = 1000
        m : float = 0.0
        t : RedBlackBST[int,str] = RedBlackBST[int,str]()
        xs : List[int] = [random.randint(0,n*n) for i in range(n)]
        for x in xs:
            t.put(x,str(x))
            m = max(m, t.height/max(1.0,math.log2(t.size)))

        for x in xs:
            self.assertTrue(t.contains(x))
        print("rand m=" + str(m))
        self.assertTrue(m < 2.0)


if __name__ == '__main__':
    unittest.main()
