import matplotlib.pyplot as plt
import sklearn.datasets as skdata
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

# Hay 1797 digitos representados en imagenes 8x8
numeros = skdata.load_digits()
target = numeros['target']
imagenes = numeros['images']
n_imagenes = len(target)
data = imagenes.reshape((n_imagenes, -1))
dd = target!=1
target[dd]= 0

# Vamos a hacer un split training test en la mitad
scaler = StandardScaler()
x_train, x_test, y_train, y_test = train_test_split(data, target, train_size=0.5)
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#PCA sobre todo train
covTrain = np.cov(x_train.T)
valoresTrain, vectoresTrain = np.linalg.eig(covTrain)
valoresTrain = np.real(valoresTrain)
vectoresTrain = np.real(vectoresTrain)
ii = np.argsort(-valoresTrain)
valoresTrain = valoresTrain[ii]
vectoresTrain = vectoresTrain[:,ii]

#Producto matricial entre todos los datos 
ResultadosX_train = x_train@vectoresTrain
ResultadosX_test = x_test@vectoresTrain
    
def fiteando(ResultadosX_train,ResultadosX_test,y_train,y_test,true):
    F1_train = []
    F1_test = []
    for i in range(3,40):
        clf = LinearDiscriminantAnalysis()
        clf.fit(ResultadosX_train[:,0:i],y_train)
        y_predict_train = clf.predict(ResultadosX_train[:,0:i])
        y_predict_test = clf.predict(ResultadosX_test[:,0:i])
        Formula1_train = f1_score(y_train, y_predict_train, pos_label = true)
        Formula1_test = f1_score(y_test, y_predict_test, pos_label = true)
        F1_train.append(Formula1_train)
        F1_test.append(Formula1_test)
    return F1_train,F1_test
F1_train,F1_test = fiteando(ResultadosX_train,ResultadosX_test,y_train,y_test,1)
x = range(3,40)
plt.figure(figsize=(12, 12))
plt.subplot(1,2,1)
plt.scatter(x,F1_train, label = 'train del 50%')
plt.scatter(x,F1_test,  label = 'test del 50%')
plt.legend()
plt.title('F1 Score de los unos')

F1_train,F1_test = fiteando(ResultadosX_train,ResultadosX_test,y_train,y_test,0)
plt.subplot(1,2,2)
plt.scatter(x,F1_train, label = 'train del 50%')
plt.scatter(x,F1_test,  label = 'test del 50%')
plt.legend()
plt.title('F1 Score de los otros')

plt.savefig('F1.png')