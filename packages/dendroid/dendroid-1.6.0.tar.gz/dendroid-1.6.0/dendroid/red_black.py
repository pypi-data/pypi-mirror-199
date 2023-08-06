from __future__ import annotations

import typing as _t
import weakref
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
                          to_balanced_tree_height as _to_balanced_tree_height,
                          to_unique_sorted_items as _to_unique_sorted_items,
                          to_unique_sorted_values as _to_unique_sorted_values)


class Node(_t.Generic[_Key, _Value]):
    _left: _t.Optional[_te.Self]
    _right: _t.Optional[_te.Self]
    _parent: _t.Optional['weakref.ref[_te.Self]']

    __slots__ = ('is_black', '_key', '_left', '_parent', '_right', '_value',
                 '__weakref__')

    def __init__(self,
                 key: _Key,
                 value: _Value,
                 is_black: bool,
                 left: _t.Union[_Nil, _te.Self] = NIL,
                 right: _t.Union[_Nil, _te.Self] = NIL,
                 parent: _t.Union[_Nil, _te.Self] = NIL) -> None:
        self._key, self._value, self.is_black = key, value, is_black
        self.left, self.right, self.parent = left, right, parent

    __repr__ = _recursive_repr()(_generate_repr(__init__))

    def __getstate__(self) -> _t.Tuple[_t.Any, ...]:
        return (self._key, self.value, self.is_black,
                self.parent, self.left, self.right)

    def __setstate__(self, state: _t.Tuple[_t.Any, ...]) -> None:
        (self._key, self._value, self.is_black,
         self.parent, self._left, self._right) = state

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


def _set_parent(node: _t.Union[_Nil, Node[_Key, _Value]],
                parent: _t.Optional[Node[_Key, _Value]]) -> None:
    if node is not NIL:
        node.parent = parent


def _set_black(maybe_node: _t.Optional[Node[_Key, _Value]]) -> None:
    if maybe_node is not None:
        maybe_node.is_black = True


def _is_left_child(node: Node[_Key, _Value]) -> bool:
    parent = node.parent
    return parent is not None and parent.left is node


