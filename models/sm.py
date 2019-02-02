import math
import numpy as np

'''
All sentences here are given as input in the form of a list, where the list starts with '<s> and
ends with '</s>'

These tags too are important for our probability count and are included in our bigram and trigram count
'''


class SentenceModel(object):
    def __init__(self, continous_text, vocabulary, language_model):
        self.continous_text = continous_text
        self.vocabulary = vocabulary
        #self.language_model = language_model
        self.trainingmodel = language_model(self.continous_text, self.vocabulary)

    def sentence_prob(self, sentence, smoothing, model):
        l = 0
        if model == "unigram":
            l = 1
            for i in xrange(len(sentence)):
                p,c,d =  self.trainingmodel.unigram_model(smoothing, sentence[i])
                l *= p
        if model == "bigram":
            p,c,d = self.trainingmodel.unigram_model(smoothing, sentence[0])
            l = p
            for i in xrange(len(sentence)-1):
                p,c,d = self.trainingmodel.bigram_model(smoothing, sentence[i], sentence[i+1])
                l *= p
        if model == "trigram":
            p1, c1, d1 = self.trainingmodel.unigram_model(smoothing, sentence[0])
            p2, c2, d2 =  self.trainingmodel.bigram_model(smoothing, sentence[0], sentence[1])
            l = p1*p2
            for i in xrange(len(sentence)-2):
                p,c,d = self.trainingmodel.trigram_model(smoothing, sentence[i], sentence[i+1], sentence[i+2])
                l *= p
        if model == "quadgram":
            p1, c1, d1 = self.trainingmodel.unigram_model(smoothing, sentence[0])
            p2, c2, d2 = self.trainingmodel.bigram_model(smoothing, sentence[0], sentence[1]) 
            p3, c3, d3 = self.trainingmodel.trigram_model(smoothing, sentence[0], sentence[1], sentence[2])
            l = p1*p2*p3
            for i in xrange(len(sentence)-3):
                p,c,d = self.trainingmodel.quadgram_model(smoothing, sentence[i], sentence[i+1], sentence[i+2], sentence[i+3])
                l *= p
        if l == 0:
            l = 0.000001
        return math.log(l, 10)

    def sentence_generator(self, model, smoothing):
        if self.trainingmodel.count_flag == 0:
            self.trainingmodel.n_gram_count_exist()
            self.trainingmodel.count_flag = 1
        r = ['<s>']
        if model == "unigram" : 
            while r[-1] != '</s>' and len(r) < 10:
                t = np.random.multinomial(100, self.trainingmodel.unigrams_p, size=1)
                index = t.argmax()
                r.append(self.trainingmodel.unigrams[index])
        if model == "bigram":
            while r[-1] != '</s>' and len(r) < 10:
                p_list = []
                for i in xrange(self.trainingmodel.vocabulary_size):
                    p,c,d = self.trainingmodel.bigram_model(smoothing, r[-1],self.trainingmodel.vocabulary[i])
                    p_list.append(p)
                for i in xrange(self.trainingmodel.vocabulary_size):
                        p_list[i] = p_list[i]/sum(p_list)
                t = np.random.multinomial(100, p_list, size=1)
                index = t.argmax()
                r.append(self.trainingmodel.vocabulary[index])
        if model == "trigram":
            count = 0 
            while r[-1] != '</s>' and len(r) < 10:
                if count == 0:
                    p_list = []
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p,c,d = self.trainingmodel.bigram_model(smoothing, r[-1],self.trainingmodel.vocabulary[i])
                        p_list.append(p)
                    l = sum(p_list)
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p_list[i] = p_list[i]/l
                    t = np.random.multinomial(100, p_list, size=1)
                    index = t.argmax()
                    r.append(self.trainingmodel.vocabulary[index])
                    count += 1
                else:
                    p_list = []
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p,c,d = self.trainingmodel.trigram_model(smoothing, r[-2], r[-1], self.trainingmodel.vocabulary[i])
                        p_list.append(p)
                    l = sum(p_list)
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p_list[i] = p_list[i]/l
                    t = np.random.multinomial(100, p_list, size=1)
                    index = t.argmax()
                    r.append(self.trainingmodel.vocabulary[index])
        if model == "quadgram":
            count = 0
            while r[-1] != '</s>' and len(r) < 10:
                if count == 0:
                    p_list = []
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p,c,d = self.trainingmodel.bigram_model(smoothing, r[-1],self.trainingmodel.vocabulary[i])
                        p_list.append(p)
                    l = sum(p_list)
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p_list[i] = p_list[i]/l
                    t = np.random.multinomial(100, p_list, size=1)
                    index = t.argmax()
                    r.append(self.trainingmodel.vocabulary[index])
                    count += 1
                elif count == 1:
                    p_list = []
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p,c,d = self.trainingmodel.trigram_model(smoothing, r[-2], r[-1], self.trainingmodel.vocabulary[i])
                        p_list.append(p)
                    l = sum(p_list)
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p_list[i] = p_list[i]/l
                    t = np.random.multinomial(100, p_list, size=1)
                    index = t.argmax()
                    r.append(self.trainingmodel.vocabulary[index])
                    count += 1
                else:
                    p_list = []
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p,c,d = self.trainingmodel.quadgram_model(smoothing, r[-3], r[-2], r[-1], self.trainingmodel.vocabulary[i])
                        p_list.append(p)
                    l = sum(p_list)
                    for i in xrange(self.trainingmodel.vocabulary_size):
                        p_list[i] = p_list[i]/l
                    t = np.random.multinomial(100, p_list, size=1)
                    index = t.argmax()
                    r.append(self.trainingmodel.vocabulary[index])
                    count += 1
        return r


    def bigram_perplexity(self, sentence, smoothing):
        n = len(sentence)
        #prob, c =  trainingmodel.unigram_model(smoothing, sentence[0])
        p = 1
        for i in xrange(n-1):
            prob, c,d = self.trainingmodel.bigram_model(smoothing, sentence[i], sentence[i+1])
            if prob != 0:
                p *= prob
        return (1.0/p)**(1.0/n)

