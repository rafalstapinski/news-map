from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

import numpy as np

train = fetch_20newsgroups(subset='train', shuffle=True)
clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, tol=5, random_state=42))
])

clf = clf.fit(train.data, train.target)

test = fetch_20newsgroups(subset='test', shuffle=True)

predicted = clf.predict(test.data)

print np.mean(predicted == test.target)
