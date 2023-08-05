from john import TestCase

from .lists import ListAt, ListId, ListUuid, ListLibId, ListUnit, ListInBom, ListOnBoard
from .lists import ListSize, ListFont, ListEffects, ListProperty, ListSymbolPin, ListSymbol

# (property "Reference" "#PWR08" (id 0) (at 168.91 100.33 0)
#       (effects (font (size 1.27 1.27)) hide)
#     )

# (property "Value" "GND" (id 1) (at 169.037 98.3742 0))

#     (property "Footprint" "" (id 2) (at 168.91 93.98 0)
#       (effects (font (size 1.27 1.27)) hide)
#     )
#     (property "Datasheet" "" (id 3) (at 168.91 93.98 0)
#       (effects (font (size 1.27 1.27)) hide)
#     )
#     (pin "1" (uuid 0462adc4-54a7-4c18-967e-f6d78a20207f))


class TestAt(TestCase):
    def test_init_with_wrong_tag(self):
        with self.assertRaisesAny():
            ListAt(['not_at'])

    def test_init_with_missing_required_Y_atom(self):
        with self.assertRaisesAny():
            ListAt(['at'], 1)

    def test_init_with_required_X_Y(self):
        with self.assertDoesNotRaise():
            ListAt(['at', 1, 2])

    def test_init_with_optional_angle(self):
        with self.assertDoesNotRaise():
            ListAt(['at', 1, 2, 3])


class TestAtdistance_from(TestCase):
    def test_valid_parm_does_raise(self):
        sut = ListAt(['at', 0, 0])

        with self.assertDoesNotRaise():
            sut.distance_from(ListAt(['at', 0, 0]))

    def test_distance(self):
        sut = ListAt(['at', 1, 1])

        actual = sut.distance_from(ListAt(['at',  1 + 3, 1 + 4]))

        self.assertEqual(actual, 5)


class TestAtProperties(TestCase):
    def setUp(self):
        self.sut = ListAt(['at', 42, 1729, 3.14])

    def test_tag(self):
        self.assertEqual(self.sut.tag, 'at')

    def test_getters(self):
        self.assertEqual(self.sut.x, 42)
        self.assertEqual(self.sut.y, 1729)
        self.assertEqual(self.sut.angle, 3.14)

    def test_set_x(self):
        self.sut.x = 13
        self.assertEqual(self.sut.tag, 'at')
        self.assertEqual(self.sut.x, 13)
        self.assertEqual(self.sut.y, 1729)
        self.assertEqual(self.sut.angle, 3.14)

    def test_set_y(self):
        self.sut.y = 27
        self.assertEqual(self.sut.tag, 'at')
        self.assertEqual(self.sut.x, 42)
        self.assertEqual(self.sut.y, 27)
        self.assertEqual(self.sut.angle, 3.14)

    def test_set_angle(self):
        self.sut.angle = 0
        self.assertEqual(self.sut.tag, 'at')
        self.assertEqual(self.sut.x, 42)
        self.assertEqual(self.sut.y, 1729)
        self.assertEqual(self.sut.angle, 0)

    def test_set_x_invalid_raises(self):
        with self.assertRaisesAny():
            self.sut.x = 'a'

    def test_set_y_invalid_raises(self):
        with self.assertRaisesAny():
            self.sut.y = 'a'

    def test_set_angle_invalid_raises(self):
        with self.assertRaisesAny():
            self.sut.angle = 'a'


class TestUuid(TestCase):
    def setUp(self):
        self.uuid = '18af9582-7c92-46f1-9603-90a0db4828ae'

    def test_init_with_wrong_tag(self):
        with self.assertRaisesAny():
            ListUuid(['not_uuid'])

    def test_init_with_missing_required_uuid_atom(self):
        with self.assertRaisesAny():
            ListUuid(['uuid'],)

    def test_init_with_required_uuid(self):
        with self.assertDoesNotRaise():
            ListUuid(['uuid', self.uuid])


