from __future__ import annotations

import typing as _t
from abc import (ABC,
                 abstractmethod)
from copy import deepcopy
from itertools import chain

import typing_extensions as _te
from reprit.base import generate_repr

from .hints import (Item,
                    Key,
                    Key_co,
                    Value)
from .utils import capacity

Nil = type(None)
NIL: Nil = None


class Node(_te.Protocol[Key_co, Value]):
    @property
    @abstractmethod
    def left(self) -> _t.Union[Nil, _te.Self]:
        """Left child."""

    @left.setter
    @abstractmethod
    def left(self, _value: _t.Union[Nil, _te.Self]) -> None:
        """Sets left child."""

    @property
    @abstractmethod
    def right(self) -> _t.Union[Nil, _te.Self]:
        """Right child."""

    @right.setter
    @abstractmethod
    def right(self, _value: _t.Union[Nil, _te.Self]) -> None:
        """Sets right child."""

    @property
    def item(self) -> Item[Key_co, Value]:
        return self.key, self.value

    @property
    @abstractmethod
    def key(self) -> Key_co:
        """Comparisons key."""

    @property
    @abstractmethod
    def value(self) -> Value:
        """Underlying value."""

    @value.setter
    def value(self, value: Value) -> None:
        pass


class Tree(ABC, _t.Generic[Key, Value]):
    root: _t.Union[Nil, Node[Key, Value]]

    __slots__ = 'root',

    def __init__(self, root: _t.Union[Nil, Node[Key, Value]]) -> None:
        self.root = root

    def __bool__(self) -> bool:
        """Checks if the tree has nodes."""
        return self.root is not NIL

    def __copy__(self) -> _te.Self:
        return type(self)(deepcopy(self.root))

    def __iter__(self) -> _t.Iterator[Node[Key, Value]]:
        """Returns iterator over nodes in ascending keys order."""
        node = self.root
        queue = []
        while True:
            while node is not NIL:
                queue.append(node)
                node = node.left
            if not queue:
                return
            node = queue.pop()
            yield node
            node = node.right

    def __len__(self) -> int:
        """Returns number of nodes."""
        return capacity(self)

    def __reversed__(self) -> _t.Iterator[Node[Key, Value]]:
        """Returns iterator over nodes in descending keys order."""
        node = self.root
        queue = []
        while True:
            while node is not NIL:
                queue.append(node)
                node = node.right
            if not queue:
                return
            node = queue.pop()
            yield node
            node = node.left

    @_t.overload
    @classmethod
    def from_components(cls,
                        keys: _t.Iterable[Key],
                        values: None = ...) -> Tree[Key, Key]:
        ...

    @_t.overload
    @classmethod
    def from_components(cls,
                        keys: _t.Iterable[Key],
                        values: _t.Iterable[Value]) -> _te.Self:
        ...

    @classmethod
    @abstractmethod
    def from_components(
            cls: _t.Union[_t.Type[Tree[Key, Key]], _t.Type[Tree[Key, Value]]],
            keys: _t.Iterable[Key],
            values: _t.Optional[_t.Iterable[Value]] = None
    ) -> _t.Union[Tree[Key, Key], Tree[Key, Value]]:
        """Constructs tree from given components."""

    __repr__ = generate_repr(from_components,
                             with_module_name=True)

    @property
    def keys(self) -> _t.List[Key]:
        return _t.cast(_t.List[Key], [node.key for node in self])

    @property
    def values(self) -> _t.List[Value]:
        return [node.value for node in self]

    def clear(self) -> None:
        self.root = NIL

    def find(self, key: Key) -> _t.Union[Nil, Node[Key, Value]]:
        """Searches for the node corresponding to a key."""
        node = self.root
        while node is not NIL:
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                break
        return node

    def infimum(self, key: Key) -> _t.Union[Nil, Node[Key, Value]]:
        """Returns first node with a key not greater than the given one."""
        node, result = self.root, NIL
        while node is not NIL:
            if key < node.key:
                node = node.left
            elif node.key < key:
                result, node = node, node.right
            else:
                result = node
                break
        return result

    @abstractmethod
    def insert(self, key: Key, value: Value) -> Node[Key, Value]:
        """Inserts given key-value pair in the tree."""

    def max(self) -> _t.Union[Nil, Node[Key, Value]]:
        """Returns node with the maximum key."""
        node = self.root
        if node is not NIL:
            while node.right is not NIL:
                node = node.right
        return node

    def min(self) -> _t.Union[Nil, Node[Key, Value]]:
        """Returns node with the minimum key."""
        node = self.root
        if node is not NIL:
            while node.left is not NIL:
                node = node.left
        return node

    def pop(self, key: Key) -> _t.Union[Nil, Node[Key, Value]]:
        """Removes node with given key from the tree."""
        node = self.find(key)
        if node is not NIL:
            self.remove(node)
        return node

    def popmin(self) -> _t.Union[Nil, Node[Key, Value]]:
        node = self.root
        if node is not NIL:
            while node.left is not NIL:
                node = node.left
            self.remove(node)
        return node

    def popmax(self) -> _t.Union[Nil, Node[Key, Value]]:
        node = self.root
        if node is not NIL:
            while node.right is not NIL:
                node = node.right
            self.remove(node)
        return node

    @abstractmethod
    def predecessor(self,
                    node: Node[Key, Value]) -> _t.Union[Nil, Node[Key, Value]]:
        """Returns last node with a key less than of the given one."""

    @abstractmethod
    def remove(self, node: Node[Key, Value]) -> None:
        """Removes node from the tree."""

    @abstractmethod
    def successor(self,
                  node: Node[Key, Value]) -> _t.Union[Nil, Node[Key, Value]]:
        """Returns first node with a key greater than of the given one."""

    def supremum(self, key: Key) -> _t.Union[Nil, Node[Key, Value]]:
        """Returns first node with a key not less than the given one."""
        node, result = self.root, NIL
        while node is not NIL:
            if key < node.key:
                result, node = node, node.left
            elif node.key < key:
                node = node.right
            else:
                result = node
                break
        return result


