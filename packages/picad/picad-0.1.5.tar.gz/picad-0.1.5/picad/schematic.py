from .sexpr import SExpr
from .lists import ListSymbol


class Schematic(SExpr):
    def __init__(self, data):
        super().__init__(data, required_tag='kicad_sch', required_atoms=('string',),
                         required_lists=('version', 'generator',
                                         'uuid', 'paper',),
                         optional_lists=('lib_symbols', 'junction[]', 'label[]', 'text[]', 'wire[]', 'no_connect[]', 'global_label[]',
                                         'sheet[]', 'sheet_instances', 'symbol_instances', 'symbol[]',),
                         )
        self._validate_or_raise("invalid initial data")

    @property
    def symbols(self) -> ():
        symbols = [ListSymbol(x) for x in self.all('symbol')]
        return tuple(symbols)
