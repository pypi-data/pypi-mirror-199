from john import TestCase

from .schematic import Schematic


class TestSchematic(TestCase):
    def test_init_with_None_raises(self):
        with self.assertRaisesAny():
            Schematic()

    def test_init_with_wrong_tag_raises(self):
        data = ['ZZ9PZA', ['version', '20211123'], ['generator', 'eeschema']]

        with self.assertRaisesAny():
            Schematic(data)
