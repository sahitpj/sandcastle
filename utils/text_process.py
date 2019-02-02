from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

wlt = WordNetLemmatizer()


def remove_stopwords(data_as_words):
    stop = stopwords.words('english')
    own_stopwords = ['!', ',', '?']
    stop = stop + own_stopwords
    r = []
    for i in xrange(len(data_as_words)):
        if data_as_words[i] not in stop:
            r.append(data_as_words[i])
    return r


def process_data(data_as_words):
    data = remove_stopwords(data_as_words)
    for i in xrange(len(data)):
        data[i] = wlt.lemmatize(data[i])
    return data


def import_data(filepath):
    f = open(filepath, 'r')
    t = f.readlines()
    text = []
    words = []
    for i in xrange(len(t)):
        f = preprocess(t[i][:-1].decode('utf-8').split())
        text.append(f)
        words.extend(f)
    return text, words

def simple_tokenizer(str_input):
    words = re.sub(r"[^A-Za-z0-9\-]", " ", str_input).lower().split()
    return words



