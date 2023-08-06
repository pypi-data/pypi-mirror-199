from .kicad import parse_sexpr, build_sexpr
import typing
from typing import Any


class SExprBase():
    _allow_instantiate_base = False

    allow_empty = True

    def __new__(cls, *args, **kwargs):
        if cls is SExprBase and not SExprBase._allow_instantiate_base:
            raise RuntimeError("please do not instantiate base class")

        return object.__new__(cls)

    def __init__(self, data: []):
        self._messages = []  # todo foss: implement this

        if data is None:
            if not SExprBase.allow_empty:
                raise RuntimeError("created empty instance")

            self._data = None
        elif isinstance(data, list):
            self._data = data
        elif isinstance(data, SExprBase):
            self._data = data._data
        else:
            raise RuntimeError(f"invalid data type '{type(data)}'")

    def __repr__(self) -> str:
        return f"<sexpr>{build_sexpr(self._data)}</sexpr>"

    @property
    def is_empty(self) -> bool:
        return self._data is None

    @property
    def tag(self) -> str:
        if self.is_empty:
            return "<EMPTY>"  # todo foss: what to do in these cases?

        if len(self._atoms) == 0:
            return "<NOTAG>"

        name = self._atoms[0]

        if not isinstance(name, str):
            return None

        return name

    @property
    def _atoms(self) -> (Any):
        if self.is_empty:
            return ()

        l = [x for x in self._data if isinstance(
            x, str) or isinstance(x, float) or isinstance(x, int)]
        return tuple(l)

    @property
    def _lists(self) -> ([Any]):
        if self.is_empty:
            return ()

        l = [x for x in self._data if isinstance(x, list)]
        return tuple(l)

    @property
    def _atom_indicies(self) -> (int):
        ii = ()

        for i, e in enumerate(self._data):
            if not isinstance(e, list):
                ii = ii + (i,)

        return ii

    @staticmethod
    def _is_atom_type(atom):
        if isinstance(atom, str):
            return True

        if isinstance(atom, int):
            return True

        if isinstance(atom, float):
            return True

    def _add_atom(self, atom: Any):

        if not SExprBase._is_atom_type(atom):
            raise RuntimeError(f"invalid atom type '{type(atom)}'")

        self._data.append(atom)

    def _set_atom(self, index, atom):
        if not isinstance(index, int):
            raise RuntimeError("non-integer index")

        if index >= len(self._atoms):
            raise RuntimeError("atom index out of range")

        if not SExprBase._is_atom_type(atom):
            raise RuntimeError(f"invalid atom type '{type(atom)}'")

        index = self._atom_indicies[index]

        self._data[index] = atom

    def _remove_atom(self, atom: Any):
        if atom in self._data:
            self._data.remove(atom)

    def _add_list(self, ll: []):
        if not isinstance(ll, list):
            raise RuntimeError(f"invalid list type '{type(ll)}'")

        if len(ll) < 2:
            raise RuntimeError(f"invalid list length '{len(ll)}'")

        if ll[0] is None:
            raise RuntimeError(f"list name is None")

        if not isinstance(ll[0], str):
            raise RuntimeError(
                f"list name is must be string (is {type(ll[0])}")

        if len(ll[0]) == 0:
            raise RuntimeError(f"list name is zero-length string")

        self._data.append(ll)

    def _remove_list(self, ll: []):
        if not ll in self._lists:
            raise RuntimeError(f"list {ll} is not in lists")

        self._data.remove(ll)

    def _find_lists(self, keys: Any) -> ():

        if isinstance(keys, tuple):
            result = []

            for l in self._lists:
                if len(l) >= len(keys):
                    matches = [keys[a] == l[a] for a in range(len(keys))]

                    if all(matches):
                        result.append(l)
            return tuple(result)

        elif isinstance(keys, str):
            return tuple([x for x in self._lists if keys == x[0]])

        raise RuntimeError(f"invalid key(s) type '{type(keys)}'")
