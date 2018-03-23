import unittest

from transformation import summarize, PointsAccumulator


class PointsAccumulatorTests(unittest.TestCase):

    def test_summarize(self):
        min_val, max_val, avg, count = summarize([1])
        self.assertEqual(1, min_val)
        self.assertEqual(1, max_val)
        self.assertEqual(1, avg)
        self.assertEqual(1, count)

        min_val, max_val, avg, count = summarize([1, 2])
        self.assertEqual(1, min_val)
        self.assertEqual(2, max_val)
        self.assertEqual(1.5, avg)
        self.assertEqual(2, count)

    def test_add(self):
        scores = PointsAccumulator()
        key = 'abc'
        scores.add(key, 42)
        self.assertEqual(1, len(scores._scores))
        self.assertEqual([42], scores._scores[key])
        scores.add(key, 44)
        self.assertEqual(1, len(scores._scores))
        self.assertEqual([42, 44], scores._scores[key])
        scores.add('xyz', 111)
        min_val, max_val, avg, count = scores.summarize()[key]
        self.assertEqual(42, min_val)
        self.assertEqual(44, max_val)
        self.assertEqual(43, avg)
        self.assertEqual(2, count)


if __name__ == '__main__':
    unittest.main()
