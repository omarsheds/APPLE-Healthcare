import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns



dataset=pd.read_csv('C:/Users/Dr. Ahmad Yousry/Documents/framingham.csv')
dataset.head(5)


x = dataset[dataset.TenYearCHD == 1]
dataset=dataset.append(x)

#print("Old data frame length:", len(dataset))
dataset=dataset.dropna(axis = 0, how ='any') 

#print("New data frame length:",  
#      len(dataset)) 



from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x = dataset.drop(['TenYearCHD'], axis = 1)
y=dataset.TenYearCHD.values
dataset.TenYearCHD.value_counts()
#y.value_counts()
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

from sklearn.svm import SVC
#classifier = RandomForestClassifier(n_estimators=100, criterion='gini')
#classifier = RandomForestClassifier(n_estimators=20, criterion='entropy')
#classifier = SVC()
#classifier.fit(x_train, y_train)
#y_pred_RF = classifier.predict(x_test)
#n = classifier.predict([[1,	39,	4.0,0	,0.0	,0.0,	0	,0	,0	,195.0	,106.0	,70.0,	26.97	,80.0 , 77],[0	,37	,2.0	,1	,5.0,	0.0,	0,	0,	0	,185.0	,100.0	,68.0	,18.38	,70.0,72.0],	[1	,36	,4.0,	0,	0.0,	0.0,	0,	0,	0,	210.0,	112.0,	85.5,	21.93,	71.0	,77.0]])
#print (n)
from sklearn.metrics import confusion_matrix
#
#
##
from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
kfold = model_selection.KFold(n_splits=10, random_state=7)
cart = DecisionTreeClassifier(criterion='gini', splitter='random')
num_trees = 100
classifier = BaggingClassifier(base_estimator=cart, n_estimators=num_trees, random_state=7)
results = model_selection.cross_val_score(classifier, x_test, y_test, cv=kfold)
classifier.fit(x_train, y_train)
#y_pred_RF = model.predict(x_test)
#s=classifier.predict([[1,46,1.0,1,15.0,0.0,0,1,0,294.0,142.0,94.0,26.31,98.0,64.0],[1, 48,1.0,1,20.0,0.0,0,0,0,245.0,127.5,80.0,25.34,75.0,70.0],[0,41,3.0,0,0.0,1.0,0,1,0,332.0,124.0,88.0,31.31,65.0,84.0]])
##s= model.predict(x_test)
###
#print(s)
##
##print(results.mean())
##
##
##
##
#print("Random Forest Confusion Matrix")
#cm = confusion_matrix(y_test, y_pred_RF)
#
#print(cm)
#from sklearn.metrics import accuracy_score
#ac=accuracy_score(y_test, y_pred_RF.round())
#print('accuracy of Random Forest: ',ac)
##
#from sklearn.metrics import f1_score
#f1 = f1_score(y_test, y_pred_RF)
#print('f1 of Random Forest: ',f1)
#
#from sklearn.metrics import precision_score
#pre = precision_score(y_test, y_pred_RF)
#print('Precision of Random Forest: ',pre)
#
#from sklearn.metrics import recall_score
#reco = recall_score(y_test, y_pred_RF)
#print('recall of Random Forest: ',reco)
