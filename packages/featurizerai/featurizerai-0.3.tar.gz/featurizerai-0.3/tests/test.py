from featurizerai.api import get_features, store_feature

# Retrieve features from the API
features = get_features('https://api.example.com/features')
print(features)

# Store a new feature via the API
new_feature = {'name': 'new_feature', 'description': 'A new feature'}
store_feature('https://api.example.com/features', new_feature)