import pandas as pd
from sklearn.naive_bayes import MultinomialNB

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV # CV under param of GridSearch
from sklearn.model_selection import KFold, cross_val_score

from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC # usually for binary

from sklearn.metrics import confusion_matrix, accuracy_score

df = pd.read_csv('training.csv')

print(df.shape)

X, y = df['Example'], df['Technique']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=4)
X_train, X_validate, y_train, y_validate = train_test_split(X_train, y_train, test_size=0.1, random_state=2)

# Building the Pipelines

model = Pipeline([('vectorizer', CountVectorizer(ngram_range=(1,2))),
 ('tfidf', TfidfTransformer(use_idf=True)),
 ('clf', MultinomialNB(alpha=0.1, fit_prior=False))])

#kf = KFold(n_splits=4)
'''
parameters = {'vectorizer__ngram_range': [(1, 1),(1, 2),(2,2)],
                'tfidf__use_idf': (True, False),
                'clf__alpha': [0.1, 1.0, 10],
                'clf__fit_prior': [True, False]}
gs_clf_svm = GridSearchCV(model, parameters, n_jobs=-1, cv=5)
gs_clf_svm = gs_clf_svm.fit(X_train, y_train)
print(gs_clf_svm.best_score_)
print(gs_clf_svm.best_params_)

'''

model.fit(X_train, y_train)
pred = model.predict(X_test)
print(model.score(X_validate, y_validate))
print(accuracy_score(y_test, pred))
print(confusion_matrix(y_test, pred))

