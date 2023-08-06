import requests

def get_features(api_url):
    """
    Retrieves features from the API endpoint.

    Args:
        api_url (str): The URL of the API endpoint.

    Returns:
        list: A list of feature objects.
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to retrieve features. Status code: {response.status_code}")

def store_feature(api_url, feature):
    """
    Stores a feature via the API endpoint.

    Args:
        api_url (str): The URL of the API endpoint.
        feature (dict): A dictionary representing the feature to store.
    """
    response = requests.post(api_url, json=feature)
    if response.status_code != 200:
        raise ValueError(f"Failed to store feature. Status code: {response.status_code}")
