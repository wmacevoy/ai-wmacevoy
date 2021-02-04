#
# Port of red black bst from Java AI 2018
#

# from __future__ import annotations

from typing import Sized, TypeVar,Generic,Optional,cast,List

Key = TypeVar('Key')
Value = TypeVar('Value')

class RedBlackBSTNode(Generic[Key,Value]):
        def __init__(self, key : Key, value : Value, color : bool, size : int):
            self.key : Key = key
            self.value : Value = value
            self.color : bool = color
            self.size : int = size
            self.left : Optional[RedBlackBSTNode[Key,Value]] = None
            self.right : Optional[RedBlackBSTNode[Key,Value]] = None
    

class RedBlackBST(Generic[Key,Value]):
    RED : bool = True
    BLACK : bool = False    

    def __init__(self):
        self._root : Optional[RedBlackBSTNode[Key,Value]] = None

    @classmethod
    def _isRed(cls,x : Optional[RedBlackBSTNode[Key,Value]]) -> bool:
        if x == None:
            return False
        return x.color == cls.RED

    @classmethod
    def _isBlack(cls,x : Optional[RedBlackBSTNode[Key,Value]]) -> bool:
        if x == None:
            return True
        return x.color == cls.BLACK
    
    @classmethod
    def _size(cls, x : Optional[RedBlackBSTNode[Key,Value]]) -> int:
        if x == None:
            return 0
        return x.size

    @property
    def size(self) -> int:
        return self._size(self._root)

    @property
    def empty(self) -> bool:
        return self._root == None

    
    def get(self,key : Key) -> Optional[Value]:
        return self._get(self._root, key)

    @classmethod
    def _get(cls,x : Optional[RedBlackBSTNode[Key,Value]], key : Key) -> Optional[Value]:
        while x != None:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x.value
        return None

    def contains(self,key : Key) -> bool:
        return self.get(key) != None

    def put(self,key : Key, value : Value):
        self._root = self._put(self._root,key,value)
        self._root.color = self.BLACK 

    @classmethod
    def _put(cls,h : Optional[RedBlackBSTNode[Key,Value]], key : Key, value : Value):
        if h == None:
            return RedBlackBSTNode[Key,Value](key, value, cls.RED, 1)
        if key < h.key:
            h.left = cls._put(h.left,key,value)
        elif key > h.key:
            h.right = cls._put(h.right,key,value)
        else:
            h.value = value

        if cls._isRed(h.right) and cls._isBlack(h.left):
            h = cls._rotateLeft(h)
        if cls._isRed(h.left) and cls._isRed(h.left.left):
            h = cls._rotateRight(h)
        if cls._isRed(h.left) and cls._isRed(h.right):
            cls._flipColors(h)
        h.size = cls._size(h.left) + cls._size(h.right) + 1
        return h

    def deleteMin(self) -> None:
        if self.empty:
            raise ValueError("BST underflow")

        if not self._isRed(self._root.left) and self._isBlack(self._root.right):
            self._root.color = self.RED

        self._root = self._deleteMin(cast(RedBlackBSTNode[Key,Value],self._root))
        if not self.empty:
            self._root.color = self.BLACK

    @classmethod
    def _deleteMin(cls,h : RedBlackBSTNode[Key,Value]) -> Optional[RedBlackBSTNode[Key,Value]]:
        if h.left == None:
            return None
        if cls._isBlack(h.left) and cls._isBlack(h.left.left):
            h = cls._moveRedLeft(h)

        h.left = cls._deleteMin(h.left)
        return cls._balance(h)

    def deleteMax(self) -> None:
        if self.empty:
            raise ValueError("BST underflow")
        if self._isBlack(self._root.left) and self._isBlack(self._root.right):
            self._root.color = self.RED

        self._root = self._deleteMax(cast(RedBlackBSTNode[Key,Value],self._root))
        if not self.empty:
            self._root.color = self.BLACK


    @classmethod
    def _deleteMax(cls,h : RedBlackBSTNode[Key,Value]) -> Optional[RedBlackBSTNode[Key,Value]]:
        if cls._isRed(h.left):
            h = cls._rotateRight(h)
        if h.right == None:
            return None
        if cls._isBlack(h.right) and cls._isBlack(h.right.left):
            h = cls._moveRedRight(h)
        h.right = cls._deleteMax(h.right)

        return cls._balance(h)

    def delete(self,key : Key) -> None:
        if not self.contains(key):
            return

        if self._isBlack(self._root.left) and self._isBlack(self._root.right):
            self._root.color = self.RED

        self._root = self._delete(cast(RedBlackBSTNode[Key,Value],self._root), key)
        if not self.empty:
            self._root.color = self.BLACK
        if not self.empty:
            self._root.color = self.BLACK

    @classmethod
    def _delete(cls,h : RedBlackBSTNode[Key,Value], key : Key) -> Optional[RedBlackBSTNode[Key,Value]]:
        if key < h.key:
            if cls._isBlack(h.left) and cls._isBlack(h.left.left):
                h = cls._moveRedLeft(h)
            h.left = cls._delete(cast(RedBlackBSTNode[Key,Value],h.left), key)
        else:
            if cls._isRed(h.left):
                h = cls._rotateRight(h)
            if key == h.key and h.right == None:
                return None
            if cls._isBlack(h.right) and cls._isBlack(h.right.left):
                h = cls._moveRedRight(h)
            if key == h.key:
                x : RedBlackBSTNode[Key,Value][Key,Value] = cls._min(cast(RedBlackBSTNode[Key,Value],h.right))
                h.key = x.key
                h.value = x.value
                h.right = cls._deleteMin(cast(RedBlackBSTNode[Key,Value],h.right))
            else:
                h.right = cls._delete(cast(RedBlackBSTNode[Key,Value],h.right), key)
        return cls._balance(h)

    @classmethod
    def _rotateRight(cls,h : RedBlackBSTNode[Key,Value]) -> RedBlackBSTNode[Key,Value]:
        x : RedBlackBSTNode[Key,Value] = cast(RedBlackBSTNode[Key,Value],h.left)
        h.left = x.right
        x.right = h
        x.color = x.right.color
        x.right.color = cls.RED
        x.size = h.size
        h.size = cls._size(h.left) + cls._size(h.right) + 1
        return x

    @classmethod
    def _rotateLeft(cls,h : RedBlackBSTNode[Key,Value]) -> RedBlackBSTNode[Key,Value]:
        x : RedBlackBSTNode[Key,Value] = cast(RedBlackBSTNode[Key,Value],h.right)
        h.right = x.left
        x.left = h
        x.color = x.left.color
        x.left.color = cls.RED
        x.size = h.size
        h.size = cls._size(h.left) + cls._size(h.right) + 1
        return x

    @classmethod
    def _flipColors(cls,h : RedBlackBSTNode[Key,Value]) -> None:
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color

    @classmethod
    def _moveRedLeft(cls,h : RedBlackBSTNode[Key,Value]) -> RedBlackBSTNode[Key,Value]:
        cls._flipColors(h)
        if cls._isRed(h.right.left):
            h.right = cls._rotateRight(cast(RedBlackBSTNode[Key,Value],h.right))
            h = cls._rotateLeft(h)
            cls._flipColors(h)
        return h

    @classmethod
    def _moveRedRight(cls,h : RedBlackBSTNode[Key,Value]) -> RedBlackBSTNode[Key,Value]:
        cls._flipColors(h)
        if cls._isRed(h.left.left):
            h = cls._rotateRight(h)
            cls._flipColors(h)
        return h

    @classmethod
    def _balance(cls,h : RedBlackBSTNode[Key,Value]) -> RedBlackBSTNode[Key,Value]:
        if cls._isRed(h.right):
            h = cls._rotateLeft(h)
        if cls._isRed(h.left) and cls._isRed(h.left.left): 
            h = cls._rotateRight(h)
        if cls._isRed(h.left) and cls._isRed(h.right):
            cls._flipColors(h)
        h.size = cls._size(h.left) + cls._size(h.right) + 1
        return h

    @property
    def height(self) -> int:
        return self._height(self._root)

    @classmethod
    def _height(cls,x : Optional[RedBlackBSTNode[Key,Value]]) -> int:
        if x == None:
            return -1
        return 1 + max(cls._height(x.left), cls._height(x.right))
    
    def min(self) -> Key:
        if self.empty:
            raise ValueError("min of empty tree")
        return self._min(cast(RedBlackBSTNode[Key,Value],self._root)).key

    @classmethod
    def _min(cls,x : RedBlackBSTNode[Key,Value]) -> RedBlackBSTNode[Key,Value]:
        if x.left == None:
            return x
        return cls._min(x.left)

    def max(self) -> Key:
        if self.empty:
            raise ValueError("max of empty tree")
        return self._max(cast(RedBlackBSTNode[Key,Value],self._root)).key

    @classmethod
    def _max(cls,x : RedBlackBSTNode[Key,Value]) -> RedBlackBSTNode[Key,Value]:
        if x.right == None:
            return x
        return cls._max(x.right)

    def floor(self,key : Key) -> Optional[Key]:
        x : Optional[RedBlackBSTNode[Key,Value]]  = self._floor(self._root,key)
        return x.key if x != None else None

    @classmethod
    def _floor(cls,x : Optional[RedBlackBSTNode[Key,Value]], key : Key) -> Optional[RedBlackBSTNode[Key,Value]]:
        if x == None:
            return None
        if key == x.key:
            return x
        if key < x.key:
            return cls._floor(x.left,key)
        t : Optional[RedBlackBSTNode[Key,Value]] = cls._floor(x.right, key)
        return t if t != None else x

    def ceiling(self,key : Key) -> Optional[Key]:
        x : Optional[RedBlackBSTNode[Key,Value]] = self._ceiling(self._root, key)
        return x.key if x != None else None

    @classmethod
    def _ceiling(cls,x : Optional[RedBlackBSTNode[Key,Value]], key : Key) -> Optional[RedBlackBSTNode[Key,Value]]:
        if x == None:
            return None
        if key == x.key:
            return x
        if key > x.key:
            return cls._ceiling(x.right,key)
        t : Optional[RedBlackBSTNode[Key,Value]] = cls._ceiling(x.left,key)
        return t if t != None else x

    def select(self, k : int) -> Key:
        if k < 0 or k >= self.size:
            raise ValueError("invalid select index")
        x : RedBlackBSTNode[Key,Value] = self._select(cast(RedBlackBSTNode[Key,Value],self._root),k)
        return x.key

    @classmethod
    def _select(cls,x : RedBlackBSTNode[Key,Value], k : int) -> RedBlackBSTNode[Key,Value]:
        t = cls._size(x)
        if t > k:
            return cls._select(cast(RedBlackBSTNode[Key,Value],x.left),k)
        elif t < k:
            return cls._select(cast(RedBlackBSTNode[Key,Value],x.right),k-t-1)
        else:
            return x

    def rank(self, key : Key) -> int:
        return self._rank(key, self._root)

    @classmethod
    def _rank(cls, key : Key, x : Optional[RedBlackBSTNode[Key,Value]]):
        if x == None:
            return 0
        if key < x.key:
            return cls._rank(key,x.left)
        elif key > x.key:
            return 1 + cls._size(x.left) + cls._rank(key,key.right)
        else:
            return cls._size(x.left)

    def keys(self) -> List[Key]:
        if self.empty:
            return []
        else:
            return self.keysInRange(self.min(),self.max())

    def keysInRange(self,lo : Key, hi : Key) -> List[Key]:
        queue : List[Key] = []
        self._keysInRange(self._root,queue, lo, hi)
        return queue

    @classmethod
    def _keysInRange(cls, x : Optional[RedBlackBSTNode[Key,Value]], queue : List[Key], lo : Key, hi : Key) -> None:
        if x == None:
            return
        if lo < x.key:
            cls._keysInRange(x.left, queue, lo, hi)
        if lo <= x.key and x.key <= hi:
            queue.append(x.key)
        if hi > x.key:
            cls._keysInRange(x.right, queue, lo, hi)

    def sizeInRange(self, lo : Key, hi : Key) -> int:
        if lo > hi:
            return 0
        if self.contains(hi):
            return self.rank(hi) - self.rank(lo) + 1
        else:
            return self.rank(hi) - self.rank(lo)

    def _node(self,i : int) -> RedBlackBSTNode[Key,Value]:
        p : RedBlackBSTNode[Key,Value] = cast(RedBlackBSTNode[Key,Value],self._root)
        while i > 0:
            i -= 1
            if p.left != None:
                if i < p.left.size:
                    p = p.left
                else:
                    i -= p.left.size
                    p = cast(RedBlackBSTNode[Key,Value],p.right)
            else:
                p = cast(RedBlackBSTNode[Key,Value],p.right)
        return p

    def key(self, i : int) -> Key:
        return self._node(i).key
    
    def clear(self) -> None:
        self._root = None

