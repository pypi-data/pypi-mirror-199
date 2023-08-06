from __future__ import annotations

import typing as _t

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
from ._core.utils import (are_keys_equal as _are_keys_equal,
                          split_items as _split_items,
                          to_unique_sorted_items as _to_unique_sorted_items,
                          to_unique_sorted_values as _to_unique_sorted_values)


class Node(_t.Generic[_Key, _Value]):
    _left: _t.Union[_Nil, _te.Self]
    _right: _t.Union[_Nil, _te.Self]

    __slots__ = '_left', '_right', '_key', '_value'

    def __init__(self,
                 key: _Key,
                 value: _Value,
                 left: _t.Union[_Nil, _te.Self] = NIL,
                 right: _t.Union[_Nil, _te.Self] = NIL) -> None:
        self._key, self._value, self._left, self._right = (key, value, left,
                                                           right)

    __repr__ = _generate_repr(__init__)

    @classmethod
    def from_simple(cls: _t.Type[Node[_Key, _Key]],
                    key: _Key,
                    *args: _t.Any) -> Node[_Key, _Key]:
        return cls(key, key, *args)

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
    def left(self, value: _t.Union[_Nil, _te.Self]) -> None:
        self._left = value

    @property
    def right(self) -> _t.Union[_Nil, _te.Self]:
        return self._right

    @right.setter
    def right(self, value: _t.Union[_Nil, _te.Self]) -> None:
        self._right = value

    @property
    def value(self) -> _Value:
        return self._value

    @value.setter
    def value(self, value: _Value) -> None:
        self._value = value


class Tree(_Tree[_Key, _Value]):
    root: _t.Optional[Node[_Key, _Value]]

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
                    constructor: _t.Callable[..., Node[_Key, _Value]] = Node
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
                    node = parent.left = Node(key, value)
                    return node
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = parent.right = Node(key, value)
                    return node
                else:
                    parent = parent.right
            else:
                return parent

    def popmax(self) -> _t.Union[_Nil, Node[_Key, _Value]]:
        node = self.root
        if node is NIL:
            return node
        elif node.right is NIL:
            self.root = node.left
            return node
        else:
            while node.right.right is not NIL:
                node = node.right
            assert node.right is not NIL
            result, node.right = node.right, node.right.left
            return result

    def popmin(self) -> _t.Union[_Nil, Node[_Key, _Value]]:
        node = self.root
        if node is NIL:
            return node
        elif node.left is NIL:
            self.root = node.right
            return node
        else:
            while node.left.left is not NIL:
                node = node.left
            assert node.left is not NIL
            result, node.left = node.left, node.left.right
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
            while result.right is not NIL:
                result = result.right
        return result

    def remove(self, node: _Node[_Key, _Value]) -> None:
        assert isinstance(node, Node)
        assert self.root is not NIL
        parent, key = self.root, node.key
        if _are_keys_equal(key, parent.key):
            if parent.left is NIL:
                self.root = parent.right
            else:
                node = parent.left
                if node.right is NIL:
                    self.root, node.right = node, self.root.right
                else:
                    while node.right.right is not NIL:
                        node = node.right
                    assert node.right is not NIL
                    (
                        self.root, node.right.left, node.right.right,
                        node.right
                    ) = (node.right, self.root.left, self.root.right,
                         node.right.left)
            return
        while True:
            assert parent is not NIL
            if key < parent.key:
                # search in left subtree
                assert parent.left is not NIL
                if _are_keys_equal(key, parent.left.key):
                    # remove `parent.left`
                    cursor = parent.left.left
                    if cursor is NIL:
                        parent.left = parent.left.right
                        return
                    elif cursor.right is NIL:
                        parent.left, cursor.right = cursor, parent.left.right
                    else:
                        while cursor.right.right is not NIL:
                            cursor = cursor.right
                        assert cursor.right is not NIL
                        (
                            parent.left, cursor.right.left, cursor.right.right,
                            cursor.right
                        ) = (cursor.right, parent.left.left, parent.left.right,
                             cursor.right.left)
                    return
                else:
                    parent = parent.left
            # search in right subtree
            else:
                assert parent.right is not NIL
                if _are_keys_equal(key, parent.right.key):
                    # remove `parent.right`
                    assert parent.right is not NIL
                    cursor = parent.right.left
                    if cursor is NIL:
                        parent.right = parent.right.right
                        return
                    elif cursor.right is NIL:
                        parent.right, cursor.right = cursor, parent.right.right
                    else:
                        while cursor.right.right is not NIL:
                            cursor = cursor.right
                        assert cursor.right is not NIL
                        (
                            parent.right, cursor.right.left,
                            cursor.right.right, cursor.right
                        ) = (
                            cursor.right, parent.right.left,
                            parent.right.right, cursor.right.left
                        )
                    return
                else:
                    parent = parent.right

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
        return result

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
