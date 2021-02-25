from elastic_enterprise_search import AppSearch
from params import search_url, private_key, engine_name


class Artwork(object):

	def __init__(self, result):
		self.name = result['name']['raw']
		self.titolo = result['titolo']['raw']
		self.url_image = result['url_image']['raw']
		self.classificazione = result['classificazione']['raw']
		self.light = result['light']['raw']
		self.sentiment = result['sentiment']['raw']
		self.shapes = result['shapes']['raw']
		self.colors = result['colors']['raw']
		self.id =result['_meta']['id']
		self.score = result['_meta']['score']

class ElasticSearch(object):

	def __init__(self):
		self.engine_name = engine_name
		self.client = self.setup_client()

	def setup_client(self):
		client = AppSearch(search_url, private_key)
		return client

	def search(self, query: str):
		"""
		ElasticSearch Query
		:param query:
		:return:
		"""

		body = {
	        "query": query,
	    }
		res = self.client.search(engine_name=self.engine_name,  body=body)
		results = self.parse_response(res)
		return results

	def parse_response(self, results):
		artworks = list()
		for result in results['results']:
			artwork = Artwork(result)
			artworks.append(artwork)
		return artworks
