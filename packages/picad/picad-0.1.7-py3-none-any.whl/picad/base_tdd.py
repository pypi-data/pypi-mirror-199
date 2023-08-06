from john import TestCase

from .base import SExprBase
from .kicad import parse_sexpr

symbol_text = """
  (symbol (lib_id "power:GND") (at 168.91 93.98 0) (unit 1)
    (in_bom yes) (on_board yes)
    (uuid 18af9582-7c92-46f1-9603-90a0db4828ae)
    (property "Reference" "#PWR08" (id 0) (at 168.91 100.33 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (id 1) (at 169.037 98.3742 0))
    (property "Footprint" "" (id 2) (at 168.91 93.98 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (id 3) (at 168.91 93.98 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid 0462adc4-54a7-4c18-967e-f6d78a20207f))
  )
"""

property_text = """
    (property "Value" "2.2K 1%" (id 1) (at 179.578 123.19 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
"""


class KiFabSExprSubClass(SExprBase):
    pass


class TestInit(TestCase):
    def setUp(self):
        SExprBase._allow_instantiate_base = True
        SExprBase.allow_empty = True

    def test_instantiate_raises_if_not_allowed(self):
        SExprBase._allow_instantiate_base = False

        with self.assertRaisesAny():
            SExprBase(['ZZ9PZA'])

    def test_instantiate_does_not_raise_if_allowed(self):
        SExprBase._allow_instantiate_base = True

        with self.assertDoesNotRaise():
            SExprBase(['ZZ9PZA'])

    def test_instantiate_does_not_raise_if_not_allowed(self):
        SExprBase._allow_instantiate_base = False

        with self.assertDoesNotRaise():
            tag = 'ZZ9PZA'
            data = [tag]
            sut = KiFabSExprSubClass(data)

            self.assertIsInstance(sut, KiFabSExprSubClass)

            expected = tag

            actual = sut.tag

            self.assertEqual(actual, expected)

    def test_throws_with_None_and_not_allow_empty(self):
        SExprBase.allow_empty = False

        with self.assertRaisesAny():
            SExprBase(None)

    def test_does_not_throw_with_None_and_allow_empty(self):
        SExprBase.allow_empty = True

        with self.assertDoesNotRaise():
            SExprBase(None)

    def test_throws_with_invalid_data(self):
        invalid_data = "(ZZ9PZA)"

        with self.assertRaisesAny():
            SExprBase(invalid_data)

    def test_is_empty_when_empty(self):
        sut = SExprBase(None)

        self.assertTrue(sut.is_empty)

    def test_is_empty_when_not_empty(self):
        data = ['ZZ9PZA']

        sut = SExprBase(data)

        self.assertFalse(sut.is_empty)


class TestTag(TestCase):
    def test_tag_with_valid_tag(self):
        expected = 'ZZ9PZA'

        actual = SExprBase([expected]).tag

        self.assertEqual(actual, expected)

    def test_does_not_raise_without_tag(self):
        with self.assertDoesNotRaise():
            SExprBase([]).tag

    def test_invalid_tag_returns_none(self):
        self.assertIsNone(SExprBase([1729]).tag)


class TestAtoms(TestCase):
    def setUp(self):
        SExprBase._allow_instantiate_base = True
        SExprBase.allow_empty = False

        self.symbol = SExprBase(data=parse_sexpr(symbol_text))

    def test_atoms(self):
        expected = ('symbol',)

        actual = self.symbol._atoms

        self.assertTupleEqual(actual, expected)

    def test_add_atom_None_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_atom(None)

    def test_add_atom_list_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_atom([])

    def test_add_atom_tuple_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_atom(())

    def test_add_atom_string_does_not_raise(self):
        with self.assertDoesNotRaise():
            self.symbol._add_atom("ZZ9PZA")

    def test_add_atom_int_does_not_raise(self):
        with self.assertDoesNotRaise():
            self.symbol._add_atom(42)

    def test_add_atom_float_does_not_raise(self):
        with self.assertDoesNotRaise():
            self.symbol._add_atom(3.14)

    def test_add_atom_increases_number_of_atoms(self):
        expected = len(self.symbol._atoms) + 1

        self.symbol._add_atom('ZZ9PZA')

        actual = len(self.symbol._atoms)

        self.assertEqual(actual, expected)

    def test_add_atom(self):
        atom = 'ZZ9PZA'

        self.symbol._add_atom(atom)

        expected = ('symbol', atom)

        actual = self.symbol._atoms

        self.assertTupleEqual(actual, expected)

    def test_atom_indices_one_list(self):
        sut = SExprBase(['ZZ9PZA', [], 'A'])

        expected = (0, 2,)

        actual = sut._atom_indicies

        self.assertSequenceEqual(actual, expected)

    def test_set_atom_out_of_range_raises(self):
        sut = SExprBase(['a', 'b'])

        with self.assertRaisesAny():
            sut._set_atom(2, 'a')

    def test_set_atom_wrong_type_raises(self):
        sut = SExprBase(['a', 'b'])

        with self.assertRaisesAny():
            sut._set_atom(1, [])

    def test_set_atom_invalid_index_raises(self):
        with self.assertRaisesAny():
            SExprBase(['a', 'b'])._set_atom('a', 'b')

    def test_set_atom_sets_value(self):
        data = ['a', [], 'b']

        expected = 'c'

        sut = SExprBase(data)
        sut._set_atom(1, expected)

        actual = sut._atoms[1]

        self.assertEqual(actual, expected)

    def test_remove_atom_decreases_number_of_atoms(self):
        expected = len(self.symbol._atoms) - 1

        self.symbol._remove_atom('symbol')

        actual = len(self.symbol._atoms)

        self.assertEqual(actual, expected)

    def test_remove_missing_atom_does_not_raise(self):
        with self.assertDoesNotRaise():
            self.symbol._remove_atom('ZZ9PZA')

    # todo foss: more than one atom


