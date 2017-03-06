'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
from Data import RawDataLoader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

HAM = 'ham'
SPAM = 'spam'

SOURCES = [
    ('../data/enron/beck-s',      HAM),
    ('../data/enron/farmer-d',    HAM),
    #('../data/enron/kaminski-v',  HAM),
    #('../data/enron/kitchen-l',   HAM),
    #('../data/enron/lokay-m',     HAM),
    #('../data/enron/williams-w3', HAM),
    #('../data/enron/BG',          SPAM),
    #('../data/enron/GP',          SPAM),
    ('../data/enron/SH',          SPAM)
]


class SpamClassifier(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.initialized = False;
        self.pipeline = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB()) ]);
        
    def set_up(self):
        if not self.initialized:
            loader = RawDataLoader();
            print "Loading data"
            
            for path, classification in SOURCES:
                loader.add_set(path, classification);
            loader.load_data();
            print "Done"
            print "Imported " + str(len(loader.data)) + " emails"
            
            print "Training on sets"
            self.pipeline.fit(loader.data['text'].values, loader.data['class'].values);
            print "Done"
            self.initialized = True;
        
    def is_spam(self, body):
        if self.initialized:
            return (self.pipeline.predict([body]) == [SPAM]);
        else:
            raise Exception("Classifier is not initialized")