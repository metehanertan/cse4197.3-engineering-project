import string
import en_core_web_sm
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from trnlp import TrnlpWord

nlp = en_core_web_sm.load()
# nltk.download('wordnet')

from textblob import TextBlob


def remove_punctuation(from_text):
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in from_text]
    return stripped


def findLemma(text):
    tokens_sentences = sent_tokenize(text)
    tokens = [[word.lower() for word in line.split()] for line in tokens_sentences]
    stripped_tokens = [remove_punctuation(i) for i in tokens]
    sw = (stopwords.words('turkish'))
    filter_set = [[token for token in sentence if (token.lower() not in sw and token.isalnum())] for sentence in
                  stripped_tokens]

    obj = TrnlpWord()
    lem = []
    for tokens in filter_set:
        sentence = []
        for token in tokens:
            obj.setword(token)
            for analiz in obj.get_inf:
                if analiz['base'] not in sentence:
                    sentence.append(analiz['base'].replace('.', ','))
        lem.append(sentence)
    return lem


def findNer(text):
    '''
    blob1 = TextBlob(text)

    try:
        blob_eng = blob1.translate(to="en")
    except:
        blob_eng = text

    textNlp = nlp(str(blob_eng))
    NER = {}
    for X in textNlp.ents:
        try:
            blob1 = TextBlob(X.text)
            blob_tr = blob1.translate(to="tr")
            NER[str(blob_tr).replace('.', ',')] = X.label_
        except:
            NER[X.text.replace('.', ',')] = X.label_
    return NER
    '''

    return ''


def sentimentAnalysis(text):
    '''
    blob1 = TextBlob(text)
    try:
        blob_eng = blob1.translate(to="en")
    except:
        blob_eng = blob1
    Sentiment = {'Polarity': int(blob_eng.sentiment[0] * 100), 'Subjectivity': int(blob_eng.sentiment[1] * 100)}
    if blob_eng.sentiment[0] < 0:
        print(blob_eng.sentiment[0], text)
    '''
    return ''
