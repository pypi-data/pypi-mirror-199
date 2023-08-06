from datos_equilibrados import *
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel,euclidean_distances
from sklearn import preprocessing

datos=datasets.load_breast_cancer()

X,y = datos['data'],datos['target']
X = preprocessing.StandardScaler().fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

S=FCNN(X_train,y_train)

##salida
##Retorna un subconjunto consistente reducido S = [S(X),s(y)] en forma de
#Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce
#como labeled point, la etiqueta se retorna en la ultima columna.

##obtener los datos
S_x, S_y = S[:,:-1] , S[:,-1] 

##cargar clasificador
clf = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto')
##ajustar clasificador
clf.fit(S_x,S_y)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print('Utilizando FCNN')
print(classification_report(y_test, y_pred))
print('\n---')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(S_x.shape[0]))
print('---')


##################################
##################################
S=KFCNN(X_train,y_train)
##obtener los datos
S_x, S_y = S[:,:-1] , S[:,-1] 
##ajustar clasificador
clf.fit(S_x,S_y)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print('Utilizando KFCNN')
print(classification_report(y_test, y_pred))
print('\n---')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(S_x.shape[0]))
print('---')


##################################
##################################
S=KPCAFCNN(X_train,y_train)
##obtener los datos
S_x, S_y = S[:,:-1] , S[:,-1] 
##ajustar clasificador
clf.fit(S_x,S_y)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print('Utilizando KPCAFCNN')
print(classification_report(y_test, y_pred))
print('\n---')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(S_x.shape[0]))
print('---')


##################################
##################################
S=KPCAFCNN2(X_train,y_train)
##obtener los datos
S_x, S_y = S[:,:-1] , S[:,-1] 
print(S_x)
print(S_y)
##ajustar clasificador
clf.fit(S_x,S_y)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print('Utilizando KPCAFCNN2')
print(classification_report(y_test, y_pred))
print('\n---')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(S_x.shape[0]))
print('---')



##ajustar clasificador
clf.fit(X_train,y_train)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print(classification_report(y_test, y_pred))
print('\n---')
print('Utilizando el conjunto T')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(X_train.shape[0]))
print('---')


#Pruebas para DROP3
S=DROP3(X_train,y_train)

##salida
##Retorna un subconjunto consistente reducido S = [S(X),s(y)] en forma de
#Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce
#como labeled point, la etiqueta se retorna en la ultima columna.

##obtener los datos
S_x, S_y = S[:,:-1] , S[:,-1] 

##cargar clasificador
clf = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto')
##ajustar clasificador
clf.fit(S_x,S_y)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print('Utilizando DROP3')
print(classification_report(y_test, y_pred))
print('\n---')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(S_x.shape[0]))
print('---')




##pruebas para kdrop3 & kpcadrop3
#Pruebas para KDROP3
S=KDROP3(X_train,y_train)

##salida

##Retorna un subconjunto consistente reducido S = [S(X),s(y)] en forma de
#Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce
#como labeled point, la etiqueta se retorna en la ultima columna.

##obtener los datos
S_x, S_y = S[:,:-1] , S[:,-1] 

##cargar clasificador
clf = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto')
##ajustar clasificador
clf.fit(S_x,S_y)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print('Utilizando KDROP3')
print(classification_report(y_test, y_pred))
print('\n---')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(S_x.shape[0]))
print('---')


#Pruebas para KPCADROP3
S=KPCADROP3(X_train,y_train)

##obtener los datos
S_x, S_y = S[:,:-1] , S[:,-1] 

##cargar clasificador
clf = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto')
##ajustar clasificador
clf.fit(S_x,S_y)
##predecir
y_pred = clf.predict(X_test)
##imprimir reporte de clasificacion
print('Utilizando KPCADROP3')
print(classification_report(y_test, y_pred))
print('\n---')
print('Se utilizaron, {} muestras para ajustar el clasificador'.format(S_x.shape[0]))
print('---')