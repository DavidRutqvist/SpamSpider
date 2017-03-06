'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
import os
import io
from pandas import DataFrame as df
from sklearn.utils import shuffle

NEWLINE = '\n'
SKIP_FILES = {'cmds'}

class RawDataLoader(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.data = df({ 'text': [], 'class': [] });
        self.data_loaded = False;
        self.sets = [];
    
    def add_set(self, path, classification):
        '''
        Adds a set to the set collection, must be called before load_data call
        '''
        if not self.data_loaded:
            self.sets.append((path, classification));
        else:
            raise Exception("All sets must be added before loading data");
    
    def load_data(self):
        '''
        Loads the data from disk, can only be run once
        '''
        if not self.data_loaded:
            for path, classification in self.sets:
                self.data = self.data.append(self.__load_set(path, classification));
                
            self.data = self.data.reindex(shuffle(self.data.index, random_state=0));
        
    def __read_files(self, path):
        '''
        Recursively scans the folder path for raw emails to read
        '''
        for root, dirs, files in os.walk(path):
            for path in dirs:
                self.__read_files(path);#Recursively scan sub-folders
            for file_name in files:
                file_path = os.path.join(root, file_name);
                if((file_name not in SKIP_FILES) and os.path.isfile(file_path)):
                    past_header = False;
                    body = [];
                    
                    with io.open(file_path, encoding="latin-1") as f:#We use with statement to ensure proper close of file in a neat way
                        for line in f:
                            if past_header:
                                body.append(line);
                            elif line == NEWLINE:#Email standard specifies that is should be a blank line between header and body
                                past_header = True;#Start recording body
                    yield file_path, NEWLINE.join(body);
            
    def __load_set(self, path, classification):
        rows, index = [], [];
        for file_name, text in self.__read_files(path):
            rows.append({ 'text': text, 'class': classification });
            index.append(file_name);
        print "Set " + path + " loaded"
        return df(rows, index=index);
    
    