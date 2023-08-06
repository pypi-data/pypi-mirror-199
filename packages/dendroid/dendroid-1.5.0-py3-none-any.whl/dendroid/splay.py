from __future__ import annotations

import typing as _t

import typing_extensions as _te

from .binary import Node
from .core.abcs import (NIL,
                        Nil as _Nil,
                        Node as _Node,
                        Tree as _Tree)
from .core.hints import (Item as _Item,
                         Key as _Key,
                         Order as _Order,
                         Value as _Value)
from .core.maps import Map as _Map
from .core.sets import (KeyedSet as _KeyedSet,
                        Set as _Set)
from .core.utils import (split_items as _split_items,
                         to_unique_sorted_items as _to_unique_sorted_items,
                         to_unique_sorted_values as _to_unique_sorted_values)


class Tree(_Tree[_Key, _Value]):
    _header: Node[_Key, _Value]
    root: _t.Optional[Node[_Key, _Value]]

    __slots__ = '_header', 'root'

    def __init__(self,
                 root: _t.Union[_Nil, Node[_Key, _Value]]) -> None:
        self.root = root
        self._header = Node(NotImplemented, NotImplemented)

    def __iter__(self) -> _t.Iterator[Node[_Key, _Value]]:
        # we are collecting all values at once
        # because tree can be implicitly changed during iteration
        # (e.g. by simple lookup)
        # and cause infinite loops
        return _t.cast(_t.Iterator[Node[_Key, _Value]],
                       iter(list(super().__iter__())))

    def __reversed__(self) -> _t.Iterator[Node[_Key, _Value]]:
        # we are collecting all values at once
        # because tree can be implicitly changed during iteration
        # (e.g. by simple lookup)
        # and cause infinite loops
        return _t.cast(_t.Iterator[Node[_Key, _Value]],
                       iter(list(super().__reversed__())))

    @_t.overload
    @classmethod
    def from_components(cls: _t.Type[Tree[_Key, _Key]],
                        _keys: _t.Iterable[_Key],
                        _values: None = ...) -> Tree[_Key, _Key]:
        ...

    @_t.overload
    @classmethod
    def from_components(cls,
                        _keys: _t.Iterable[_Key],
                        _values: _t.Iterable[_Value]) -> _te.Self:
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
            items = _to_unique_sorted_items(keys, tuple(_values))

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

    def find(self, key: _Key) -> _t.Union[_Nil, Node[_Key, _Value]]:
        if self.root is NIL:
            return NIL
        self._splay(key)
        root = self.root
        return NIL if key < root.key or root.key < key else root

    def insert(self, key: _Key, value: _Value) -> _Node[_Key, _Value]:
        if self.root is NIL:
            node = self.root = Node(key, value)
            return node
        self._splay(key)
        if key < self.root.key:
            self.root.left, self.root = NIL, Node(key, value,
                                                          self.root.left,
                                                          self.root)
        elif self.root.key < key:
            self.root.right, self.root = NIL, Node(key, value,
                                                           self.root,
                                                           self.root.right)
        return self.root

    def max(self) -> _t.Union[_Nil, _Node[_Key, _Value]]:
        node = self.root
        if node is not NIL:
            while node.right is not NIL:
                node = node.right
                assert node is not NIL
            self._splay(node.key)
        return node

    def min(self) -> _t.Union[_Nil, _Node[_Key, _Value]]:
        node = self.root
        if node is not NIL:
            while node.left is not NIL:
                node = node.left
                assert node is not NIL
            self._splay(node.key)
        return node

    def popmax(self) -> _t.Union[_Nil, _Node[_Key, _Value]]:
        if self.root is NIL:
            return self.root
        result = self.max()
        self._remove_root()
        return result

    def popmin(self) -> _t.Union[_Nil, _Node[_Key, _Value]]:
        if self.root is NIL:
            return self.root
        result = self.min()
        self._remove_root()
        return result

    def predecessor(
            self, node: _Node[_Key, _Value]
    ) -> _t.Union[_Nil, Node[_Key, _Value]]:
        assert isinstance(node, Node)
        if node.left is NIL:
            result, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                assert cursor is not NIL
                if cursor.key < key:
                    result, cursor = cursor, cursor.right
                else:
                    cursor = cursor.left
        else:
            result = node.left
            assert result is not NIL
            while result.right is not NIL:
                result = result.right
                assert result is not NIL
        if result is not NIL:
            self._splay(result.key)
        return result

    def remove(self, node: _Node[_Key, _Value]) -> None:
        self._splay(node.key)
        self._remove_root()

    def successor(
            self, node: _Node[_Key, _Value]
    ) -> _t.Union[_Nil, Node[_Key, _Value]]:
        assert isinstance(node, Node)
        if node.right is NIL:
            result, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                assert cursor is not NIL
                if key < cursor.key:
                    result, cursor = cursor, cursor.left
                else:
                    cursor = cursor.right
        else:
            result = node.right
            assert result is not NIL
            while result.left is not NIL:
                result = result.left
                assert result is not NIL
        if result is not NIL:
            self._splay(result.key)
        return result

    def _splay(self, key: _Key) -> None:
        next_root = self.root
        next_root_left_child = next_root_right_child = self._header
        while True:
            assert next_root is not NIL
            if key < next_root.key:
                if next_root.left is NIL:
                    break
                elif key < next_root.left.key:
                    next_root = self._rotate_right(next_root)
                    if next_root.left is NIL:
                        break
                next_root_right_child.left = next_root
                next_root_right_child, next_root = next_root, next_root.left
            elif next_root.key < key:
                if next_root.right is NIL:
                    break
                elif next_root.right.key < key:
                    next_root = self._rotate_left(next_root)
                    if next_root.right is NIL:
                        break
                next_root_left_child.right = next_root
                next_root_left_child, next_root = next_root, next_root.right
            else:
                break
        assert next_root is not NIL
        next_root_left_child.right, next_root_right_child.left = (
            next_root.left, next_root.right
        )
        next_root.left, next_root.right = self._header.right, self._header.left
        self.root = next_root

    def _remove_root(self) -> None:
        root = self.root
        assert root is not NIL
        if root.left is NIL:
            self.root = root.right
        else:
            right_root_child = root.right
            self.root = root.left
            self._splay(root.key)
            assert self.root is not NIL
            self.root.right = right_root_child

    @staticmethod
    def _rotate_left(
            node: Node[_Key, _Value]
    ) -> Node[_Key, _Value]:
        replacement = node.right
        assert replacement is not NIL
        node.right, replacement.left = replacement.left, node
        return replacement

    @staticmethod
    def _rotate_right(
            node: Node[_Key, _Value]
    ) -> Node[_Key, _Value]:
        replacement = node.left
        assert replacement is not NIL
        node.left, replacement.right = replacement.right, node
        return replacement


def map_(*items: _Item[_Key, _Value]) -> _Map[_Key, _Value]:
    return _Map(Tree.from_components(*_split_items(items)))


def set_(
        *values: _Value,
        key: _t.Optional[_Order[_Value, _Key]] = None
) -> _t.Union[_KeyedSet[_Value], _Set[_Value]]:
    return (_Set(Tree.from_components(values))
            if key is None
            else _KeyedSet(Tree.from_components([key(value)
                                                 for value in values],
                                                values),
                           key))
