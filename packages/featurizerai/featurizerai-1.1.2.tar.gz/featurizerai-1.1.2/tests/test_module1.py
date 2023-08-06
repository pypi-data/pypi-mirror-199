import unittest

from ..src.featurizerai.features import features


class TestSimple(unittest.TestCase):
    def test_add(self):
        g = features.get_features(self, 'http://127.0.0.1:5000/query?db=kafkastream&collection_name=names_by_device_last_30_days&device_id=3639')
        print(g)

if __name__ == '__main__':
    unittest.main()
