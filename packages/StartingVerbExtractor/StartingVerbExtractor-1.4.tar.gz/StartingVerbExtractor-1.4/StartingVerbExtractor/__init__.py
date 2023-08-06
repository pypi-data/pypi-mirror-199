import nltk
import re
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def tokenize(text, url_place_holder_string='urlplaceholder'):
    """
    Tokenize the text function

    Arguments:
        text -> Text message which needs to be tokenized
    Output:
        clean_tokens -> List of tokens extracted from the provided text
    """

    # Replace all urls with an urlplaceholder string
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Extract all the urls from the provided text
    detected_urls = re.findall(url_regex, text)

    # Replace url with a url placeholder string
    for detected_url in detected_urls:
        text = text.replace(detected_url, url_place_holder_string)

    # Extract the word tokens from the provided text
    tokens = nltk.word_tokenize(text)

    # Lemmanitizer to remove inflectional and derivationally related forms of a word
    lemmatizer = nltk.WordNetLemmatizer()

    # List of clean tokens
    clean_tokens = [lemmatizer.lemmatize(w).lower().strip() for w in tokens]
    return clean_tokens


class StartingVerbExtractor:
    def __init__(self, BaseEstimator, TransformerMixin):
        """ Starting Verb Extractor class
        This class extract the starting verb of a sentence,
        creating a new feature for the ML classifier
        """

    def starting_verb(self, text):
        sentence_list = nltk.sent_tokenize(text)
        for sentence in sentence_list:
            pos_tags = nltk.pos_tag(tokenize(sentence))
            first_word, first_tag = pos_tags[0]
            if first_tag in ['VB', 'VBP'] or first_word == 'RT':
                return True
        return False

    # Given it is a tranformer we can return the self
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.starting_verb)
        return pd.DataFrame(X_tagged)
