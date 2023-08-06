import unittest

from ..src.featurizerai.features import features

# Retrieve features from the API
features = features.get_features('https://api.example.com/features')
print(features)