class TestLibId(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListLibId(['lib_id', 'power:GND'])


class TestUnit(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListUnit(['unit', 1])


class TestInBom(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListInBom(['in_bom', 'yes'])


class TestOnBoard(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListOnBoard(['on_board', 'yes'])


class TestSize(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListSize(['size', 3.14, 1729])


class TestFont(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListFont(['font', ['size', 3.14, 1729]])


class TestEffects(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListEffects(['effects', ['font', ['size', 3.14, 1729]], 'hide'])


class TestProperty(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListProperty(['property', 'Reference', '#PWR08',
                          ['id', 1], ['at', 168.91, 100.33, 0],
                          ['effects', ['font', ['size', 3.14, 1729]], 'hide']])

    def test_key(self):
        sut = ListProperty(['property', 'Reference', '#PWR08',
                            ['id', 1], ['at', 168.91, 100.33, 0],
                            ['effects', ['font', ['size', 3.14, 1729]], 'hide']])

        self.assertEqual("Reference", sut.key)


class TestSymbolPin(TestCase):
    def test_init(self):
        with self.assertDoesNotRaise():
            ListSymbolPin(
                ['pin', '1', ['uuid', '0462adc4-54a7-4c18-967e-f6d78a20207f']])

    def test_key(self):
        sut = ListSymbolPin(
            ['pin', '1', ['uuid', '0462adc4-54a7-4c18-967e-f6d78a20207f']])
        self.assertEqual('1', sut.key)


symbol_data = ['symbol',
               ['lib_id', 'power:GND'],
               ['at',  168.91, 93.98, 0],
               ['unit', 1],
               ['in_bom', 'yes'],
               ['on_board', 'yes'],
               ['uuid', '18af9582-7c92-46f1-9603-90a0db4828ae'],
               ['property', 'Reference', '#PWR08',
                ['id', 1], ['at', 168.91, 100.33, 0],
                   ['effects', ['font', ['size', 3.14, 1729]], 'hide']],
               ['property', 'Value', 'GND', ['id', 1], ['at', 169.037, 98.3742, 0]],
               ['property', 'Footprint', '', ['id', 2], ['at', 168.91, 93.98, 0],
                ['effects', ['font', ['size', 3.14, 1729]], 'hide']],
               ['property', 'Datasheet', '', ['id', 3], ['at', 168.91, 93.98, 0],
                ['effects', ['font', ['size', 3.14, 1729]], 'hide']],
               ['pin', '1', ['uuid', '0462adc4-54a7-4c18-967e-f6d78a20207f']],
               ['pin', '2', ['uuid', 'ab6930b8-e44b-4fa6-a4a5-0f73c81f4f14']],
               ]


class TestSymbol(TestCase):
    def setUp(self):
        self.sut = ListSymbol(symbol_data)

    def test_init(self):
        with self.assertDoesNotRaise():
            ListSymbol(self.sut)


class TestSymbolProperties(TestCase):
    def setUp(self):
        self.sut = ListSymbol(symbol_data)

    def test_properies_is_properties_list(self):
        self.assertIsInstance(self.sut.properties, tuple)

    def test_properties_has_correct_length(self):
        self.assertEqual(4, len(self.sut.properties))

    def test_properties_contains_properties(self):
        for prop in self.sut.properties:
            self.assertIsInstance(prop, ListProperty)

    def test_properties_has_correct_properties(self):
        expected = ('Reference', 'Value', 'Footprint', 'Datasheet',)

        actual = tuple([x.key for x in self.sut.properties])

        self.assertSequenceEqual(actual, expected)

    def test_get_property_by_key(self):
        expected = "Datasheet"

        actual = self.sut.get_property(expected)

        self.assertEqual(actual.key, expected)

    def test_missing_property_returns_None(self):
        self.assertIsNone(self.sut._property("Missing"))

    def test_value(self):
        self.assertEqual('#PWR08', self.sut._property("Reference").value)

    def test_write_value(self):
        expected = 'NEW_FOOTPRINT'

        self.sut._property("Footprint").value = expected

        actual = self.sut._data[9][2]

        self.assertEqual(actual, expected)


class TestSymbolLists(TestCase):
    def setUp(self):
        self.sut = ListSymbol(symbol_data)

    def test_lib_id(self):
        self.assertEqual(self.sut.lib_id.lib_id, "power:GND")

    def test_at(self):
        self.assertEqual(self.sut.at.x, 168.91)
        self.assertEqual(self.sut.at.y, 93.98)
        self.assertEqual(self.sut.at.angle, 0)

    def test_unit(self):
        self.assertEqual(1, self.sut.unit.unit)

    def test_in_bom(self):
        self.assertEqual('yes', self.sut.in_bom.in_bom)

    def test_on_board(self):
        self.assertEqual('yes', self.sut.on_board.on_board)

    def test_uuid(self):
        self.assertEqual(
            '18af9582-7c92-46f1-9603-90a0db4828ae', self.sut.uuid.uuid)

    def test_reference(self):
        self.assertEqual("Reference", self.sut.reference.key)

    def test_value(self):
        self.assertEqual("Value", self.sut.value.key)
        self.assertEqual("GND", self.sut.value.value)

    def test_footprint(self):
        self.assertEqual("Footprint", self.sut.footprint.key)

    def test_datasheet(self):
        self.assertEqual("Datasheet", self.sut.datasheet.key)

    def test_pins(self):
        self.assertIsInstance(self.sut.pins, tuple)

    def test_pins_by_key(self):
        self.assertEqual('2', self.sut.pins[1].key)