def _is_node_black(node: _t.Union[_Nil, Node[_Key, _Value]]) -> bool:
    return node is NIL or node.is_black


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
                    depth: int,
                    height: int = _to_balanced_tree_height(len(keys)),
                    constructor: _t.Callable[..., Node[_Key, _Key]]
                    = Node.from_simple
            ) -> Node[_Key, _Key]:
                middle_index = (start_index + end_index) // 2
                return constructor(
                        keys[middle_index],
                        depth != height,
                        (to_simple_node(start_index, middle_index, depth + 1)
                         if middle_index > start_index
                         else NIL),
                        (to_simple_node(middle_index + 1, end_index, depth + 1)
                         if middle_index < end_index - 1
                         else NIL)
                )

            simple_root = to_simple_node(0, len(keys), 0)
            simple_root.is_black = True
            return _t.cast(_t.Type[Tree[_Key, _Key]], cls)(simple_root)
        else:
            items = _to_unique_sorted_items(keys, tuple(_values))

            def to_complex_node(
                    start_index: int,
                    end_index: int,
                    depth: int,
                    height: int = _to_balanced_tree_height(len(items)),
                    constructor: _t.Callable[..., Node[_Key, _Value]] = Node
            ) -> Node[_Key, _Value]:
                middle_index = (start_index + end_index) // 2
                return constructor(
                        *items[middle_index],
                        depth != height,
                        (to_complex_node(start_index, middle_index, depth + 1)
                         if middle_index > start_index
                         else NIL),
                        (to_complex_node(middle_index + 1, end_index,
                                         depth + 1)
                         if middle_index < end_index - 1
                         else NIL)
                )

            complex_root = to_complex_node(0, len(items), 0)
            complex_root.is_black = True
            return _t.cast(_t.Type[Tree[_Key, _Value]], cls)(complex_root)

    def insert(self, key: _Key, value: _Value) -> Node[_Key, _Value]:
        parent = self.root
        if parent is NIL:
            node = self.root = Node(key, value, True)
            return node
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = Node(key, value, False)
                    parent.left = node
                    break
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = Node(key, value, False)
                    parent.right = node
                    break
                else:
                    parent = parent.right
            else:
                return parent
        self._restore(node)
        return node

    def remove(self, node: _Node[_Key, _Value]) -> None:
        assert isinstance(node, Node)
        successor, is_node_black = node, node.is_black
        if successor.left is NIL:
            (successor_child, successor_child_parent,
             is_successor_child_left) = (successor.right, successor.parent,
                                         _is_left_child(successor))
            self._transplant(successor, successor_child)
        elif successor.right is NIL:
            (successor_child, successor_child_parent,
             is_successor_child_left) = (successor.left, successor.parent,
                                         _is_left_child(successor))
            self._transplant(successor, successor_child)
        else:
            assert node.right is not NIL
            successor = node.right
            while successor.left is not NIL:
                successor = successor.left
            is_node_black = successor.is_black
            successor_child, is_successor_child_left = successor.right, False
            if successor.parent is node:
                successor_child_parent = successor
            else:
                is_successor_child_left = _is_left_child(successor)
                successor_child_parent = successor.parent
                self._transplant(successor, successor.right)
                successor.right = node.right
            self._transplant(node, successor)
            assert node.left is not NIL
            node.left.parent = successor
            successor.left, successor.is_black = node.left, node.is_black
        if is_node_black:
            self._remove_node_fixup(successor_child, successor_child_parent,
                                    is_successor_child_left)

    def _restore(self, node: Node[_Key, _Value]) -> None:
        while not _is_node_black(node.parent):
            parent = node.parent
            assert parent is not NIL
            grandparent = parent.parent
            assert grandparent is not NIL
            if parent is grandparent.left:
                assert grandparent is not NIL
                uncle = grandparent.right
                if _is_node_black(uncle):
                    if node is parent.right:
                        self._rotate_left(parent)
                        node, parent = parent, node
                    parent.is_black, grandparent.is_black = True, False
                    assert grandparent is not NIL
                    self._rotate_right(grandparent)
                else:
                    assert uncle is not NIL
                    parent.is_black = uncle.is_black = True
                    grandparent.is_black = False
                    node = grandparent
            else:
                uncle = grandparent.left
                if _is_node_black(uncle):
                    if node is parent.left:
                        self._rotate_right(parent)
                        node, parent = parent, node
                    parent.is_black, grandparent.is_black = True, False
                    assert grandparent is not NIL
                    self._rotate_left(grandparent)
                else:
                    assert uncle is not NIL
                    parent.is_black = uncle.is_black = True
                    grandparent.is_black = False
                    node = grandparent
        assert self.root is not NIL
        self.root.is_black = True

    def _remove_node_fixup(self,
                           node: _t.Union[_Nil, Node[_Key, _Value]],
                           parent: _t.Union[_Nil, Node[_Key, _Value]],
                           is_left_child: bool) -> None:
        while node is not self.root and _is_node_black(node):
            assert parent is not NIL
            if is_left_child:
                sibling = parent.right
                assert sibling is not NIL
                if not _is_node_black(sibling):
                    sibling.is_black, parent.is_black = True, False
                    self._rotate_left(parent)
                    sibling = parent.right
                assert sibling is not NIL
                if (_is_node_black(sibling.left)
                        and _is_node_black(sibling.right)):
                    sibling.is_black = False
                    assert parent is not NIL
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.right):
                        assert sibling is not NIL
                        assert sibling.left is not NIL
                        sibling.left.is_black, sibling.is_black = True, False
                        self._rotate_right(sibling)
                        sibling = parent.right
                    assert sibling is not NIL
                    sibling.is_black, parent.is_black = parent.is_black, True
                    _set_black(sibling.right)
                    self._rotate_left(parent)
                    node = self.root
            else:
                sibling = parent.left
                if not _is_node_black(sibling):
                    assert sibling is not NIL
                    sibling.is_black, parent.is_black = True, False
                    self._rotate_right(parent)
                    sibling = parent.left
                assert sibling is not NIL
                if (_is_node_black(sibling.left)
                        and _is_node_black(sibling.right)):
                    assert sibling is not NIL
                    sibling.is_black = False
                    assert parent is not NIL
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.left):
                        assert sibling.right is not NIL
                        sibling.right.is_black, sibling.is_black = True, False
                        self._rotate_left(sibling)
                        sibling = parent.left
                    assert sibling is not NIL
                    sibling.is_black, parent.is_black = parent.is_black, True
                    _set_black(sibling.left)
                    self._rotate_right(parent)
                    node = self.root
        _set_black(node)

    def _rotate_left(self, node: Node[_Key, _Value]) -> None:
        replacement = node.right
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.right, replacement.left = replacement.left, node

    def _rotate_right(self, node: Node[_Key, _Value]) -> None:
        replacement = node.left
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.left, replacement.right = replacement.right, node

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
