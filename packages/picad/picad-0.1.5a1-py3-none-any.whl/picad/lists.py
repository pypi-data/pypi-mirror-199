import math

from .sexpr import SExpr


class ListAt(SExpr):  # (at 168.91 100.33 0)
    def __init__(self, data):
        super().__init__(data, required_tag='at', required_atoms=(
            'string', 'number', 'number',), optional_atoms=('number',))
        self._validate_or_raise("invalid initial data")

    @property
    def x(self) -> str:
        return self._atoms[1]

    @x.setter
    def x(self, v: float):
        self._set_atom(1, v)
        self._validate_or_raise()

    @property
    def y(self) -> str:
        return self[2]

    @y.setter
    def y(self, v: float):
        self._set_atom(2, v)
        self._validate_or_raise()

    @property
    def angle(self) -> str:
        return self[3]

    @angle.setter
    def angle(self, v: float):
        self._set_atom(3, v)
        self._validate_or_raise()

    def distance_from(self, other) -> float:
        x = other.x - self.x
        y = other.y - self.y
        return math.sqrt(x * x + y * y)


class ListId(SExpr):  # (id 0)
    def __init__(self, data):
        super().__init__(data, required_tag='id', required_atoms=('string', 'number',))
        self._validate_or_raise("invalid initial data")

    @property
    def id(self) -> int:
        return self._atoms[1]

    @id.setter
    def id(self, v: int):
        self._set_atom(1, v)
        self._validate_or_raise()


class ListUuid(SExpr):  # (uuid 18af9582-7c92-46f1-9603-90a0db4828ae)
    def __init__(self, data):
        super().__init__(data, required_tag='uuid', required_atoms=('string', 'string',))
        self._validate_or_raise("invalid initial data")

    @property
    def uuid(self) -> int:
        return self._atoms[1]

    @uuid.setter
    def uuid(self, v: int):
        self._set_atom(1, v)
        self._validate_or_raise()


class ListLibId(SExpr):  # (lib_id "power:GND")
    def __init__(self, data):
        super().__init__(data, required_tag='lib_id', required_atoms=('string', 'string',))
        self._validate_or_raise("invalid initial data")

    @property
    def lib_id(self) -> int:
        return self._atoms[1]

    @lib_id.setter
    def lib_id(self, v: int):
        self._set_atom(1, v)
        self._validate_or_raise()


class ListUnit(SExpr):  # (unit 1)
    def __init__(self, data):
        super().__init__(data, required_tag='unit', required_atoms=('string', 'number',))
        self._validate_or_raise("invalid initial data")

    @property
    def unit(self) -> int:
        return self._atoms[1]

    @unit.setter
    def unit(self, v: int):
        self._set_atom(1, v)
        self._validate_or_raise()


class ListInBom(SExpr):  # (in_bom yes)
    def __init__(self, data):
        super().__init__(data, required_tag='in_bom', required_atoms=('string', 'string',))
        self._validate_or_raise("invalid initial data")

    @property
    def in_bom(self) -> str:
        return self._atoms[1]

    @in_bom.setter
    def in_bom(self, v: str):
        self._set_atom(1, v)
        self._validate_or_raise()


class ListOnBoard(SExpr):  # (on_board yes)
    def __init__(self, data):
        super().__init__(data, required_tag='on_board', required_atoms=('string', 'string',))
        self._validate_or_raise("invalid initial data")

    @property
    def on_board(self) -> str:
        return self._atoms[1]

    @on_board.setter
    def on_board(self, v: str):
        self._set_atom(1, v)
        self._validate_or_raise()


class ListSize(SExpr):  # (size 1.27 1.27)
    def __init__(self, data):
        super().__init__(data, required_tag='size',
                         required_atoms=('string', 'number', 'number',))
        self._validate_or_raise("invalid initial data")

    @property
    def x(self) -> float:
        return self._atoms[1]

    @x.setter
    def x(self, v: float):
        self._set_atom(1, v)
        self._validate_or_raise()

    @property
    def y(self) -> float:
        return self._atoms[2]

    @y.setter
    def y(self, v: float):
        self._set_atom(2, v)
        self._validate_or_raise()


