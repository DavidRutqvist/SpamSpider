'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
from Data import RawDataLoader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, f1_score
import numpy as np

HAM = 'ham'
SPAM = 'spam'

SOURCES = [
    ('../data/enron/beck-s',            HAM),
#     ('../data/enron/farmer-d',          HAM),
#     ('../data/enron/kaminski-v',        HAM),
#     ('../data/enron/kitchen-l',         HAM),
#     ('../data/enron/lokay-m',           HAM),
#     ('../data/enron/williams-w3',       HAM),
#     ('../data/enron/BG',                SPAM),
#     ('../data/enron/GP',                SPAM),
     ('../data/enron/SH',                SPAM),
#     ('../data/spamassassin/easy_ham',   HAM),
#     ('../data/spamassassin/easy_ham_2', HAM),
#     ('../data/spamassassin/hard_ham',   HAM),
#     ('../data/spamassassin/spam',       SPAM),
#     ('../data/spamassassin/spam2',      SPAM)
]


class SpamClassifier(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__initialized = False;
        self.__pipeline = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=(1,2))),
            #('tfidf_transformer',  TfidfTransformer()),
            ('classifier', MultinomialNB()) ]);
        self.__loader = RawDataLoader();
        
    def set_up(self, cross_validate = False):
        if not self.__initialized:
            print "Loading data"
            
            for path, classification in SOURCES:
                self.__loader.add_set(path, classification);
            self.__loader.load_data();
            print "Done"
            print "Imported " + str(len(self.__loader.data)) + " emails"
            
            #We first do cross-validation on the data to obtain a accurate score
            if cross_validate:
                print "Cross-validating to determine score"
                fold = KFold(n_splits=3);
                scores = [];
                confusion = np.array([[0, 0], [0, 0]]);
                for train, test in fold.split(self.__loader.data):
                    train_X = self.__loader.data.iloc[train]['text'].values;
                    train_y = self.__loader.data.iloc[train]['class'].values;
                    
                    test_X = self.__loader.data.iloc[test]['text'].values;
                    test_y = self.__loader.data.iloc[test]['class'].values;
                    
                    self.__pipeline.fit(train_X, train_y);
                    predictions = self.__pipeline.predict(test_X);
                    
                    confusion += confusion_matrix(test_y, predictions);#This will tell in which class we got the wrong predictions
                    scores.append(f1_score(test_y, predictions, pos_label=SPAM));
                
                print "Done"
                print "Score: " + str(sum(scores) / len(scores))
                print "Confusion matrix: "
                print confusion
            
            #Then we use the whole data set as training in order to classify new incoming messages
            print "Training on sets"
            self.__pipeline.fit(self.__loader.data['text'].values, self.__loader.data['class'].values);
            print "Done"
            
            self.__initialized = True;
        else:
            print "Already initialized, ignoring"
        
    def is_spam(self, body):
        if self.__initialized:
            return (self.__pipeline.predict([body]) == [SPAM]);
        else:
            raise Exception("Classifier is not initialized")