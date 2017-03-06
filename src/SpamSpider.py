'''
Created on 6 Mar 2017

@author: david.rutqvist
'''

from Data import DataSet
from sklearn.neural_network import MLPClassifier
import numpy as np


ds = DataSet();
ds.loadSpamBase();
print "Number of samples loaded: " + str(ds.numSamples());
print "Splitted as number of train samples: " + str(len(ds.getTrainX())) + " and test samples: " + str(len(ds.getTestX()))

classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(50, 3), random_state=1);
print "Training Neural Network"
classifier.fit(ds.getTrainX(), ds.getTrainY());
print "Training done"

print "Starting test"
predicted = classifier.predict(ds.getTestX());
print "Done"
accuracy = np.mean(predicted == ds.getTestY());
print "Accuracy: " + str(accuracy);