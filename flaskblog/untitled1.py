import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns



dataset=pd.read_csv('C:/Users/Dr. Ahmad Yousry/Documents/framingham.csv')
dataset.head(5)


x = dataset[dataset.TenYearCHD == 1]
dataset=dataset.append(x)
#
#print("Old data frame length:", len(dataset))
dataset=dataset.dropna(axis = 0, how ='any') 
#print("New data frame length:",  
#       len(dataset)) 

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x = dataset.drop(['TenYearCHD'], axis = 1)
y = dataset.TenYearCHD.values
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

#from sklearn.ensemble import RandomForestClassifier
##classifier = RandomForestClassifier(n_estimators=100, criterion='gini')
##classifier = RandomForestClassifier(n_estimators=20, criterion='entropy')
#classifier = RandomForestClassifier(n_estimators=500, criterion='gini')

from sklearn.metrics import confusion_matrix
#
#
#
from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
seed=8
kfold = model_selection.KFold(n_splits=10, random_state=seed)
classifier= DecisionTreeClassifier(criterion='gini', splitter='random', random_state=seed)
classifier.fit(x_train, y_train)
y_pred_RF = classifier.predict(x_test)

num_trees = 300
model = BaggingClassifier(base_estimator=classifier, n_estimators=num_trees, random_state=seed)
results = model_selection.cross_val_score(model, x_train, y_train, cv=kfold)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
print(results.mean())






from sklearn.metrics import accuracy_score
ac=accuracy_score(y_test, y_pred.round())
print('accuracy : ',ac)
#
#
from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred)
print('f1 score',f1)

from sklearn.metrics import precision_score
pre = precision_score(y_test, y_pred)
print('Precision: ',pre)

from sklearn.metrics import recall_score
reco = recall_score(y_test, y_pred)
print('recall  ',reco)
