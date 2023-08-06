from john import TestCase

import copy

from .sexpr import SExpr, SExprEmpty


class TestInit(TestCase):
    def test_default_init_raises(self):
        with self.assertRaisesAny():
            SExpr()

    def test_init_with_None_raises(self):
        with self.assertRaisesAny():
            SExpr(None)

    def test_init_with_scalar_raises(self):
        with self.assertRaisesAny():
            SExpr('ZZ9PZA')

        with self.assertRaisesAny():
            SExpr(('ZZ9PZA',))

        with self.assertRaisesAny():
            SExpr(42)

        with self.assertRaisesAny():
            SExpr(3.14)

    def test_init_with_list_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr([])

    def test_init_with_SExpr_does_not_raise(self):
        SExpr(SExpr([]))
        with self.assertDoesNotRaise():
            SExpr(SExpr([]))

    def test_init_with_required_atoms_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr([], required_atoms=())

    def test_required_atoms_must_be_tuple(self):
        with self.assertRaisesAny():
            SExpr([], required_atoms=[])

    def test_init_with_optional_atoms_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr([], optional_atoms=())

    def test_optional_atoms_must_be_tuple(self):
        with self.assertRaisesAny():
            SExpr([], optional_atoms=[])

    def test_init_with_required_lists_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr([], required_lists=())

    def test_required_lists_must_be_tuple(self):
        with self.assertRaisesAny():
            SExpr([], required_lists=[])

    def test_required_lists_must_contain_strings(self):
        with self.assertRaisesAny():
            SExpr([], required_lists=('A', 'B', 3.14))

    def test_init_with_optional_lists_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr([], optional_lists=())

    def test_optional_lists_must_be_tuple(self):
        with self.assertRaisesAny():
            SExpr([], optional_lists=3.14)

    def test_optional_lists_must_contain_strings(self):
        with self.assertRaisesAny():
            SExpr([], optional_lists=('A', [], 'B'))


