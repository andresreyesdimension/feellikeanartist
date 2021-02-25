from collections import namedtuple

class EmotionValues(object):


    def _mapping_values(self):

        emotion_level = namedtuple("emotion_level", ['e_range', 'label'])
        emotion_levels = [
            emotion_level(e_range=range(0, 2), label='neutral'),
            emotion_level(e_range=range(2, 5), label='verylow'),
            emotion_level(e_range=range(5, 15), label='low'),
            emotion_level(e_range=range(15, 35), label='medium'),
            emotion_level(e_range=range(35, 75), label='high'),
            emotion_level(e_range=range(75, 100), label='veryhigh'),
        ]

        return emotion_level, emotion_levels

    def emotion_values(self, emotion_value):

        """
        :return:
                {
                   "intensity":"medium",
                   "polarity":"positive"
                }
        """

        emotion_level, emotion_levels = self._mapping_values()

        value = abs(emotion_value)
        for emotion_level in emotion_levels:
            if int(value) in emotion_level.e_range:

                if emotion_value > 0:
                    sign = "positive"
                else:
                    sign = "negative"

                prediction = dict()
                if emotion_level.label != "neutral":
                    prediction['intensity'] = emotion_level.label
                    prediction['polarity'] = sign
                else:
                    #neutral case
                    prediction['polarity'] = emotion_level.label
                    prediction['intensity'] = None
                return prediction
