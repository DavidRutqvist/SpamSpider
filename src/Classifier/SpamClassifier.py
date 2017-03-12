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
from sklearn.externals import joblib
import numpy as np
import os.path

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
    A helper class which takes care of all underlying handling and only exposes simple high-level methods for spam classification
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__initialized = False;
        self.__pipeline = Pipeline([# The pipeline is essentially where we define the whole classifier
            ('vectorizer', CountVectorizer(ngram_range=(1,2))),#Count Vectorizer counts the number of occurrences of a "word". We use bag of words and bigram (i.e. ngram from 1 to 2)
            #('tfidf_transformer',  TfidfTransformer()),
            ('classifier', MultinomialNB()) ]);
        self.__loader = RawDataLoader();
        
    def save(self):
        '''
        Saves a fitted model to disk in order to be able to hot-start using load method later on
        '''
        if self.__initialized:# We can only save an existing model
            print "Saving model"
            joblib.dump(self.__pipeline, "model.pkl");# Joblib is the recommended saving technique when dealing with NumPy arrays
            print "Done"
        else:
            raise Exception("Not initialized");
        
    def load(self):
        '''
        Tries to load a previously fitted and saved model from disk. Will raise a warning if no model exists.
        '''
        if not self.__initialized:
            if os.path.exists("model.pkl"):# We check if the file exists first to give the user the abitility to catch the warning and initialize instead
                print "Loading model"
                self.__pipeline = joblib.load("model.pkl");
                self.__initialized = True;
                print "Done"
            else:
                raise Warning("No file found, nothing imported nor initialized");
        else:
            raise Exception("Already initialized, either load existing classifier or initialize new one not both.");
        
    def set_up(self, cross_validate = False):
        if not self.__initialized:
            # First load data to train on
            print "Loading data"
            
            for path, classification in SOURCES:
                self.__loader.add_set(path, classification);
            self.__loader.load_data();
            print "Done"
            print "Imported " + str(len(self.__loader.data)) + " emails"
            
            # We first do cross-validation on the data to obtain an accurate score
            if cross_validate:
                print "Cross-validating to determine score"
                fold = KFold(n_splits=3);# 3-fold cross validation
                scores = [];
                confusion = np.array([[0, 0], [0, 0]]);# The confusion matrix is in this case a bit more important than the accuracy
                for train, test in fold.split(self.__loader.data):
                    # Extract train and test data
                    train_X = self.__loader.data.iloc[train]['text'].values;
                    train_y = self.__loader.data.iloc[train]['class'].values;
                    
                    test_X = self.__loader.data.iloc[test]['text'].values;
                    test_y = self.__loader.data.iloc[test]['class'].values;
                    
                    self.__pipeline.fit(train_X, train_y);# Fit on the train data
                    predictions = self.__pipeline.predict(test_X);# And predict on the test data
                    
                    confusion += confusion_matrix(test_y, predictions);# This will tell in which class we got the wrong predictions
                    scores.append(f1_score(test_y, predictions, pos_label=SPAM));# Add the score so we can get the mean score, F1 score is designed for bianry classification so we use it here
                
                print "Done"
                print "Score: " + str(sum(scores) / len(scores))
                print "Confusion matrix: "
                print confusion
            
            # Then we use the whole data set as training in order to classify new incoming messages,
            # thus the accuracy calculated above is maybe not the actual accuracy but this should be even better.
            # Accuracy is mostly important during design phase of classifier, when we reach this stage are we
            # just interested in classifying new messages in an application.
            print "Training on sets"
            self.__pipeline.fit(self.__loader.data['text'].values, self.__loader.data['class'].values);
            print "Done"
            
            self.__initialized = True;
        else:
            print "Already initialized, ignoring"
        
    def is_spam(self, body):
        '''
        Classifies an e-mail body as either spam or not
        '''
        if self.__initialized:
            return (self.__pipeline.predict([body]) == [SPAM]);
        else:
            raise Exception("Classifier is not initialized")