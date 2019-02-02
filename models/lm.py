
import math
import numpy as np

'''
All sentences here are given as input in the form of a list, where the list starts with '<s> and
ends with '</s>'

These tags too are important for our probability count and are included in our bigram and trigram count
'''


class LanguageModel(object):
    def __init__(self, continous_text, vocabulary):
        self.continous_text = continous_text
        self.tokens = len(self.continous_text)
        self.vocabulary = vocabulary
        self.vocabulary_size = len(vocabulary)
        self.len_continous_text = len(continous_text)
        self.unigrams = []
        self.no_of_unigrams = 0
        self.unigrams_p =[]
        self.bigrams = []
        self.no_of_bigrams = 0
        self.bigrams_p = []
        self.trigrams = []
        self.no_of_trigrams = 0
        self.trigrams_p = []
        self.quadgrams = []
        self.no_of_quadgrams = 0
        self.quadgrams_p = []
        self.unigrams_count = [0]*10000
        self.bigrams_count = [0]*10000
        self.count_flag = 0

    def find_word_set(self, *args):
        count = 0
        arg_l = len(args)
        for i in xrange(self.len_continous_text-arg_l+1):
            t = 0
            while t < arg_l:
                if args[t] == self.continous_text[i+t]:
                    if t == arg_l-1:
                        count += 1
                else:
                    break
                t += 1
        return float(count)

    def unigram_count_cal(self):
        for i in xrange(self.vocabulary_size):
            count = self.find_word_set(self.vocabulary[i])
            self.unigrams_count[int(count)] += 1

    def bigram_count_cal(self):
        for i in xrange(self.vocabulary_size):
            for j in xrange(self.vocabulary_size):
                count = self.find_word_set(self.vocabulary[i], self.vocabulary[j])
                self.bigrams_count[int(count)] += 1
                
    


# n - gram models return probability, [original count of the n-gram ( denominator ) and the pseudocount] , discount

