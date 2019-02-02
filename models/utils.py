from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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

def simple_tokenizer(str_input):
    words = re.sub(r"[^A-Za-z0-9\-]", " ", str_input).lower().split()
    return words

def c_distance(self, a, b):
    if a.shape[0] == b.shape[0]:
        r = 0.
        a = np.array(csr_matrix(a).todense()).T
        b = np.array(csr_matrix(b).todense())
        for i in xrange(a.shape[0]):
            r += a[i][0]*b[i][0]
        return r/((np.linalg.norm(a)*np.linalg.norm(b)))
    else:
        print 'Dimension mismatch'