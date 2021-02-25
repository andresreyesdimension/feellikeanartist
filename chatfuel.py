import random
from cf_components import ChatComponents
from sentiment import Sentiment
from app_search import ElasticSearch
from config_logger import custom_logger

logger = custom_logger()

class Chatfuel(ChatComponents):

	def __init__(self):
		super().__init__()
		self.freespeech = ""
		self.target_emotion = ""
		self.new_block = ""


	def handle_answer(self, data: dict):

		"""
		:request:
					{
						"freespeech": "",
						"user":"{{first name}}",
						"target_emotion": ""
					}
		:return:
				{
					"set_attributes": {
					    "block": "emotive_state",
					    "intensity": "high",
					    "polarity": "negative"
					  }
				}
		"""

		if 'freespeech' in data:
			self.freespeech = data['freespeech']
		if 'target_emotion' in data:
			self.target_emotion = data['target_emotion']
		if 'default_language' in data:
			self.default_language = data['default_language']

		attribute_session = self.analyze_sentiment()
		attributes = {
			"set_attributes": attribute_session
		}
		return attributes

	def analyze_sentiment(self):

		attribute_session = dict()

		sentiment = Sentiment(self.default_language)
		e = sentiment.emotion_state(self.freespeech)

		intensity = e['intensity']
		polarity = e['polarity']


		log_info = {
			"log": "Pol & intensity",
			"polarity": polarity,
			"intensity":intensity
		}
		logger.info(log_info)


		attribute_session['intensity'] = intensity
		attribute_session['polarity'] = polarity
		attribute_session['block'] = "emotive_state"
		return attribute_session


	def redirect_block(self, data: dict):

		blocks = list()
		block = data['block']
		blocks.append(block)

		redirect = {
			"redirect_to_blocks": blocks
		}

		return redirect

	def galleries(self, query):

		es = ElasticSearch()

		log_info = {
			"log": "ElasticSearch Query",
			"query": query,
		}
		logger.info(log_info)

		opere = es.search(query)
		for opera in opere:

			sentiment = (random.choice(opera.sentiment))
			emotion, intensity = sentiment.split('_')

			self.card_gallery(
					title=opera.titolo,
					image_url=opera.url_image,
					sub_title=opera.name,
					redirect_block=emotion)

		gallery = self.gallery_component()
		return gallery

	def send_images(self, url_image):

		image = {
			"messages": [
				{
					"attachment": {
						"type": "image",
						"payload": {
							"url": url_image
						}
					}
				}
			]
		}

		return image




