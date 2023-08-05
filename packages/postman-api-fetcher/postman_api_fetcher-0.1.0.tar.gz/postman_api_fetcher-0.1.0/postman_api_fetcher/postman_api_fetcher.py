import requests

class PostmanAPIFetcher:
    def __init__(self, api_key, collection_name):
        self.api_key = api_key
        self.collection_name = collection_name
        self.base_url = 'https://api.getpostman.com'

    def get_collections(self):
        """Fetch all collections for the provided API key."""
        url = f"{self.base_url}/collections"
        headers = {'X-Api-Key': self.api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()['collections']
        else:
            raise Exception(f"An error occurred while fetching API collections. Status code: {response.status_code}")

    def get_collection_by_name(self):
        """Fetch a collection by name and return its details."""
        collections = self.get_collections()
        collection = next((c for c in collections if c['name'] == self.collection_name), None)

        if collection:
            collection_id = collection['uid']
            collection_url = f"{self.base_url}/collections/{collection_id}"
            headers = {'X-Api-Key': self.api_key}
            collection_response = requests.get(collection_url, headers=headers)

            if collection_response.status_code == 200:
                return collection_response.json()['collection']
            else:
                raise Exception(f"Error fetching collection '{self.collection_name}'. Status code: {collection_response.status_code}")
        else:
            raise Exception(f"Collection with name '{self.collection_name}' not found.")
