from sentences import Sentences


class Emotion(Sentences):

	def __init__(self, language: str):
		super().__init__(language)

	def raw_emotion_data(self, full_text: str):

		sentences = self.sentences_analysis(full_text)
		emotion_analysis = dict()

		if sentences['emoji_founded'] is True:
			emojis_analysis = self.extract_emoji_sentiment(full_text)
			emojis = emojis_analysis['emojis']
			demojize_text = emojis_analysis['demojize_text']
			demojize_span = emojis_analysis['demojize_span']

			emotion_analysis['full_text'] = full_text
			emotion_analysis['sentences'] = sentences['sentences']
			emotion_analysis['overall_score'] = sentences['overall_score']
			emotion_analysis['values'] = sentences['values']
			emotion_analysis['emojis'] = emojis
			emotion_analysis['demojize_text'] = demojize_text
			emotion_analysis['demojize_span'] = demojize_span
		else:
			emotion_analysis['full_text'] = full_text
			emotion_analysis['sentences'] = sentences['sentences']
			emotion_analysis['overall_score'] = sentences['overall_score']
			emotion_analysis['values'] = sentences['values']
			emotion_analysis['emojis'] = list()
			emotion_analysis['demojize_text'] = list()
			emotion_analysis['demojize_span'] = list()

		return emotion_analysis






