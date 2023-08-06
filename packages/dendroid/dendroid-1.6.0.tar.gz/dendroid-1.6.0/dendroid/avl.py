from __future__ import annotations

import typing as _t
from reprlib import recursive_repr as _recursive_repr

import typing_extensions as _te
from reprit.base import generate_repr as _generate_repr

from ._core.abcs import (NIL,
                         Nil as _Nil,
                         Node as _Node,
                         Tree as _Tree)
from ._core.hints import (Item as _Item,
                          Key as _Key,
                          Order as _Order,
                          Value as _Value)
from ._core.maps import Map as _Map
from ._core.sets import (KeyedSet as _KeyedSet,
                         Set as _Set)
from ._core.utils import (dereference_maybe as _dereference_maybe,
                          maybe_weakref as _maybe_weakref,
                          split_items as _split_items,
                          to_unique_sorted_items as _to_unique_sorted_items,
                          to_unique_sorted_values as _to_unique_sorted_values)


class Node(_t.Generic[_Key, _Value]):
    __slots__ = ('height', '_key', '_left', '_parent', '_right', '_value',
                 '__weakref__')

    def __init__(self,
                 key: _Key,
                 value: _Value,
                 left: _t.Union[_Nil, _te.Self] = NIL,
                 right: _t.Union[_Nil, _te.Self] = NIL,
                 parent: _t.Union[_Nil, _te.Self] = NIL) -> None:
        self._key, self._value = key, value
        self.left, self.right, self.parent = left, right, parent
        self.height = max(_to_height(self.left), _to_height(self.right)) + 1

    __repr__ = _recursive_repr()(_generate_repr(__init__))

    def __getstate__(self) -> _t.Tuple[
        _Key, _Value, int, _t.Union[_Nil, _te.Self],
        _t.Union[_Nil, _te.Self], _t.Union[_Nil, _te.Self]
    ]:
        return (self._key, self._value, self.height,
                self.parent, self.left, self.right)

    def __setstate__(
            self,
            state: _t.Tuple[
                _Key, _Value, int, _t.Union[_Nil, _te.Self],
                _t.Union[_Nil, _te.Self], _t.Union[_Nil, _te.Self]
            ]
    ) -> None:
        (self._key, self._value, self.height,
         self.parent, self._left, self._right) = state

    @classmethod
    def from_simple(cls: _t.Type[Node[_Key, _Key]],
                    key: _Key,
                    *args: _t.Any) -> Node[_Key, _Key]:
        return cls(key, key, *args)

    @property
    def balance_factor(self) -> int:
        return _to_height(self.left) - _to_height(self.right)

    @property
    def item(self) -> _Item[_Key, _Value]:
        return self.key, self.value

    @property
    def key(self) -> _Key:
        return self._key

    @property
    def left(self) -> _t.Union[_Nil, _te.Self]:
        return self._left

    @left.setter
    def left(self, node: _t.Union[_Nil, _te.Self]) -> None:
        self._left = node
        _set_parent(node, self)

    @property
    def parent(self) -> _t.Union[_Nil, _te.Self]:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, node: _t.Union[_Nil, _te.Self]) -> None:
        self._parent = _maybe_weakref(node)

    @property
    def right(self) -> _t.Union[_Nil, _te.Self]:
        return self._right

    @right.setter
    def right(self, node: _t.Union[_Nil, _te.Self]) -> None:
        self._right = node
        _set_parent(node, self)

    @property
    def value(self) -> _Value:
        return self._value

    @value.setter
    def value(self, value: _Value) -> None:
        self._value = value


def _to_height(node: _t.Union[_Nil, Node[_Key, _Value]]) -> int:
    return -1 if node is NIL else node.height


def _update_height(node: Node[_Key, _Value]) -> None:
    node.height = max(_to_height(node.left), _to_height(node.right)) + 1


def _set_parent(node: _t.Union[_Nil, Node[_Key, _Value]],
                parent: _t.Optional[Node[_Key, _Value]]) -> None:
    if node is not NIL:
        node.parent = parent


