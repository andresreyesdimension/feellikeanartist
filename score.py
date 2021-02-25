
class Emoji(object):

	def __init__(self, data: dict):
		"""
		{
		 "emoji":"😟",
		 "unicode_name":"worried_face",
		 "sentiment_score":0.072,
		 "polarity":"positive"
		}
		"""
		self.emoji = data['emoji']
		self.unicode_name = data['unicode_name']
		self.sentiment_score = data['sentiment_score']
		self.polarity = data['polarity']


class Sentence(object):

	def __init__(self, data: dict):

		"""
		{
			 "text":"",
			 "text_score":-7.9,
			 "values":{
				"intensity":"",
				"polarity":""
			 }
		}
		:return:
		"""

		self.text = data['text']
		self.text_score = data['text_score']
		self.values = data['values']
		self.intensity = data['values']['intensity']
		self.polarity = data['values']['polarity']



class Score(Sentence, Emoji):

	def _calculate_text_score(self, sentences: list):

		"""

		:param sentences:
						[
							{'text': "",
							'text_score': -1.5,
							'values': {
										'polarity': 'neutral',
										'intensity': None}
							},
							{}
						]
		:return:
		"""

		score = 0
		if len(sentences) > 1:
			for s in sentences:
				sent = Sentence(s)
				if sent.polarity == 'positive':
					score += abs(sent.text_score)
				elif sent.polarity == 'negative':
					score -= abs(sent.text_score)
				elif sent.polarity == 'neutral':
					score = sent.text_score

		elif len(sentences) == 1:
			s = sentences[0]
			sent = Sentence(s)
			score = sent.text_score

		return score

	def _calculate_emoji_score(self, emojis: list, text_score: float):

		"""
		:param emojis:
		[
			{
				'emoji': '😔',
				'unicode_name': 'pensive_face',
				'sentiment_score': -0.146,
				'polarity': 'negative'
			}
		]

		:param text_score:
		:return:
		"""

		score = 0
		if len(emojis) > 0:
			for emo in emojis:
				e = Emoji(emo)
				if e.polarity == 'positive':
					score = text_score + abs(e.sentiment_score)
				elif e.polarity == 'negative':
					score = text_score - abs(e.sentiment_score)
		else:
			score = text_score

		return score
