import pandas as pd
import numpy as np
import math
import random

from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob as tb

fw_file = "fw_10000.txt"
stop_words = pd.read_csv(fw_file)
stop_tags = ["MD","VBP","NN$","CD","POS","RB"]

test_file = "reviews.csv"
df = pd.read_csv(test_file)
cmts = df['comments']


# take samples from comments by random index number
def sample_cmts(cmts,num):
    if len(cmts) > num:
        comment = random.sample(list(cmts),num)
        return comment
    return cmts
        

# check if an item is numeric
def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
######################################################
    # The original tf-idf
def tf(word,blob):
    return blob.words.count(word)/len(blob.words)

def n_containing(word,bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word,bloblist):
    idf_score = math.log(len(bloblist)/(1+n_containing(word,bloblist)))
    word = word.strip()
    if word in stop_words.values or is_num(word):
        return math.log(len(bloblist)/100/(1+n_containing(word,bloblist)))
    return idf_score


def tfidf(word,blob,bloblist):
    return tf(word,blob) * idf(word,bloblist)

def testtf(bloblist):
    for i,blob in enumerate(bloblist):
        print("Top words in d{}".format(i+1))
        scores = {word:tfidf(word,blob,bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(),key=lambda x: x[1], reverse = True)
        for word,score in sorted_words[:3]:
            print("\tWord:{}, TF-IDF: {}".format(word,round(score, 5)))
'''
bl = []


for i in range(10):
    bl.append(tb(cmts[i].strip().lower()) )
'''

###################################################################


def stem(words):
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    stemmed = []
    for w in words:
        stemmed.append(stemmer.stem(w))
    return stemmed

df_table={}

def ngrams(num,blob):
    word_list = []
    for word in blob.words:
        word_list.append(word)
    for n in range(2,num+1):
        ng = blob.ngrams(n=n)
        for wl in ng:
            w_n = ""
            for w in wl:
                w_n += w
                w_n += " "
            w_n = w_n[:-1]
            word_list.append(w_n)
    return word_list
        
def has_stopwords(word):
    wl = word.split(' ')
    for w in wl:
        if w in stop_words.values:
            return True
    return False

def is_stopword(word):
    wl = word.split(' ')
    if len(wl) == 1 and wl[0] in stop_words.values:
        return True
    return False

def has_stoptags(word):
    tags = tb(word).tags
    for t in tags:
        if t[1] in stop_tags:
            return True
    return False
    
def ng_tf(word,doc):
    return doc.count(word)

def ngn_containing(word,doclist):
    df = sum(1 for doc in doclist if word in doc)
    df_table[word] = df
    return df


def ng_idf(word,doclist):
    d = len(doclist)
    df_word = ngn_containing(word,doclist)
    
    
    dfw = 0
    dft = 0
    theta_list = ngrams(len(word.split(' ')),tb(word))
    for t in theta_list:
        if t in df_table:
            dfw += df_table[t]
        else:
            '''
            if has_stopwords(t):
                dft = ngn_containing(t,doclist)*len(doclist)
            else:
                dft = ngn_containing(t,doclist)
                '''
            dft = ngn_containing(t,doclist)
            dfw += dft
            df_table[t] = dft
                
            
    #print(theta_list,d,df_word,dfw,(d*df_word+0.1)/(dfw*dfw+0.1))
    idf_score = math.log( (d*df_word+0.1)/(dfw*dfw) )
    return idf_score


def ng_tfidf(word,doc,doclist):
    return ng_tf(word,doc) * ng_idf(word,doclist)

avg_score_table = {}
def ng_get_avg(doclist,n):
    #doclist.append(testdoc)
    #last_index = len(doclist)
    doc_len = len(doclist)
    for doc in doclist:
        ng_list = ngrams(n,tb(doc))
        for word in ng_list:
            score = ng_tfidf(word,doc,doclist)
            if word in avg_score_table:
                avg_score_table[word] += score
            else:
                avg_score_table[word] = score
        #scores = {word:tfidf(word,doc,doclist) for word in ng_list}
    avg_score_table.update((x,y/doc_len) for x,y in avg_score_table.items()) 
    
    filtered = dict((key,value) for (key,value) in avg_score_table.items()  if (not is_stopword(key) and not is_num(key) and not has_stoptags(key)))
    sorted_words = sorted(filtered.items(),key=lambda x: x[1], reverse = True)
    '''
    for word,score in sorted_words[:200]:
            print("\tWord:{}, TF-IDF: {}".format(word,round(score, 5)))'''
    return sorted_words

# get samples by the number defined     
sam_cmts = sample_cmts(cmts,500)

test = []
# filter the NaN, delete space and transform to lower case
for i in range(0,len(sam_cmts)):
    if type(sam_cmts[i]) == float and math.isnan(sam_cmts[i]):
        continue
    test.append( sam_cmts[i].strip().lower() )
# stem the comments
test = stem(test)

# define the gram number of test set
result = ng_get_avg(test,5)

# write to file and filter single words
f = open('sorted_word','w')
for k,v in result:
    if len(k.split(' ')) > 1:
        f.write('{}: {}\n'.format(k.encode('utf-8','replace'),v))
    
f.close()

