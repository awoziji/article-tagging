from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from tagnews.senteval import police_words


def process_google_result(text):
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_entity_sentiment(document=document)

    for entity in sentiment.entities:
        clean_entity = "".join(filter(str.isalpha, entity)).lower()

        if clean_entity in police_words:

            for mention in entity.mentions:
                return mention.sentiment.score


class SentimentGoogler:
    def __init__(self):
        self.client = self.connect_to_client()
        self.polce_words = police_words

    def run(self, doc_text):
        sentiment_ = self.call_api(doc_text)
        for entity in sentiment_.entities:
            police_entity = self.is_police_entity(entity)
            if police_entity:
                return self.sentiment_from_entity(police_entity)

    def connect_to_client(self):
        return language.LanguageServiceClient()

    def sentiment_from_entity(self, entity):
        return entity.sentiment.score

    def call_api(self, doc_text):
        """
        Parameters
        ----------
        doc_text : str
            article text

        Returns
        -------
        sentiment : json
            google response call
        """
        document = types.Document(content=doc_text, type=enums.Document.Type.PLAIN_TEXT)
        sentiment = self.client.analyze_entity_sentiment(document=document)

        return sentiment

    def is_police_entity(self, entity):
        possible_responses = [
            "police",
            "officer",
            "cop",
            "officers",
            "pigs",
            "policeofficer",
        ]
        if entity in self.police_words:
            return entity
        for mention in entity.mentions:
            if pre_process_text(mention.text.content) in self.police_words:
                return entity
            return False


def pre_process_text(html_text):
    """
    Parameters
    ----------
    html_text : str
        Article text.

    Returns
    -------
    words: str
        lower case, just letters
    """
    words = "".join(filter(str.isalpha, html_text)).lower()
    return words
