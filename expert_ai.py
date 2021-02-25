import os
from expertai.nlapi.cloud.client import ExpertAiClient
from params import expertai_pass, expertai_username

os.environ["EAI_USERNAME"] = expertai_username
os.environ["EAI_PASSWORD"] = expertai_pass

class ExpertAI(object):

	def __init__(self, language):
		self._client = ExpertAiClient()
		self._language = language

	def _resource_analysis(self, text: str, resource="sentiment"):

		body = {
			"document":
				{
					"text": text
				}
		}

		params = {
			'language': self._language,
			'resource': resource
		}

		self.document = self._client.specific_resource_analysis(body=body, params=params)
		return self.document

	def overall_sentiment_score(self, text: str):

		"""
		Overall sentiment score

		:param text:
		:return:
		"""

		document = self._resource_analysis(text)

		lemmas = list()
		nested_lemmas = list()
		grouped_lemmas = {
			"lemmas": nested_lemmas
		}

		for item in self.document.sentiment.items:
			if not item.lemma:
				grouped_lemmas['branch_sentiment'] = item.sentiment
				for nested in item.items:
					lemma = dict()
					lemma['lemma'] = nested.lemma
					lemma['syncon'] = nested.syncon
					lemma['sentiment'] = nested.sentiment
					nested_lemmas.append(lemma)
			else:
				lemma = dict()
				lemma['lemma'] = item.lemma
				lemma['syncon'] = item.syncon
				lemma['sentiment'] = item.sentiment
				lemmas.append(lemma)

		result = dict()
		result['lemmas'] = lemmas
		result['grouped_lemmas'] = grouped_lemmas
		result['overall'] = document.sentiment.overall
		return result

	def main_sentences(self, text):

		"""
		Key elements are obtained with the relevants analysis
		and identified from the document as main sentences

		:param text:
		:return:
		"""
		document = self._resource_analysis(text, resource="relevants")

		sentences = list()
		for sentence in document.main_sentences:
			result = dict()
			result['value'] = sentence.value
			result['score'] = sentence.score
			sentences.append(result)
		return sentences


