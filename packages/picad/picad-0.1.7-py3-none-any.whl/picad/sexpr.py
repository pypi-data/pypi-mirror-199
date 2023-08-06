from typing import Any

from .base import SExprBase


class SExprEmpty(SExprBase):
    def __init__(self):
        super().__init__(None)


class SExpr(SExprBase):
    def __init__(self, data, required_tag=None,
                 required_atoms=None, optional_atoms=None,
                 required_lists=None, optional_lists=None):

        self._messages = []

        self._required_tag = required_tag
        self._required_atoms = required_atoms
        self._optional_atoms = optional_atoms
        self._required_lists = required_lists
        self._optional_lists = optional_lists

        if self._required_atoms is not None:
            if not isinstance(self._required_atoms, tuple):
                self._messages.append('required atoms must be tuple')
                raise RuntimeError()

            for required_type in self._required_atoms:
                if 'string' != required_type and 'number' != required_type:
                    self._messages.append(
                        f"invalid atom type '{required_type}'")
                    raise RuntimeError()

        if self._optional_atoms is not None:
            if not isinstance(self._optional_atoms, tuple):
                raise RuntimeError("optional atoms must be tuple")

            for type in self._optional_atoms:
                if 'string' != type and 'number' != type:
                    raise RuntimeError(f"invalid atom type '{type}'")

        if self._required_lists is not None:
            if not isinstance(self._required_lists, tuple):
                raise RuntimeError("required lists must be tuple")

            if 0 != len([x for x in self._required_lists if not isinstance(x, str)]):
                raise RuntimeError("required lists must contain strings")

        if self._optional_lists is not None:
            if not isinstance(self._optional_lists, tuple):
                raise RuntimeError("optional lists must be tuple")

            if 0 != len([x for x in self._optional_lists if not isinstance(x, str)]):
                raise RuntimeError("optional lists must contain strings")

        if data is None:
            raise RuntimeError("data must not be None")

        if not isinstance(data, list) and not isinstance(data, SExpr):
            self._error("data must be a list")
            raise RuntimeError(self._messages)

        super().__init__(data)

    def __getitem__(self, index) -> SExprBase:
        if self._data is None:
            return SExprEmpty()

        if isinstance(index, tuple):
            items = self.all(keys=index)
            if 0 == len(items):
                return SExprEmpty()

            if 1 != len(items):
                raise RuntimeError(
                    f"indexer can only be used on unique keys ('{index}' appears {len(items)} times)")

            return items[0]

        if isinstance(index, str):
            items = [x for x in self._lists if x[0] == index]
            if 0 == len(items):
                return SExprEmpty()

            if 1 != len(items):
                raise RuntimeError(
                    f"indexer can only be used on unique keys ('{index}' appears {len(items)} times)")

            return SExpr(items[0])

        if isinstance(index, int):
            if index >= len(self._atoms):
                return SExprEmpty()

            return self._atoms[index]

        raise RuntimeError(f"bad index type {type(index)}")

    def __setitem__(self, index, value) -> None:
        if self._data is None:
            return

        if isinstance(index, int):
            if isinstance(self._data[index], str):
                self._data[index] = value
                return

            if isinstance(self._data[index], float):
                self._data[index] = value
                return

            if isinstance(self._data[index], int):
                self._data[index] = value
                return

        raise RuntimeError(f"[{index}] has invalid atom type {type(index)}")

    def _allowed_list_tags(self) -> (str):
        allowed_tags = self._required_lists if self._required_lists is not None else ()
        allowed_tags = allowed_tags + \
            (self._optional_lists if self._optional_lists is not None else ())
        return allowed_tags

    def _keyed_list_tags(self) -> (str):
        keyed_tags = [x[:-2]
                      for x in self._allowed_list_tags() if x.endswith('[]')]
        return keyed_tags

    def _is_allowed_list_tag(self, tag: str) -> bool:
        allowed_tags = self._allowed_list_tags()

        if not tag in allowed_tags and not tag + '[]' in allowed_tags:
            return False

        return True

    def _validate(self) -> bool:
        self._messages = []

        result = self._validate_inner()

        # todo foss: logging
        # if not result:
        #     print(self._messages)

        return result

    def _validate_inner(self):

        if 0 == len(self._data):
            return self._error("data has zero length")

        if 0 == len(self._atoms):
            return self._error("atoms has zero lenhth")

        if not isinstance(self.tag, str):
            return self._error('tag is not a string')

        max_number_of_atoms = 0

        if self._required_atoms is not None:
            max_number_of_atoms += len(self._required_atoms)

            if len(self._atoms) < len(self._required_atoms):
                return self._error(f'not enough atoms')

            for i, required_type in enumerate(self._required_atoms):
                if 'number' == required_type:
                    if not isinstance(self._atoms[i], float) and not isinstance(self._atoms[i], int):
                        return self._error(f"atom {i} should be number")

                if 'string' == required_type:
                    if not isinstance(self._atoms[i], str):
                        return self._error(f"atom {i} should be string")

        if self._optional_atoms is not None:
            max_number_of_atoms += len(self._optional_atoms)
            first_index = 0 if self._required_atoms is None else len(
                self._required_atoms)

            if len(self._atoms) > first_index + len(self._optional_atoms):
                return self._error('too many atoms')

            for i, optional_type in enumerate(self._optional_atoms):
                index = first_index + i

                if index < len(self._atoms):
                    atom = self._atoms[index]

                    if 'number' == optional_type:
                        if not isinstance(atom, float) and not isinstance(atom, int):
                            return False

                    if 'string' == optional_type:
                        if not isinstance(atom, str):
                            self._error(
                                f"atom index {i} should be string (found '{atom}')")
                            return False

        if len(self._atoms) > max_number_of_atoms:
            self._error("too many atoms")
            return False

        list_tags = [x[0] for x in self._lists]

        if self._required_lists is not None:
            # todo foss: this test is no good given keyed lists
            if len(self._lists) < len(self._required_lists):
                self._error("not enough required lists")
                return False

        for tag in list_tags:
            if not self._is_allowed_list_tag(tag):
                self._error(f"invalid list tag '{tag}'")
                return False

            tag_count = list_tags.count(tag)
            if tag_count > 1 and not tag in self._keyed_list_tags():
                self._error(
                    f"too many instances of list tag '{tag}' ({tag_count})")
                return False

        if self._required_tag is not None:
            if self.tag != self._required_tag:
                self._error(
                    f"required tag '{self._required_tag}' missing (found '{self.tag}')")
                return False

        return True

    def _validate_or_raise(self, message=None):
        if not self._validate():
            raise RuntimeError(
                "validation failed" if message is None else message)

    def _error(self, message: str) -> bool:
        tag = self.tag if self.tag is not None else '[None]'
        message = f"ERROR: {tag}:{type(self)}:{message}"
        # print(message)  # todo foss: proper logging
        # print(self._data)f
        self._messages.append(message)
        return False

    def _get_keyed_list(self, tag: str, key: str) -> []:
        lists = self._find_lists((tag, key,))

        return lists[0]

    def all(self, keys: Any) -> (SExprBase):
        result = []

        if isinstance(keys, tuple):

            for l in self._lists:
                if len(l) >= len(keys):
                    matches = [keys[a] == l[a] for a in range(len(keys))]

                    if all(matches):
                        result.append(SExpr(l))

        elif isinstance(keys, str):

            for record in self._lists:
                if keys == record[0]:
                    result.append(SExpr(record))

        else:
            raise RuntimeError(f"bad keys type'{type(keys)}'")

        if result is None:
            result.append(SExprEmpty())

        return tuple(result)

    def first(self, keys: Any) -> SExprBase:
        a = self.all(keys)
        return a[0] if len(a) != 0 else SExprEmpty()

    def remove(self, index: Any) -> int:
        if isinstance(index, int):
            if index < len(self._atoms):
                self._remove_atom(self._atoms[index])
        elif isinstance(index, list) or isinstance(index, str):
            for record in self.all(index):
                self._data.remove(record._data)

    def add_list(self, ll: []):
        self._add_list(ll)
