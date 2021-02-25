from emotions_sentiment_analysis import Emotion
from score import Score


class Sentiment(Emotion, Score):

	"""
	sentiment = Sentiment('en')
	text = "i'm feeling sad"
	prediction = sentiment.emotion_state(text)
	print(prediction)
	"""

	def __init__(self, language):
		super().__init__(language)

	def emotion_state(self, full_text: str):

		"""
		Creating a Chatfuel block

		:param full_text:
		:return:
				{
					'intensity': 'low',
					'polarity': 'negative'
				}


		"""

		raw_data = self.raw_emotion_data(full_text)

		emojis = raw_data['emojis']
		sentences = raw_data['sentences']

		text_score = self._calculate_text_score(sentences)
		total_score = self._calculate_emoji_score(emojis, text_score)

		values = self.emotion_values(total_score)
		return values











