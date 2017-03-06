'''
Created on 6 Mar 2017

@author: david.rutqvist
'''

from Data import DataSet


ds = DataSet();
ds.loadSpamBase();
print "Number of samples loaded: " + str(ds.numSamples());