from clustering.clustering import get_data

url = 'https://data.boston.gov/api/action/datastore_search?resource_id=2968e2c0-d479-49ba-a884-4ef523ada3c0'
key1 = "result"
key2 = "records"

df = get_data(url, key1=key1, key2=key2)

# take out weird amount of requests geocoded to city hall
