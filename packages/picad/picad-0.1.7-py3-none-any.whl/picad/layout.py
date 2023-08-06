from .sexpr import SExpr
from .lists import ListAt
from math import sqrt

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


class ListPointBase(SExpr, XYMixin):
    def distance_from(self, other:XYMixin) -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return sqrt(dx * dx + dy * dy)

    def lerp(self, other:XYMixin, a:float) -> None:
        self.x += a * (other.x - self.x)
        self.y += a * (other.y - self.y)

    def move_to(self, other:XYMixin) -> None:
        self.lerp(other, 1.0)

class ListStart(ListPointBase):
    def __init__(self, data): 
        super().__init__(data, required_tag='start', required_atoms=('string', 'number', 'number',),)
        self._validate_or_raise("invalid initial data")


class ListEnd(ListPointBase):
    def __init__(self, data): 
        super().__init__(data, required_tag='end', required_atoms=('string', 'number', 'number',),)
        self._validate_or_raise("invalid initial data")


class LineMixin:
    @property
    def start(self) -> ListStart:
        return ListStart(self['start'])

    @property
    def end(self) -> ListEnd:
        return ListEnd(self['end'])

    @property
    def end_points(self):
        return (self.start, self.end,)


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

"""
['gr_text', '⏚', 
    ['at', 51.802091, 61.703002], 
    ['layer', 'B.SilkS'], 
    ['tstamp', '0c7df807-3073-4929-bb80-e67459aef9d0'], 
    ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]], ['justify', 'mirror']]
]
"""

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

"""
(gr_line 
    (start 7.740089 3.132185) 
    (end 7.740089 -6.616) 
    (layer "Edge.Cuts") 
    (width 0.1) 
    (tstamp 0f23c1d0-7aa6-43cc-9213-c1c2175be244)
)
"""

class ListGrLine(SExpr, LineMixin):
    def __init__(self, data): 
        super().__init__(data, required_tag='gr_line', required_atoms=('string',),
            required_lists=('start', 'end', 'layer', 'width', 'tstamp'),
            )
        self._validate_or_raise("invalid initial data")

    @property
    def layer(self) -> ListLayer:
        return ListLayer(self['layer'])

"""
(gr_arc 
    (start -12 4.687) 
    (mid -11.759765 4.146629) 
    (end -11.2115 3.925) 
    (layer "Edge.Cuts") 
    (width 0.1) 
    (tstamp 0636cef5-2fb7-4994-9efe-167d5ff96e48)
)
"""

class ListGrArc(SExpr, LineMixin):
    def __init__(self, data): 
        super().__init__(data, required_tag='gr_arc', required_atoms=('string',),
            required_lists=('start', 'mid', 'end', 'layer', 'width', 'tstamp'),
            )
        self._validate_or_raise("invalid initial data")

    @property
    def layer(self) -> ListLayer:
        return ListLayer(self['layer'])

"""
(gr_rect 
    (start -11.8465 -7.505) 
    (end 9.2355 17.133) 
    (layer "Dwgs.User") 
    (width 0.1) 
    (fill none) 
    (tstamp f5997333-8b86-4d95-b636-ef884537e0c7)
)
"""

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

    # todo foss: all 4 points
    @property
    def end_points(self):
        return (self.start, self.end,)

    @property
    def layer(self) -> ListLayer:
        return ListLayer(self['layer'])

    def contains(self, other) -> bool:
        return other.at.x > self.start.x and other.at.y > self.start.y and other.at.x < self.end.x and other.at.y < self.end.y

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

    @property
    def gr_arcs(self) -> ():
        return tuple([ListGrArc(x) for x in self.all('gr_arc')])

    @property
    def gr_lines(self) -> ():
        return tuple([ListGrLine(x) for x in self.all('gr_line')])

    def get_all_lines(self, layer_name:str=None) -> ():
        lines = self.gr_arcs + self.gr_lines
        if isinstance(layer_name, str):
            return [x for x in lines if layer_name == x.layer.name]
        else:
            return [x for x in lines]