class TestValidate(TestCase):
    def test_data_must_not_be_empty(self):
        sut = SExpr([])

        self.assertFalse(sut._validate())

    def test_must_not_have_zero_atoms(self):
        sut = SExpr([['ZZ9PZA']])

        self.assertFalse(sut._validate())

    def test_first_atom_must_be_string(self):
        self.assertFalse(SExpr([42])._validate())
        self.assertFalse(SExpr([3.14])._validate())

    def test_invalid_atom_type_raises(self):
        with self.assertRaisesAny():
            SExpr(['ZZ9PZA'], required_atoms=('a',))

    def test_string_atom_type_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr(['ZZ9PZA'], required_atoms=('string',))

    def test_number_atom_type_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr(['ZZ9PZA'], required_atoms=('number',))

    def test_first_atom_string_wrong_type(self):
        self.assertFalse(
            SExpr(['ZZ9PZA'], required_atoms=('number',))._validate())

    def test_first_atom_string(self):
        self.assertTrue(
            SExpr(['ZZ9PZA'], required_atoms=('string',))._validate())

    def test_second_atom_string(self):
        self.assertTrue(SExpr(['ZZ9PZA', 'A'], required_atoms=(
            'string', 'string',))._validate())

    def test_second_atom_number_is_float(self):
        self.assertTrue(SExpr(['ZZ9PZA', 3.14], required_atoms=(
            'string', 'number',))._validate())

    def test_second_atom_number_is_int(self):
        self.assertTrue(SExpr(['ZZ9PZA', 1729], required_atoms=(
            'string', 'number',))._validate())

    def test_more_atoms_than_required(self):
        self.assertFalse(SExpr(['ZZ9PZA', 'A', 'B'], required_atoms=(
            'string', 'string',))._validate())

    def test_too_many_optional_atoms(self):
        self.assertFalse(SExpr(['ZZ9PZA', 'A', 'B'], required_atoms=(
            'string', 'string',), optional_atoms=())._validate())

    def test_one_optional_number_atom(self):
        self.assertTrue(SExpr(['ZZ9PZA', 'A', 3.14], required_atoms=(
            'string', 'string',), optional_atoms=('number',))._validate())

    def test_one_optional_number_atom_wrong_type(self):
        self.assertFalse(SExpr(['ZZ9PZA', 'A', 'B'], required_atoms=(
            'string', 'string',), optional_atoms=('number',))._validate())

    def test_one_optional_string_atom_wrong_type(self):
        self.assertFalse(SExpr(['ZZ9PZA', 'A', 3.14], required_atoms=(
            'string', 'string',), optional_atoms=('string',))._validate())

    def test_one_optional_atom_not_supplied(self):
        SExpr(['ZZ9PZA', 'A'], required_atoms=('string', 'string',),
              optional_atoms=('number',))._validate()
        self.assertTrue(SExpr(['ZZ9PZA', 'A'], required_atoms=(
            'string', 'string',), optional_atoms=('number',))._validate())

    def test_two_optional_atoms(self):
        self.assertTrue(SExpr(['ZZ9PZA', 'A', 'B', 'C'], required_atoms=(
            'string', 'string',), optional_atoms=('string', 'string',))._validate())

    def test_required_lists(self):
        self.assertTrue(SExpr(['ZZ9PZA', ['A']], required_atoms=(
            'string',), required_lists=('A',))._validate())

    def test_required_lists_longer_than_lists(self):
        self.assertFalse(SExpr(['ZZ9PZA', ['A']], required_atoms=(
            'string',), required_lists=('A', 'B',))._validate())

    def test_required_lists_missing(self):
        self.assertFalse(SExpr(['ZZ9PZA', ['B']], required_atoms=(
            'string',), required_lists=('A',))._validate())

    def test_required_lists_missing_one(self):
        self.assertFalse(SExpr(['ZZ9PZA', ['A'], ['B']], required_atoms=(
            'string',), required_lists=('A', 'C',))._validate())

    def test_one_optional_list_missing(self):
        self.assertFalse(SExpr(['ZZ9PZA', ['A'], ['B']], required_atoms=(
            'string',), required_lists=('A',), optional_lists=('C',))._validate())

    def test_one_optional_list(self):
        self.assertTrue(SExpr(['ZZ9PZA', ['A'], ['B']], required_atoms=(
            'string',), required_lists=('A',), optional_lists=('B',))._validate())

    def test_two_optional_lists_second_missing(self):
        self.assertFalse(SExpr(['ZZ9PZA', ['A'], ['B'], ['C']], required_atoms=(
            'string',), required_lists=('A',), optional_lists=('B',))._validate())

    def test_required_and_optional_lists_mixed(self):
        self.assertTrue(SExpr(['ZZ9PZA', ['opt_A'], ['req_B'], ['opt_C']], required_atoms=(
            'string',), required_lists=('req_B',), optional_lists=('opt_A', 'opt_C'))._validate())

    def test_only_optional_lists(self):
        self.assertTrue(SExpr(['ZZ9PZA', ['opt_A'], ['opt_B']], required_atoms=(
            'string',), optional_lists=('opt_A', 'opt_B'))._validate())

    def test_keyed_list_accepted(self):
        self.assertTrue(SExpr(['ZZ9PZA', ['A', 'key_A']], required_atoms=(
            'string',),  required_lists=('A[]',))._validate())

    def test_non_keyed_list_does_not_allow_duplicates(self):
        self.assertFalse(SExpr(['ZZ9PZA', ['A'], ['A']], required_atoms=(
            'string',),  required_lists=('A',))._validate())

    def test_keyed_list_does_allow_duplicates(self):
        self.assertTrue(SExpr(['ZZ9PZA', ['A'], ['A']], required_atoms=(
            'string',),  required_lists=('A[]',))._validate())

    def test_required_tag_wrong_tag(self):
        self.assertFalse(SExpr(['ZZ9PZA'], required_atoms=(
            'string',), required_tag='A')._validate())

    def test_required_tag(self):
        self.assertTrue(SExpr(['ZZ9PZA'], required_atoms=(
            'string',), required_tag='ZZ9PZA')._validate())

    def test_validate_or_raise(self):
        with self.assertRaisesAny():
            SExpr(['ZZ9PZA'], required_atoms=('string',),
                  required_tag='A')._validate_or_raise()


class TestAtomIndexer(TestCase):
    def test_atom_indexer_not_found_does_not_raise(self):
        sut = SExpr(['ZZ9PZA', 'other'])

        with self.assertDoesNotRaise():
            sut[2]

    def test_atom_indexer_not_found_returns_Empty(self):
        sut = SExpr(['ZZ9PZA', 'other'])

        actual = sut[2]

        self.assertIsInstance(actual, SExprEmpty)

    def test_atom_get_indexer(self):
        expected = 'ZZ9PZA'

        sut = SExpr(['blah', expected, 'other'])

        actual = sut[1]

        self.assertEqual(actual, expected)

    def test_set_indexer_non_integer_index_raises(self):
        sut = SExpr(['ZZ9PZA'])

        with self.assertRaisesAny():
            sut['Arthur'] = 1

    def test_atom_set_indexer_int(self):
        sut = SExpr(['ZZ9PZA'])

        expected = 42

        sut[0] = expected

        actual = sut[0]

        self.assertEqual(actual, expected)

    def test_atom_set_indexer_float(self):
        sut = SExpr(['ZZ9PZA'])

        expected = 3.14

        sut[0] = expected

        actual = sut[0]

        self.assertEqual(actual, expected)

    def test_atom_set_indexer_string(self):
        sut = SExpr(['ZZ9PZA'])

        expected = 'Ford'

        sut[0] = expected

        actual = sut[0]

        self.assertEqual(actual, expected)