# trigram and quadgram do not have the "gt" smoothing in them yet"
# Work in progress

    def unigram_model(self, smoothing,  word):
        f =  self.find_word_set(word)
        count_before = f
        if f == 0:
            count_before = 1
        if smoothing == "add1":
            count_after = (f+1)/(self.tokens + self.vocabulary_size)*self.tokens
            return (f+1)/(self.tokens + self.vocabulary_size), [count_before, count_after], count_after/count_before
        if smoothing == "gt":
            count_after = ((f+1)*self.unigrams_count[f+1]/self.unigrams_count[f])
            return self.unigrams_count[f+1]/self.tokens, [count_before, count_after], count_after/count_before
        if smoothing == None:
            return f/self.tokens, [count_before, count_before], 1

    def bigram_model(self, smoothing, word_1, word_2):
        c1 = self.find_word_set(word_1, word_2)
        c2 = self.find_word_set(word_2)
        count_before = c1
        if c1 == 0:
            count_before = 0.00001
        if smoothing == "add1":
            count_after = (c1+1)/(c2+self.vocabulary_size)*c2
            return (c1+1)/(c2+self.vocabulary_size), [count_before, count_after], count_after/count_before
        if smoothing == "gt":
            if self.bigrams_count[int(c1+1)] == 0:
                self.bigrams_count[int(c1+1)] = 1
            count_after = ((c1+1)*self.bigrams_count[int(c1+1)]/self.bigrams_count[int(c1+1)])
            if c2 == 0:
                c2 =  0.00001
            return self.bigrams_count[int(c1+1)]/c2, [count_before, count_after], count_after/count_before
        if smoothing == None:
            if c2 == 0:
                return 0, [0,0], 0
            else:
                return c1/c2 , [c1, c1], 1

    def trigram_model(self, smoothing, word_1, word_2, word_3):
        c1 = self.find_word_set(word_1, word_2, word_3)
        c2 = self.find_word_set(word_1, word_2)
        count_before = c1
        if c1== 0:
            count_before = 0.00001
        if smoothing == "add1":
            count_after = (c1+1)/(c2+self.vocabulary_size)*c2
            return (c1+1)/(c2+self.vocabulary_size), [count_before, count_after], count_after/count_before
        if smoothing == "gt":
            print "still in the making"
        if smoothing == None:
            if c2 == 0:
                return 0, [0,0], 0
            else:
                return c1/c2 , [c1, c1], 1

    def quadgram_model(self, smoothing, word_1, word_2, word_3, word_4):
        c1 = self.find_word_set(word_1, word_2, word_3, word_4)
        c2 = self.find_word_set(word_1, word_2, word_3)
        count_before = c1
        if c1== 0:
            count_before =  0.00001
        if smoothing == "add1":
            count_after = (c1+1)/(c2+self.vocabulary_size)*c2
            return (c1+1)/(c2+self.vocabulary_size) , [count_before, count_after], count_after/count_before
        if smoothing == "gt":
            print "still in the making"
        if smoothing == None:
            if c2 == 0:
                return 0, [0,0], 0
            else:
                return c1/c2 , [c1, c1], 1

        
    def n_gram_count_all(self):
        for i in xrange(self.vocabulary_size):
            p1, c1, d = self.unigram_model(None, self.vocabulary[i])
            self.unigrams_p.append(p1)
            self.unigrams.append([self.vocabulary[i]])
            if c1[0] != 0:
                self.no_of_unigrams += 1
            for j in xrange(self.vocabulary_size):
                p2, c2, d = self.bigram_model(None, self.vocabulary[i], self.vocabulary[j])
                self.bigrams_p.append(p2)
                self.bigrams.append([self.vocabulary[i], self.vocabulary[j]])
                self.bigrams_count[int(c2[0])] += 1
                if c2[0] != 0:
                    self.no_of_bigrams += 1
                for k in xrange(self.vocabulary_size):
                    p3, c3, d = self.trigram_model(None, self.vocabulary[i], self.vocabulary[j], self.vocabulary[k])
                    self.trigrams_p.append(p3)
                    self.trigrams.append([self.vocabulary[i], self.vocabulary[j], self.vocabulary[k]])
                    if c3[0] != 0:
                        self.no_of_trigrams += 1
                    for l in xrange(self.vocabulary_size):
                        p4, c4, d = self.quadgram_model(None, self.vocabulary[i], self.vocabulary[j], self.vocabulary[k], self.vocabulary[l])
                        self.quadgrams_p.append(p4)
                        self.quadgrams.append([self.vocabulary[i], self.vocabulary[j], self.vocabulary[k], self.vocabulary[l]])
                        if c4[0] != 0:
                            self.no_of_quadgrams += 1
        
    
    def n_gram_count_exist(self):
        for i in xrange(self.vocabulary_size):
            p1, c1, d = self.unigram_model(None, self.vocabulary[i])
            self.unigrams_p.append(p1)
            self.unigrams.append([self.vocabulary[i]])
            self.no_of_unigrams += 1
        for i in xrange(self.vocabulary_size-1):
            p2, c2, d = self.bigram_model(None, self.vocabulary[i], self.vocabulary[i+1])
            self.bigrams_p.append(p2)
            self.bigrams.append([self.vocabulary[i], self.vocabulary[i+1]])
            self.bigrams_count[int(c2[0])] += 1
            self.no_of_bigrams += 1
        for i in xrange(self.vocabulary_size-2):
            p3, c3, d = self.trigram_model(None, self.vocabulary[i], self.vocabulary[i+1], self.vocabulary[i+2])
            self.trigrams_p.append(p3)
            self.trigrams.append([self.vocabulary[i], self.vocabulary[i+1], self.vocabulary[i+2]])
            self.no_of_trigrams += 1
        for i in xrange(self.vocabulary_size-3):
            p4, c4, d = self.quadgram_model(None, self.vocabulary[i], self.vocabulary[i+1], self.vocabulary[i+2], self.vocabulary[i+3])
            self.quadgrams_p.append(p4)
            self.quadgrams.append([self.vocabulary[i], self.vocabulary[i+1], self.vocabulary[i+2], self.vocabulary[i+3]])
            self.no_of_quadgrams += 1


    
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


    