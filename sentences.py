from expert_ai import ExpertAI
from emoji_sentiment_analysis import EmojiEmotion
from emotion_values import EmotionValues


class Sentences(ExpertAI, EmojiEmotion, EmotionValues):

    def __init__(self, language):
        super().__init__(language)

    def _text_emotion_score(self, text: str):
        overall_sentiment = self.overall_sentiment_score(text)
        text_sentiment_score = overall_sentiment['overall']
        return text_sentiment_score

    def _sentences(self, text):

        emoji_founded = self.has_emoji_text(text)
        if emoji_founded is True:
            new_text = self.remove_emoji(text)
            sentences = self._get_sentences(new_text)
        else:
            sentences = self._get_sentences(text)
        return sentences

    def _get_sentences(self, text: str):

        sentences = list()
        for sentence in self.main_sentences(text):
            s = dict()
            value = sentence['value']
            text_score = self._text_emotion_score(value)
            values = self.emotion_values(text_score)
            s['text'] = value
            s['text_score'] = text_score
            s['values'] = values
            sentences.append(s)
        return sentences

    def _sentences_analysis(self, text: str):

        emoji_founded = self.has_emoji_text(text)

        analysis = dict()
        if emoji_founded is True:
            new_text = self.remove_emoji(text)
            overall_score = self._text_emotion_score(new_text)

            analysis['emoji_founded'] = True
            analysis['sentences'] = self._get_sentences(new_text)
            analysis['demoji_span'] = self.demoji_span(text)
            analysis['demoji_text'] = self.demojize_text(text)
            analysis['overall_score'] = overall_score
            analysis['values'] = self.emotion_values(overall_score)
        else:
            overall_score = self._text_emotion_score(text)

            analysis['emoji_founded'] = False
            analysis["sentences"] = self._get_sentences(text)
            analysis['demoji_span'] = list()
            analysis['demoji_text'] = list()
            analysis['overall_score'] = overall_score
            analysis['values'] = self.emotion_values(overall_score)

        return analysis

    def _partial_sentence_analysis(self, text: str):

        """
        :param text example: i'm feeling bad
        :return:
        """

        emoji_founded = self.has_emoji_text(text)

        analysis = dict()
        sentences = list()
        overall_score = float()

        if emoji_founded is True:
            analysis['emoji_founded'] = True
            analysis['demoji_span'] = self.demoji_span(text)
            analysis['demoji_text'] = self.demojize_text(text)

            new_text = self.remove_emoji(text)
            text_score = self._text_emotion_score(new_text)
            values = self.emotion_values(text_score)

            partial_sentence = {
                "text": text,
                "text_score": text_score,
                "values": values
            }
            sentences.append(partial_sentence)

            r = self.extract_emoji_sentiment(text)
            emojis = r['emojis']

            if len(emojis) > 0:
                for emoji in emojis:
                    emoji_score = abs(emoji['sentiment_score'])
                    polarity = emoji['polarity']
                    if polarity == 'positive':
                        text_score = text_score + emoji_score
                    elif polarity == 'negative':
                        text_score = text_score - emoji_score
                    overall_score = text_score
            else:
                overall_score = text_score

        else:
            #in this case overall_score and text_score is the same
            # because we don't have emojis
            overall_score = self._text_emotion_score(text)
            values = self.emotion_values(overall_score)
            partial_sentence = {
                "text": text,
                "text_score": overall_score,
                "values": values
            }
            sentences.append(partial_sentence)
            analysis['emoji_founded'] = False
            analysis['demoji_span'] = list()
            analysis['demoji_text'] = list()


        overall_score = float("{:.2f}".format(overall_score))
        values = self.emotion_values(overall_score)

        analysis['sentences'] = sentences
        analysis['overall_score'] = overall_score
        analysis['values'] = values
        return analysis

    def sentences_analysis(self, text):

        sentences = self._sentences(text)
        if len(sentences) != 0:
            full_analysis = self._sentences_analysis(text)
        else:
            full_analysis = self._partial_sentence_analysis(text)
        return full_analysis




