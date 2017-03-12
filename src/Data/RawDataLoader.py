'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
import os
import io
from pandas import DataFrame as df
from sklearn.utils import shuffle

NEWLINE = '\n'# This should maybe be moved to a setting for the data sets
SKIP_FILES = {'cmds'} # This should maybe be moved to a setting for the data sets

class RawDataLoader(object):
    '''
    Helper to load raw e-mails by recursively scanning sets (i.e. folders).
    Loaded data will reside within the data property containing the e-mail
    body as 'text' and the label as 'class', i.e. spam or ham
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.data = df({ 'text': [], 'class': [] });# Set up empty DataFrame
        self.data_loaded = False;
        self.sets = [];# Initialize empty folder list
    
    def add_set(self, path, classification):
        '''
        Adds a set to the set collection, must be called before load_data call
        '''
        if not self.data_loaded:# This is just to prevent any mistakes, thus we throw an exception if calls are made in the wrong order
            self.sets.append((path, classification));
        else:
            raise Exception("All sets must be added before loading data");
    
    def load_data(self):
        '''
        Loads the data from disk, can only be run once
        '''
        if not self.data_loaded:# We only allow the data to be loaded once, this is just by design and not really any restriction
            for path, classification in self.sets:
                self.data = self.data.append(self.__load_set(path, classification));# Append each set of loaded data to the complete list of data
                
            # We shuffle the data since it is probably ordered by label in the sets and want to have an even spread of data. Random state ensures that shuffling is consistent
            self.data = self.data.reindex(shuffle(self.data.index, random_state=0));
        
    def __read_files(self, path):
        '''
        Recursively scans the folder path for raw e-mails to read
        '''
        for root, dirs, files in os.walk(path):# This basically retrieves all items in a folder from the underlying OS
            for path in dirs:
                self.__read_files(path);# Recursively scan sub-folders
            for file_name in files:
                file_path = os.path.join(root, file_name);
                if((file_name not in SKIP_FILES) and os.path.isfile(file_path)):
                    past_header = False;
                    body = [];
                    
                    with io.open(file_path, encoding="latin-1") as f:# We use with statement to ensure proper close of file in a neat way
                        # Loop line-by-line. Ignore everything until e-mail header has passed.
                        # One should maybe parse the from-address here which resides within e-mail header in order to implement black-/whitelist
                        for line in f:
                            if past_header:
                                body.append(line);
                            elif line == NEWLINE:# Email standard specifies that it should be a blank line between header and body
                                past_header = True;#Start recording body
                    yield file_path, NEWLINE.join(body);# Yield return is a neat way to get a loopable "list"-isch return without wrapping everything within a list
            
    def __load_set(self, path, classification):
        '''
        Loads a single set of raw e-mails and returns a DataFrame containing loaded e-mails
        '''
        rows, index = [], [];
        for file_name, text in self.__read_files(path):
            rows.append({ 'text': text, 'class': classification });
            index.append(file_name);
        print "Set " + path + " loaded"
        return df(rows, index=index);
    
    