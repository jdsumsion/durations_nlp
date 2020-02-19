import unittest

from durations_nlp import Duration, Scale
from durations_nlp.exceptions import ScaleFormatError


class TestDuration(unittest.TestCase):
    def setUp(self):
        self.test_duration = Duration('1d')

    def tearDown(self):
        pass

    def test_repr_has_valid_representation(self):
        self.assertEqual(
            self.test_duration.__repr__(),
            '<Duration 1d>'
        )

    def test_parse_simple_valid_scale(self):
        duration_representation = self.test_duration.parse('1d')
        self.assertTrue(isinstance(duration_representation, list))

        duration_representation = duration_representation[0]
        self.assertEqual(duration_representation.value, 1.0)
        self.assertTrue(isinstance(duration_representation.scale, Scale))
        self.assertEqual(duration_representation.scale.representation.short, 'd')

    def test_parse_composed_valid_scale(self):
        duration_representation = self.test_duration.parse('1d, 24h and 36 minutes')  # noqa: E501

        self.assertTrue(isinstance(duration_representation, list))
        self.assertEqual(len(duration_representation), 3)

        first, second, third = duration_representation

        self.assertEqual(first.value, 1.0)
        self.assertTrue(isinstance(first.scale, Scale))
        self.assertEqual(first.scale.representation.short, 'd')

        self.assertEqual(second.value, 24.0)
        self.assertTrue(isinstance(second.scale, Scale))
        self.assertEqual(second.scale.representation.short, 'h')

        self.assertEqual(third.value, 36.0)
        self.assertTrue(isinstance(third.scale, Scale))
        self.assertEqual(third.scale.representation.short, 'm')

    def test_parse_simple_malformed_scale_raises(self):
        self.assertRaises(ScaleFormatError, Duration, 'd1')

    def test_parse_composed_malformed_scale_raises(self):
        self.assertRaises(ScaleFormatError, Duration, '1d h23')
