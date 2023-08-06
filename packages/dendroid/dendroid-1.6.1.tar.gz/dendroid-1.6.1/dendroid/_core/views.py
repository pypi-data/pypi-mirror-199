from __future__ import annotations

import typing as _t
from collections import abc

from reprit.base import generate_repr

from .abcs import (NIL,
                   AbstractSet,
                   Node,
                   Tree)
from .hints import (Item,
                    Key,
                    Value)
from .utils import split_items


class BaseView(_t.Generic[Key, Value]):
    __slots__ = 'tree',

    def __init__(self, tree: Tree[Key, Value]) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __len__(self) -> int:
        return len(self.tree)


@abc.Set.register
class ItemsView(BaseView[Key, Value], AbstractSet[Item[Key, Value]]):
    def __contains__(self, item: Item[Key, Value]) -> bool:
        key, value = item
        node = self.tree.find(key)
        return node is not NIL and node.value == value

    def __iter__(self) -> _t.Iterator[Item[Key, Value]]:
        for node in self.tree:
            yield node.item

    def __reversed__(self) -> _t.Iterator[Item[Key, Value]]:
        for node in reversed(self.tree):
            yield node.item

    def from_iterable(
            self, _value: _t.Iterable[Item[Key, Value]]
    ) -> ItemsView[Key, Value]:
        keys, values = split_items(list(_value))
        return ItemsView(self.tree.from_components(keys, values))


@abc.Set.register
class KeysView(BaseView[Key, _t.Any], AbstractSet[Key]):
    def __contains__(self, key: Key) -> bool:
        return self.tree.find(key) is not NIL

    def __iter__(self) -> _t.Iterator[Key]:
        for node in self.tree:
            yield node.key

    def __reversed__(self) -> _t.Iterator[Key]:
        for node in reversed(self.tree):
            yield node.key

    def from_iterable(self, _value: _t.Iterable[Key]) -> KeysView[Key]:
        return KeysView(self.tree.from_components(_value))


class ValuesView(BaseView[Key, Value]):
    def __contains__(self, value: Value) -> bool:
        return any(candidate == value for candidate in self)

    def __iter__(self) -> _t.Iterator[Value]:
        for node in self.tree:
            yield node.value

    def __reversed__(self) -> _t.Iterator[Value]:
        for node in reversed(self.tree):
            yield node.value