class ListFont(SExpr):  # (font (size 1.27 1.27))
    def __init__(self, data):
        super().__init__(data, required_tag='font',
                         required_atoms=('string',), required_lists=('size',))
        self._validate_or_raise("invalid initial data")


class ListEffects(SExpr):  # (effects (font (size 1.27 1.27)) hide)
    def __init__(self, data):
        super().__init__(data, required_tag='effects', required_atoms=(
            'string',), optional_atoms=('string',), required_lists=('font',))
        self._validate_or_raise("invalid initial data")


class ListProperty(SExpr):
    # (property "Reference" "#PWR08" (id 0) (at 168.91 100.33 0)
    #   (effects (font (size 1.27 1.27)) hide)
    # )
    def __init__(self, data):
        super().__init__(data, required_tag='property',
                         required_atoms=('string', 'string', 'string'),
                         optional_lists=('id', 'at', 'effects',))
        self._validate_or_raise("invalid initial data")

    @property
    def key(self) -> str:
        return self._atoms[1]

    @property
    def value(self) -> str:
        return self._atoms[2]

    @value.setter
    def value(self, value):
        self[self._atom_indicies[2]] = value


class ListSymbolPin(SExpr):  # (pin "1" (uuid 0462adc4-54a7-4c18-967e-f6d78a20207f))
    def __init__(self, data):
        super().__init__(data, required_tag='pin', required_atoms=(
            'string', 'string',), required_lists=('uuid',))
        self._validate_or_raise("invalid initial data")

    @property
    def key(self) -> str:
        return self._atoms[1]


class ListSymbol(SExpr):
    #   (symbol (lib_id "power:GND") (at 168.91 93.98 0) (unit 1)
    #     (in_bom yes) (on_board yes)
    #     (uuid 18af9582-7c92-46f1-9603-90a0db4828ae)
    #     (property "Reference" "#PWR08" (id 0) (at 168.91 100.33 0)
    #       (effects (font (size 1.27 1.27)) hide)
    #     )
    #     (property "Value" "GND" (id 1) (at 169.037 98.3742 0))
    #     (property "Footprint" "" (id 2) (at 168.91 93.98 0)
    #       (effects (font (size 1.27 1.27)) hide)
    #     )
    #     (property "Datasheet" "" (id 3) (at 168.91 93.98 0)
    #       (effects (font (size 1.27 1.27)) hide)
    #     )
    #     (pin "1" (uuid 0462adc4-54a7-4c18-967e-f6d78a20207f))
    #   )
    def __init__(self, data):
        super().__init__(data, required_tag='symbol', required_atoms=('string',),
                         required_lists=('lib_id', 'at', 'unit', 'in_bom', 'on_board', 'uuid', 'property[]', 'pin[]'))
        self._validate_or_raise("invalid initial data")

    @property
    def properties(self) -> ():
        props = [ListProperty(x) for x in self._find_lists('property')]
        return tuple(props)

    @property
    def pins(self) -> ():
        pins = [ListSymbolPin(x) for x in self._find_lists('pin')]
        return tuple(pins)

    def _property(self, key: str) -> ListProperty:
        selected = [x for x in self.properties if x.key == key]

        return None if 0 == len(selected) else selected[0]

    @property
    def datasheet(self) -> ListProperty:
        return self._property('Datasheet')

    @property
    def footprint(self) -> ListProperty:
        return self._property('Footprint')

    @property
    def reference(self) -> ListProperty:
        return self._property('Reference')

    @property
    def value(self) -> ListProperty:
        return self._property('Value')

    @property
    def lib_id(self) -> ListLibId:
        return ListLibId(self["lib_id"])

    @property
    def at(self) -> ListAt:
        return ListAt(self['at'])

    @property
    def unit(self) -> ListUnit:
        return ListUnit(self['unit'])

    @property
    def in_bom(self) -> ListInBom:
        return ListInBom(self['in_bom'])

    @property
    def on_board(self) -> ListOnBoard:
        return ListOnBoard(self['on_board'])

    @property
    def uuid(self) -> ListUuid:
        return ListUuid(self['uuid'])

    def add_property(self, prop: ListProperty) -> None:
        self.add_list(prop._data)

    def get_property(self, key: str) -> ListProperty:
        return self._property(key)
