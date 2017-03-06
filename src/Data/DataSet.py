'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
import zipfile
import numpy as np
import io
      
class DataSet(object):
    def __init__(self):
        '''
            Constructor, Dataset is an instance which keeps track of the dataset currently used
        '''
        self.samples = np.zeros((1, 58));#Init samples as one sample with all zeroes
        print self.samples;
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
                self.samples = np.loadtxt(data, delimiter=",");
        print "Import done"
        
    def numSamples(self):
        '''
            Return the number of samples loaded in the WHOLE dataset
        '''
        return len(self.samples);