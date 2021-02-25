import emoji
import re
import json
import requests
from bs4 import BeautifulSoup


class EmojiModel(object):

	"""
	Emoji DataModel
	"""

	def __init__(self, data):
		"""	
		{
			'polarity': 'positive', 
			'emoji': '😂', 
			'unicode_name': 'face_with_tears_of_joy',
			'unicode': '0x1f602', 
			'sentiment_score': 0.221, 
			'explanation': 'face with tears of joy', 
			'unicode_block': 'emoticons'
		}
		:return: 
		"""
		self.polarity = data['polarity']
		self.unicode_name = data['unicode_name']
		self.unicode = data['emoji']
		self.sentiment_score = data['sentiment_score']
		self.explanation = data['explanation']
		self.unicode_block = data['unicode_block']

class EmojiEmotion(object):

	"""
	Construction and analysis of Emoji Sentiment Ranking is described in the following paper:
	Sentiment of Emojis, PLoS ONE 10(12): e0144296, doi:10.1371/journal.pone.0144296, 2015.
	P. Kralj Novak, J. Smailovic, B. Sluban, I. Mozetic,
	"""

	def __init__(self):
		self.emojis = dict()
		self.url_ranking = 'http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html'

	def extract_emojis(self, text):
		"""
		:param text example: i'm very happy 😘 ♥
		:return:
			{
				'😘': 'face_blowing_a_kiss',
				'♥': 'heart_suit'
			}
		"""

		text = emoji.demojize(text)

		pattern = r'(:[^:]*:)'
		emoji_matches = [m.group() for m in re.finditer(pattern, text)]

		self.emojis = {k: emoji.demojize(k).replace(":", "") for k in emoji_matches}
		return self.emojis

	def demoji_span(self, text):

		"""
		Span using unicode_name
		:param text:
		:return:
		"""

		text = emoji.demojize(text)
		pattern = r'(:[^:]*:)'
		span = [[m.start(), m.end()] for m in re.finditer(pattern, text)]
		return span

	def has_emoji_text(self, text):
		has_emoji = bool(emoji.get_emoji_regexp().search(text))
		return has_emoji

	def remove_emoji(self, text):
		e = emoji.get_emoji_regexp()
		new_text = re.sub(e, r"", text)
		return new_text

	def demojize_text(self, text):
		text = emoji.demojize(text)
		return text

	def _parse_emoji_sentiment_ranking(self):

		"""
		Parsing Emoji Sentiment ranking page
		:return:
		"""

		page = requests.get(self.url_ranking)
		soup = BeautifulSoup(page.content, 'html.parser')

		table = soup.find('table')
		table_body = table.find('tbody')
		table_rows = table_body.find_all('tr')

		ranking_rows = list()
		for row in table_rows:
			cols = row.find_all('td')
			new_cols = list()
			for ele in cols:
				element = ele.text.strip()
				new_cols.append(element)

			ranking_rows.append([ele for ele in new_cols if ele])

		new_rankin_rows = list()
		for row in ranking_rows:
			del row[4:8]
			del row[0]
			del row[2]
			new_rankin_rows.append(row)
		return new_rankin_rows

	def _create_emoji_ranking_data(self):

		ranking_rows = self._parse_emoji_sentiment_ranking()

		new_ranking_rows = list()
		for row in ranking_rows:
			emoji_dict = dict()
			emo = row[0]
			unicode = row[1]
			sentiment_score = float(row[2])

			if sentiment_score > 0:
				emoji_dict['polarity'] = 'positive'
			elif sentiment_score < 0:
				emoji_dict['polarity'] = 'negative'
			elif sentiment_score == 0:
				emoji_dict['polarity'] = 'neutral'

			explanation = row[3]
			block = row[4]

			emoji_dict['emoji'] = emo
			emoji_dict['unicode_name'] = emoji.demojize(emo).replace(":", "")
			emoji_dict['unicode'] = unicode
			emoji_dict['sentiment_score'] = sentiment_score
			emoji_dict['explanation'] = explanation.lower()
			emoji_dict['unicode_block'] = block.lower()
			new_ranking_rows.append(emoji_dict)

		return new_ranking_rows

	def save_emoji_ranking(self):
		data = self._create_emoji_ranking_data()
		with open('emojis.json', 'w') as write_file:
			json.dump(data, write_file)

	def read_emoji_ranking(self):
		with open('emojis.json', "r") as read_file:
			data = json.load(read_file)
			return data

	def extract_emoji_sentiment(self, text):

		data = self.read_emoji_ranking()
		emojis = self.extract_emojis(text)
		demojis_span = self.demoji_span(text)
		demojize_text = emoji.demojize(text)

		emojis_sentiment = list()
		for key, value in emojis.items():
			for row in data:
				e = EmojiModel(row)
				if value == e.unicode_name:
					score = e.sentiment_score
					emoji_data = {
								"emoji": emoji.emojize(key),
								"unicode_name": value,
								"sentiment_score": score,
								"polarity": e.polarity,
						}
					emojis_sentiment.append(emoji_data)

		results = {
			"text": text,
			"demojize_text": demojize_text,
			"emojis": emojis_sentiment,
			"demojize_span": demojis_span
		}

		return results


