class TestLists(TestCase):
    def setUp(self):
        SExprBase._allow_instantiate_base = True
        SExprBase.allow_empty = True

        self.symbol = SExprBase(data=parse_sexpr(symbol_text))

    def test_lists(self):
        expected = (
            ['lib_id', 'power:GND'],
            ['at', 168.91, 93.98, 0],
            ['unit', 1],
            ['in_bom', 'yes'],
            ['on_board', 'yes'],
            ['uuid', '18af9582-7c92-46f1-9603-90a0db4828ae'],
            ['property', 'Reference', '#PWR08', ['id', 0], ['at', 168.91, 100.33, 0], [
                'effects', ['font', ['size', 1.27, 1.27]], 'hide']],
            ['property', 'Value', 'GND', ['id', 1], ['at', 169.037, 98.3742, 0]],
            ['property', 'Footprint', '', ['id', 2], ['at', 168.91, 93.98, 0],
                ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
            ['property', 'Datasheet', '', ['id', 3], ['at', 168.91, 93.98, 0],
                ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
            ['pin', '1', ['uuid', '0462adc4-54a7-4c18-967e-f6d78a20207f']]
        )

        actual = self.symbol._lists

        self.assertTupleEqual(actual, expected)

    def test_find_lists_returns_tuple(self):
        keys = ("property", "Value")

        actual = self.symbol._find_lists(keys)

        self.assertIsInstance(actual, tuple)
        self.assertEqual(len(actual), 1)

    def test_find_lists_returns_correct_types(self):
        ll = self.symbol._find_lists(("property", "Value"))
        actual = ll[0]

        self.assertEqual(len(actual), 5)
        self.assertIsInstance(actual[0], str)
        self.assertIsInstance(actual[1], str)
        self.assertIsInstance(actual[2], str)
        self.assertIsInstance(actual[3], list)
        self.assertIsInstance(actual[4], list)

    def test_find_lists_returns_correct_data(self):
        expected = ['property', 'Value', 'GND', [
            'id', 1], ['at', 169.037, 98.3742, 0]]

        actual = self.symbol._find_lists(("property", "Value"))[0]

        self.assertListEqual(actual, expected)

    def test_add_None_list_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_list(None)

    def test_add_empty_list_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_list([])

    def test_add_one_element_list_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_list([None])

    def test_add_two_element_list_without_name_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_list([None, None])

    def test_add_two_element_list_with_non_string_name_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_list([2, None])

    def test_add_two_element_list_with_empty_name_raises(self):
        with self.assertRaisesAny():
            self.symbol._add_list(['', None])

    def test_add_two_element_list_with_name_does_not_raise(self):
        with self.assertDoesNotRaise():
            self.symbol._add_list(['ZZ9PZA', None])

    def test_add_list_increases_number_of_lists(self):
        expected = len(self.symbol._lists) + 1

        self.symbol._add_list(['A', 'B'])

        actual = len(self.symbol._lists)

        self.assertEqual(actual, expected)

    def test_add_list_adds_list(self):
        ll = ["ZZ9PZA", 42]

        self.symbol._add_list(ll)

        expected = ll

        actual = self.symbol._lists[11]

        self.assertListEqual(actual, expected)

    def test_remove_nonexistent_list_raises(self):
        with self.assertRaisesAny():
            self.symbol._remove_list(['a', 'b'])

    def test_remove_list_decreases_number_of_lists(self):
        expected = len(self.symbol._lists) - 1

        ll = self.symbol._lists[1]

        self.symbol._remove_list(ll)

        actual = len(self.symbol._lists)

        self.assertEqual(actual, expected)

    def test_remove_list_removes_list(self):
        expected = self.symbol._lists[2]

        self.symbol._remove_list(self.symbol._lists[1])

        actual = self.symbol._lists[1]

        self.assertListEqual(actual, expected)


class SanityChecks(TestCase):
    def setUp(self):
        SExprBase._allow_instantiate_base = False
        SExprBase.allow_empty = False

        self.symbol = KiFabSExprSubClass(data=parse_sexpr(symbol_text))

    def test_update_list_works(self):
        value = self.symbol._find_lists(("property", "Value"))[0]

        expected = "3v3"

        value[2] = expected

        actual = self.symbol._data[8][2]

        self.assertEqual(actual, expected)

    def test_overridden_new_has_not_done_anything_weird(self):
        tag = 'ZZ9PZA'
        data = [tag]
        sut = KiFabSExprSubClass(data)

        self.assertIsInstance(sut, KiFabSExprSubClass)

        expected = tag

        actual = sut.tag

        self.assertEqual(actual, expected)