class TestListIndexer(TestCase):
    def test_list_indexer_not_found_does_not_raise(self):
        sut = SExpr(['ZZ9PZA', 'other'])

        with self.assertDoesNotRaise():
            sut['cabbage']

    def test_list_indexer_not_found_returns_Empty(self):
        sut = SExpr(['ZZ9PZA', 'other'])

        actual = sut['cabbage']

        self.assertIsInstance(actual, SExprEmpty)

    def test_list_get_indexer(self):
        key = 'ZZ9PZA'

        expected = [key, 'blah']

        sut = SExpr(['blah', expected, ['other']])

        actual = sut[key]
        self.assertIsInstance(actual, SExpr)
        self.assertListEqual(actual._data, expected)

    def test_list_get_indexer_list_key_raises(self):
        sut = SExpr(['ZZ9PZA'])

        with self.assertRaisesAny():
            sut[[]]

    def test_list_get_indexer_tuple_key_not_found_returns_Empty(self):
        keys = ('ZZ9PZA', 'Lemon')

        expected = [keys[0], keys[1], 'blah']

        sut = SExpr(['blah', expected, ['other']])

        actual = sut[tuple(keys) + ('a',)]

        self.assertIsInstance(actual, SExprEmpty)

    def test_list_get_indexer_tuple_key(self):
        keys = ('ZZ9PZA', 'Lemon')

        expected = [keys[0], keys[1], 'blah']

        sut = SExpr(['blah', expected, ['other']])

        actual = sut[tuple(keys)]

        self.assertIsInstance(actual, SExpr)
        self.assertListEqual(actual._data, expected)


class TestAddList(TestCase):
    def test_add_list(self):
        sut = SExpr(['ZZ9PZA'])

        ll = ['a', 'b']

        sut.add_list(ll)

        expected = copy.deepcopy(ll)

        actual = sut._lists[0]

        self.assertListEqual(actual, expected)


class TestAll(TestCase):
    def test_empty_all_returns_empty_tuple(self):
        sut = SExpr(['A'])

        actual = sut.all('ZZ9PZA')

        expected = ()

        self.assertTupleEqual(actual, expected)

    def test_all_returns_tuple(self):
        sut = SExpr(['ZZ9PZA'])

        actual = sut.all('ZZ9PZA')

        self.assertIsInstance(actual, tuple)

    def test_all(self):
        data = ['ZZ9PZA',
                ['A', 'B', 'C'],
                ['B', 'B', 'D'],
                ['A', 'B', 'E']
                ]

        sut = SExpr(data)

        expected = [data[1], data[3]]

        actual = [sexpr._data for sexpr in sut.all(('A', 'B',))]

        self.assertSequenceEqual(expected, actual)


class TestFirst(TestCase):
    def test_missing_first_returns_Empty(self):
        sut = SExpr(['A'])

        actual = sut.first('ZZ9PZA')

        self.assertIsInstance(actual, SExprEmpty)

    def test_first(self):
        sut = SExpr(['ZZ9PZA', ['ZZ9PZA', 'A'], ['ZZ9PZA', 'B']])

        actual = sut.first('ZZ9PZA')._data

        expected = sut._lists[0]

        self.assertListEqual(actual, expected)


class TestRemove(TestCase):
    def test_empty_remove_atom_does_not_raise(self):
        with self.assertDoesNotRaise():
            SExpr(['ZZ9PZA']).remove(2)

    def test_remove_atom(self):
        sut = SExpr(['A', 'B', 'C'])

        expected = (sut[0], sut[2])

        sut.remove(1)

        actual = sut._atoms

        self.assertTupleEqual(actual, expected)

    def test_remove_list(self):
        sut = SExpr(['ZZ9PZA', ['A', 'B'], ['C', 'D']])

        expected = (sut._lists[0],)

        sut.remove('C')

        actual = sut._lists

        self.assertTupleEqual(actual, expected)


class TestKeyed_lists(TestCase):
    def test_get_keyed_list(self):
        expected = ['A', '2']
        sut = SExpr(['ZZ9PZA', ['A', '1'], expected],
                    required_atoms=('string',), required_lists=('A[]',))

        actual = sut._get_keyed_list('A', '2')

        self.assertSequenceEqual(actual, expected)
