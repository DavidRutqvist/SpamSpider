'''
Created on 6 Mar 2017

@author: david.rutqvist
'''
from Classifier import SpamClassifier

clf = SpamClassifier();# Instantiate a new instance of our helper class

# Either run set_up of load not both, however if load fails then we might call set_up anyways
try:
    print "Trying to load model"
    clf.load();# Tries loading a previously fitted and saved model
except Warning:# Load throws warning if no model exists
    print "No model exists, initializing new one"
    clf.set_up(cross_validate=True);# Then we create a new one. Set_up loads data and trains the classifier. Use cross_validate to run a validation and output the accuracy
    print "Initialized, now saving model"
    clf.save();# And saves it to disk for later use
print "Classifier up and running"

# Some examples to test our classifier on arbitrary text. This method is what you should commonly use in an application.
print clf.is_spam('Free Viagra call today!');# Should be spam
print clf.is_spam('I\'m going to attend the lecture tomorrow. Are you coming?');# Should not be spam
print clf.is_spam('MICROSOFT GB CORPORATION\nCardinal Place\n80-100 Victoria Street\nLondon, SW1E 5JL, United Kingdom\n \nAttention E-mail Prize Winner,\nWe wish to congratulate you for being one of the selected E-mail On-line Winner in the 2016 MICROSOFT GB CORPORATION AWARDS, Kindly view the enclosed attachment for the MICROSOFT WINNING AWARD LETTER.\n \nThe best is yet to come, Congratulations on behalf of Staffs and Members of Microsoft GB Board Commission.\n \nRegards,\nDR. NICOLA HUDSON\nMicrosoft GB General Secretary, Public Sector\nMicrosoft GB Corporation');# Spam taken from David's inbox

print "DONE"

#----------Below is a simple implementation using Spambase dataset, (first approach). Only left as reference but works if you uncomment everything and comment everything above this line

#   
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