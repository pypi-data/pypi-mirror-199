import typing as _t

import typing_extensions as _te

_T = _t.TypeVar('_T',
                contravariant=True)


class Ordered(_te.Protocol):
    def __lt__(self, other: _te.Self) -> bool:
        ...


Key = _t.TypeVar('Key',
                 bound=Ordered)
Key_co = _t.TypeVar('Key_co',
                    bound=Ordered,
                    covariant=True)
Value = _t.TypeVar('Value',
                   bound=_t.Any)
Order = _t.Callable[[Value], Key]
Item = _t.Tuple[Key, Value]
