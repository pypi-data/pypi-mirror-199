from .sexpr import SExpr
from .lists import ListAt

class XYMixin:
    @property
    def x(self) -> str: 
        return self._atoms[1]

    @x.setter
    def x(self, v:str): 
        self._set_atom(1, v)
        self._validate_or_raise()
        
    @property
    def y(self) -> float: 
        return self[2]

    @y.setter
    def y(self, v:float): 
        self._set_atom(2, v)
        self._validate_or_raise()


class ListStart(SExpr, XYMixin):
    def __init__(self, data): 
        super().__init__(data, required_tag='start', required_atoms=('string', 'number', 'number',),)
        self._validate_or_raise("invalid initial data")


class ListEnd(SExpr, XYMixin):
    def __init__(self, data): 
        super().__init__(data, required_tag='end', required_atoms=('string', 'number', 'number',),)
        self._validate_or_raise("invalid initial data")


class ListLayer(SExpr):
    def __init__(self, data): 
        super().__init__(data, required_tag='layer', required_atoms=('string', 'string',),)
        self._validate_or_raise("invalid initial data")

    @property
    def name(self) -> str: 
        return self[1]

    @name.setter
    def name(self, v:str): 
        self._set_atom(1, v)
        self._validate_or_raise()


class ListFpText(SExpr):
    def __init__(self, data): 
        super().__init__(data, required_tag='fp_text', required_atoms=('string', 'string', 'string'),
            optional_atoms=('string',),
            required_lists=('at', 'layer', 'tstamp', 'effects',),
            )
        self._validate_or_raise(f"fp_text invalid initial data '{data}'")

    @property
    def key(self) -> str:
        return self._atoms[1]

    @property
    def text(self) -> str:
        return self._atoms[2]

    @text.setter
    def text(self, value):
        self[self._atom_indicies[2]] = value

    @property
    def at(self) -> ListAt:
        return ListAt(self['at'])

class ListFootprint(SExpr):
    def __init__(self, data): 
        super().__init__(data, required_tag='footprint', required_atoms=('string', 'string'), optional_atoms=('string',),
            required_lists=('layer', 'tedit', 'tstamp', 'at',),
            optional_lists=('descr', 'tags', 'property[]', 'path', 'attr', 'clearance', 'fp_text[]', 'fp_line[]', 'fp_rect[]', 'pad[]', 'model')
            )
        self._validate_or_raise("footprint invalid initial data")

    @property
    def lib_id(self) -> str:
        return self._atoms[1]

    @lib_id.setter
    def lib_id(self, value):
        self[self._atom_indicies[1]] = value

    @property
    def at(self) -> ListAt:
        return ListAt(self['at'])

    @property
    def fp_texts(self) -> ():
        return tuple([ListFpText(x) for x in self.all('fp_text')])

class ListGrText(SExpr):
    def __init__(self, data): 
        super().__init__(data, required_tag='gr_text', required_atoms=('string', 'string'),
            required_lists=('at', 'layer', 'tstamp', 'effects',),
            )
        self._validate_or_raise("invalid initial data")

    @property
    def text(self) -> str:
        return self._atoms[1]

    @text.setter
    def text(self, value):
        self[self._atom_indicies[1]] = value

    @property
    def at(self) -> ListAt:
        return ListAt(self['at'])

class ListGrRect(SExpr):
    def __init__(self, data): 
        super().__init__(data, required_tag='gr_rect', required_atoms=('string',),
            required_lists=('start', 'end', 'layer', 'width', 'fill', 'tstamp'),
            )
        self._validate_or_raise("invalid initial data")

    @property
    def start(self) -> ListStart:
        return ListStart(self['start'])

    @property
    def end(self) -> ListEnd:
        return ListEnd(self['end'])

    @property
    def layer(self) -> ListLayer:
        return ListLayer(self['layer'])

    def contains(self, other) -> bool:
        return other.at.x > self.start.x and other.at.y > self.start.y and other.at.x < self.end.x and other.at.y < self.end.y

"""
['gr_text', '⏚', 
    ['at', 51.802091, 61.703002], 
    ['layer', 'B.SilkS'], 
    ['tstamp', '0c7df807-3073-4929-bb80-e67459aef9d0'], 
    ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]], ['justify', 'mirror']]
]
"""

class Layout(SExpr):
    def __init__(self, data): 
        super().__init__(data, required_tag='kicad_pcb', required_atoms=('string',), 
            required_lists=('version', 'generator', 'general', 'paper',),
            optional_lists=('layers', 'setup', 'net[]', 'footprint[]', 'gr_poly[]', 'gr_line[]', 'gr_text[]', 'gr_rect[]', 'gr_arc[]', 'group[]', 'segment[]', 'zone[]'),
            )
        self._validate_or_raise("invalid initial data")

    @property
    def footprints(self) -> ():
        footprints = [ListFootprint(x) for x in self.all('footprint')]
        return tuple(footprints)

    @property
    def gr_texts(self) -> ():
        return tuple([ListGrText(x) for x in self.all('gr_text')])

    @property
    def gr_rects(self) -> ():
        return tuple([ListGrRect(x) for x in self.all('gr_rect')])
