import json
import requests
from urllib import parse
from params import opere_url, baseurl


class Opere(object):

	def __init__(self):
		super().__init__()
		self.opere_url = opere_url
		self.baseurl = baseurl
		self.headers = {
			'Content-Type': 'application/json'
		}

	def get_opere(self, opera_umbraco_id):

		payload= {
			  "skip":0,
			  "take":10000,
			  "cropper": ["300x300"],
			  "mainImage":True,
			  "people":True,
			  "gallery":True,
			  "tags": True,
			  "filter": {
				  "id": [opera_umbraco_id]
			  }
		  }

		response = requests.post(self.opere_url, headers=self.headers, data=json.dumps(payload))
		res = json.loads(response.text.encode('utf8'))
		return res

	def _opera_colorTags(self, opera):

		"""
		Cleaning color tags
		:param opera:
		:return:
		"""

		color_tags = opera['colorTags']
		color_tags = color_tags.split(",")

		colors = list()
		for color_tag in color_tags:
			color_tag = color_tag.split("_")
			color = color_tag[0]
			colors.append(color)
		return colors

	def _opera_shapeTags(self, opera):

		"""
		Cleaning Shapes Tags
		:param opera:
		:return:
		"""

		shape_tags = opera['shapeTags']
		shape_tags = shape_tags.split(",")

		shapes = list()
		for shape_tag in shape_tags:
			# shape_tag = shape_tag.split("_")
			# color = shape_tag[0]
			shapes.append(shape_tag)
		return shapes

	def _opera_sentimentTags(self, opera):

		"""
		Cleaning Shapes Tags
		:param opera:
		:return:
		"""

		sentiment_tags = opera['sentimentTags']
		sentiment_tags = sentiment_tags.split(",")

		sentiments = list()
		for sentiment_tag in sentiment_tags:
			sentiments.append(sentiment_tag)
		return sentiments

	def _parse_images(self, res):

		artisti = res['list']
		artists_images = list()

		for opera in artisti:
			artist = dict()
			colors = self._opera_colorTags(opera)
			shapes = self._opera_shapeTags(opera)
			sentiment = self._opera_sentimentTags(opera)

			artist['id'] = opera['id']
			artist['name'] = opera['name']
			artist['titolo'] = opera['titolo']
			artist['classificazione'] = opera['classificazione']
			artist['light'] = opera['lightTags']
			artist['sentiment'] = sentiment
			artist['shapes'] = shapes
			artist['colors'] = colors

			url_image = opera['immaginePrincipale'][0]
			artist['url_image'] = parse.unquote(self.baseurl + url_image['url'])

			artists_images.append(artist)

		res = {
				"opere": artists_images,
				"count_opere": len(artists_images),
			}

		return res

	def get_opere_id(self, opera_umbraco_id):
		res = self.get_opere(opera_umbraco_id)
		res = self._parse_images(res)
		opere = res['opere']
		return opere[0]