class AbstractSet(ABC, _t.Generic[Value]):
    def __and__(self, other: AbstractSet[Value]) -> _te.Self:
        """Returns intersection of the set with given one."""
        return (self.from_iterable(value for value in self if value in other)
                if isinstance(other, AbstractSet)
                else NotImplemented)

    @abstractmethod
    def __contains__(self, value: Value) -> bool:
        """Checks if given value is presented in the set."""

    @_t.overload
    def __eq__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __eq__(self, other: _t.Any) -> _t.Any:
        ...

    def __eq__(self, other: _t.Any) -> _t.Any:
        """Checks if the set is equal to given one."""
        return (len(self) == len(other) and self <= other <= self
                if isinstance(other, AbstractSet)
                else NotImplemented)

    @_t.overload
    def __ge__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __ge__(self, other: _t.Any) -> _t.Any:
        ...

    def __ge__(self, other: _t.Any) -> _t.Any:
        """Checks if the set is a superset of given one."""
        return (len(self) >= len(other)
                and all(value in self for value in other)
                if isinstance(other, AbstractSet)
                else NotImplemented)

    @_t.overload
    def __gt__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __gt__(self, other: _t.Any) -> _t.Any:
        ...

    def __gt__(self, other: _t.Any) -> _t.Any:
        """Checks if the set is a strict superset of given one."""
        return (len(self) > len(other)
                and self >= other and self != other
                if isinstance(other, AbstractSet)
                else NotImplemented)

    @abstractmethod
    def __iter__(self) -> _t.Iterator[Value]:
        """Returns iterator over the set values."""

    @_t.overload
    def __le__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __le__(self, other: _t.Any) -> _t.Any:
        ...

    def __le__(self, other: _t.Any) -> _t.Any:
        """Checks if the set is a subset of given one."""
        return (len(self) <= len(other)
                and all(value in other for value in self)
                if isinstance(other, AbstractSet)
                else NotImplemented)

    @abstractmethod
    def __len__(self) -> int:
        """Returns size of the set."""

    @_t.overload
    def __lt__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __lt__(self, other: _t.Any) -> _t.Any:
        ...

    def __lt__(self, other: _t.Any) -> _t.Any:
        """Checks if the set is a strict subset of given one."""
        return (len(self) < len(other)
                and self <= other and self != other
                if isinstance(other, AbstractSet)
                else NotImplemented)

    def __or__(self, other: AbstractSet[Value]) -> _te.Self:
        """Returns union of the set with given one."""
        return (self.from_iterable(chain(self, other))
                if isinstance(other, AbstractSet)
                else NotImplemented)

    def __sub__(self, other: AbstractSet[Value]) -> _te.Self:
        """Returns subtraction of the set with given one."""
        return (self.from_iterable(value
                                   for value in self
                                   if value not in other)
                if isinstance(other, AbstractSet)
                else NotImplemented)

    def __xor__(self, other: AbstractSet[Value]) -> _te.Self:
        """Returns symmetric difference of the set with given one."""
        return ((self - other) | (other - self)
                if isinstance(other, AbstractSet)
                else NotImplemented)

    @abstractmethod
    def from_iterable(self, _value: _t.Iterable[Value]) -> _te.Self:
        """Constructs set from given values."""

    def isdisjoint(self, other: _te.Self) -> bool:
        """Checks if the tree has no intersection with given one."""
        return (all(value not in other for value in self)
                if len(self) < len(other)
                else all(value not in self for value in other))


class MutableSet(AbstractSet[Value]):
    def __iand__(self, other: AbstractSet[Value]) -> _te.Self:
        """Intersects the set with given one in-place."""
        if not isinstance(other, AbstractSet):
            return NotImplemented
        for value in self - other:
            self.discard(value)
        return self

    def __ior__(self, other: AbstractSet[Value]) -> _te.Self:
        """Unites the set with given one in-place."""
        if not isinstance(other, AbstractSet):
            return NotImplemented
        for value in other:
            self.add(value)
        return self

    def __isub__(self, other: AbstractSet[Value]) -> _te.Self:
        """Subtracts from the set a given one in-place."""
        if not isinstance(other, AbstractSet):
            return NotImplemented
        if self == other:
            self.clear()
        else:
            for value in other:
                self.discard(value)
        return self

    def __ixor__(self, other: AbstractSet[Value]) -> _te.Self:
        """Exclusively disjoins the set with given one in-place."""
        if not isinstance(other, AbstractSet):
            return NotImplemented
        if self == other:
            self.clear()
        else:
            for value in other:
                if value in self:
                    self.discard(value)
                else:
                    self.add(value)
        return self

    @abstractmethod
    def add(self, value: Value) -> None:
        """Adds given value to the set."""

    @abstractmethod
    def clear(self) -> None:
        """Adds given value to the set."""

    @abstractmethod
    def discard(self, value: Value) -> None:
        """Removes given value from the set if it is present."""

    @abstractmethod
    def remove(self, value: Value) -> None:
        """Removes given value that is present in the set."""
