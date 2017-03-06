'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
import zipfile
import numpy as np
import io
import math
from sklearn.utils import shuffle
      
class DataSet(object):
    TEST_PARTITION = 0.10;#Percentage of data used as test
    
    def __init__(self):
        '''
            Constructor, Dataset is an instance which keeps track of the dataset currently used
        '''
        self.samples = np.zeros((1, 58));#Init samples as one sample with all zeroes
        self.answers = np.zeros((1, 1));#Init the true answers used during supervised learning
        return;
    
    def loadSpamBase(self):
        '''
            Loads the spambase dataset into the dataset instance
        '''
        #Unzip and read data file into matrix
        print "Importing Spambase dataset"
        #This unzips the zip file in the memory, using with statement to ensure proper close of file.
        with zipfile.ZipFile("../data/spambase.zip", "r") as archive:
            #Opens the actual data file, using read mode only so no disk access errors encounters
            with io.BufferedReader(archive.open("spambase.data", mode="r")) as data:
                #Parse file into matrix, one row for each line and columns separated by comma
                loadedData = np.loadtxt(data, delimiter=",");#The first 56 columns are the inputs, the last column is the answer
                loadedData = shuffle(loadedData, random_state=0);#The dataset is ordered such that all spam is in the beggining, this may have some severe effects on tuning, the sklearn shuffle shuffles data in a consistent way
                self.samples = loadedData[:,0:-1];#Everything except last column
                self.answers = loadedData[:,-1:].ravel();#Last column, ravel changes shape as suggested by sklearn
        print "Import done"
        
    def getTrainX(self):
        return self.samples[:self.__getSplitIndex()];
    
    def getTrainY(self):
        return self.answers[:self.__getSplitIndex()];
    
    def getTestX(self):
        return self.samples[self.__getSplitIndex():];
    
    def getTestY(self):
        return self.answers[self.__getSplitIndex():];
        
    def __getSplitIndex(self):
        num = len(self.answers);
        index = math.floor(num * (1 - self.TEST_PARTITION));
        return int(index);
        
    def numSamples(self):
        '''
            Return the number of samples loaded in the WHOLE dataset
        '''
        return len(self.samples);