class Tree(_Tree[_Key, _Value]):
    root: _t.Optional[Node[_Key, _Value]]

    @staticmethod
    def predecessor(
            node: _Node[_Key, _Value]
    ) -> _t.Union[_Nil, Node[_Key, _Value]]:
        assert isinstance(node, Node)
        if node.left is NIL:
            result = node.parent
            while result is not None and node is result.left:
                node, result = result, result.parent
        else:
            result = node.left
            while result.right is not NIL:
                result = result.right
        return result

    @staticmethod
    def successor(
            node: _Node[_Key, _Value]
    ) -> _t.Union[_Nil, Node[_Key, _Value]]:
        assert isinstance(node, Node)
        if node.right is NIL:
            result = node.parent
            while result is not None and node is result.right:
                node, result = result, result.parent
        else:
            result = node.right
            while result.left is not NIL:
                result = result.left
        return result

    @_t.overload
    @classmethod
    def from_components(cls,
                        _keys: _t.Iterable[_Key],
                        _values: None = ...) -> Tree[_Key, _Key]:
        ...

    @_t.overload
    @classmethod
    def from_components(cls,
                        _keys: _t.Iterable[_Key],
                        _values: _t.Iterable[_Value]) -> Tree[_Key, _Value]:
        ...

    @classmethod
    def from_components(
            cls: _t.Union[
                _t.Type[Tree[_Key, _Key]], _t.Type[Tree[_Key, _Value]]
            ],
            _keys: _t.Iterable[_Key],
            _values: _t.Optional[_t.Iterable[_Value]] = None
    ) -> _t.Union[Tree[_Key, _Key], Tree[_Key, _Value]]:
        keys = list(_keys)
        if not keys:
            return cls(NIL)
        elif _values is None:
            keys = _to_unique_sorted_values(keys)

            def to_simple_node(
                    start_index: int,
                    end_index: int,
                    constructor: _t.Callable[..., Node[_Key, _Key]]
                    = Node.from_simple
            ) -> Node[_Key, _Key]:
                middle_index = (start_index + end_index) // 2
                return constructor(keys[middle_index],
                                   (to_simple_node(start_index, middle_index)
                                    if middle_index > start_index
                                    else NIL),
                                   (to_simple_node(middle_index + 1, end_index)
                                    if middle_index < end_index - 1
                                    else NIL))

            return _t.cast(_t.Type[Tree[_Key, _Key]], cls)(
                    to_simple_node(0, len(keys))
            )
        else:
            items = _to_unique_sorted_items(keys, list(_values))

            def to_complex_node(
                    start_index: int,
                    end_index: int,
                    constructor: _t.Callable[..., Node[_Key, _Value]]
                    = Node[_Key, _Value]
            ) -> Node[_Key, _Value]:
                middle_index = (start_index + end_index) // 2
                return constructor(*items[middle_index],
                                   (to_complex_node(start_index, middle_index)
                                    if middle_index > start_index
                                    else NIL),
                                   (to_complex_node(middle_index + 1,
                                                    end_index)
                                    if middle_index < end_index - 1
                                    else NIL))

            return _t.cast(_t.Type[Tree[_Key, _Value]], cls)(
                    to_complex_node(0, len(items))
            )

    def insert(self, key: _Key, value: _Value) -> Node[_Key, _Value]:
        parent = self.root
        if parent is NIL:
            node = self.root = Node(key, value)
            return node
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = Node(key, value)
                    parent.left = node
                    break
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = Node(key, value)
                    parent.right = node
                    break
                else:
                    parent = parent.right
            else:
                return parent
        self._rebalance(node.parent)
        return node

    def remove(self, node: _Node[_Key, _Value]) -> None:
        assert isinstance(node, Node)
        if node.left is NIL:
            imbalanced_node = node.parent
            self._transplant(node, node.right)
        elif node.right is NIL:
            imbalanced_node = node.parent
            self._transplant(node, node.left)
        else:
            successor = node.right
            while successor.left is not NIL:
                successor = successor.left
            if successor.parent is node:
                imbalanced_node = successor
            else:
                imbalanced_node = successor.parent
                self._transplant(successor, successor.right)
                successor.right = node.right
            self._transplant(node, successor)
            successor.left, successor.left.parent = node.left, successor
        self._rebalance(imbalanced_node)

    def _rebalance(self, node: _t.Union[_Nil, Node[_Key, _Value]]) -> None:
        while node is not None:
            _update_height(node)
            if node.balance_factor > 1:
                assert node.left is not NIL
                if node.left.balance_factor < 0:
                    self._rotate_left(node.left)
                self._rotate_right(node)
            elif node.balance_factor < -1:
                assert node.right is not NIL
                if node.right.balance_factor > 0:
                    self._rotate_right(node.right)
                self._rotate_left(node)
            node = node.parent

    def _rotate_left(self, node: Node[_Key, _Value]) -> None:
        replacement = node.right
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.right, replacement.left = replacement.left, node
        _update_height(node)
        _update_height(replacement)

    def _rotate_right(self, node: Node[_Key, _Value]) -> None:
        replacement = node.left
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.left, replacement.right = replacement.right, node
        _update_height(node)
        _update_height(replacement)

    def _transplant(self,
                    origin: Node[_Key, _Value],
                    replacement: _t.Union[_Nil, Node[_Key, _Value]]) -> None:
        parent = origin.parent
        if parent is None:
            self.root = replacement
            _set_parent(replacement, None)
        elif origin is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement

    __slots__ = 'root',

    def __init__(self, root: _t.Union[_Nil, Node[_Key, _Value]]) -> None:
        self.root = root


def map_(*items: _Item[_Key, _Value]) -> _Map[_Key, _Value]:
    return _Map(Tree.from_components(*_split_items(items)))


@_t.overload
def set_(*values: _Value,
         key: None = ...) -> _Set[_Value]:
    ...


@_t.overload
def set_(*values: _Value,
         key: _Order[_Value, _Key]) -> _KeyedSet[_Key, _Value]:
    ...


def set_(
        *values: _Value,
        key: _t.Optional[_Order[_Value, _Key]] = None
) -> _t.Union[_KeyedSet[_Key, _Value], _Set[_Value]]:
    return (_Set(Tree.from_components(values))
            if key is None
            else _KeyedSet(Tree.from_components([key(value)
                                                 for value in values],
                                                values),
                           key))
