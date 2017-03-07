'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
from Classifier import SpamClassifier

clf = SpamClassifier();
clf.set_up(cross_validate=True);
print clf.is_spam('Free Viagra call today!');
print clf.is_spam('I\'m going to attend the Linux users group tomorrow.');

print "DONE"

# from Data import DataSet
# from sklearn.neural_network import MLPClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.ensemble import VotingClassifier
# 
# 
# ds = DataSet();
# ds.loadSpamBase();
# print "Number of samples loaded: " + str(ds.numSamples());
# print "Splitted as number of train samples: " + str(len(ds.getTrainX())) + " and test samples: " + str(len(ds.getTestX()))
# 
# classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(32), random_state=0);
# print "Training Neural Network"
# classifier.fit(ds.getTrainX(), ds.getTrainY());
# print "Training done"
# 
# classifier2 = GaussianNB();
# print "Training Naive Bayes"
# classifier2.fit(ds.getTrainX(), ds.getTrainY());
# print "Training done"
# 
# ensembledClassifier = VotingClassifier(estimators=[('nn', classifier), ('nb', classifier2)], voting='hard');
# print "Training ensembled voting classifier"
# ensembledClassifier.fit(ds.getTrainX(), ds.getTrainY());
# print "Training done"
# 
# print "Testing"
# print "Accuracy of Neural Network: " + str(classifier.score(ds.getTestX(), ds.getTestY()))
# print "Accuracy of Naive Bayes: " + str(classifier2.score(ds.getTestX(), ds.getTestY()))
# print "Accuracy of Voting (hard): " + str(ensembledClassifier.score(ds.getTestX(), ds.getTestY()))