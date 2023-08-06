import numpy as np
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel,euclidean_distances
from sklearn.decomposition import KernelPCA



"""# Otras Funciones"""

def GM_score(_ytrue,_ypredict):
  """
  Calcula la metrica gm score descrita en (Basgal,2021) [FDR2-BD]
  _ytrue : es un vector de las etiquetas verdaderas 
  _ypredict : es un vector de etiquetas estimadas por algun clasificador 
  """
  if len(np.unique(_ytrue))==2:
    tn, fp, fn, tp = confusion_matrix(_ytrue, _ypredict).ravel()
    tpr = tp/(tp+fn)
    tnr = tn/(fp+tn)
    return np.sqrt(tpr*tnr)
  else:
    return 0

def redondeo_particiones(_rdd,tamano_particion):
  if int(len(_rdd)/tamano_particion)>0 :
    return int(len(_rdd)/tamano_particion)
  else:
    return 1

def distancia_kernel_polynomial(X,Y,gamma):
  """
  X = Matriz de n x p
  Y = Matriz de n x p o m x p 
  La funcion retorna una matriz de distancias usando funciones kernel, mas especificamente 
  el kernel polynomial
  Si X == Y:
    Retorna una matriz de nxn
  Si X != Y:
    Retorna una matriz de n x (m-n)
  """
  if X.shape[0]!=Y.shape[0]:
    X_prima=np.append(X,Y,axis=0)
    K = polynomial_kernel(X_prima,X_prima,degree=gamma,gamma=1)
    t=np.diag(K).reshape(-1,1)@(np.repeat(1,len(K)).reshape(1,-1))
    return (t+t.T-2*K)[:len(X),len(X):]
  else:
    K = polynomial_kernel(X,Y,degree=gamma,gamma=1)
    t=np.diag(K).reshape(-1,1)@(np.repeat(1,len(K)).reshape(1,-1))
    return (t+t.T-2*K)

def distancia_kernel_rbf(X,Y,gamma):  
  """
  X = Matriz de n x p
  Y = Matriz de n x p o m x p 
  La funcion retorna una matriz de distancias usando funciones kernel, mas especificamente 
  el kernel gaussiano o rbf
  Si X == Y:
    Retorna una matriz de nxn
  Si X != Y:
    Retorna una matriz de n x m
  """

  if X.shape[0]!=Y.shape[0]:
    X_prima=np.append(X,Y,axis=0)
    K = rbf_kernel(X_prima,X_prima,gamma=gamma)
    t=np.diag(K).reshape(-1,1)@(np.repeat(1,len(K)).reshape(1,-1))
    return (t+t.T-2*K)[:len(X),len(X):]
  else:
    K = rbf_kernel(X,Y,gamma=gamma)
    t=np.diag(K).reshape(-1,1)@(np.repeat(1,len(K)).reshape(1,-1))
    return (t+t.T-2*K)





























def FCNN(X_datos,y_etiquetas):
  """
  Funcion FCNN, tiene como objetivo reducir el numero de instancias para
  entrenar un clasificador, bajo la idea de tener una perdida minima en el
  rendimiento del mismo
  -Entrada-
  X: Matriz de nxp tal que n es el numero de observaciones y p el numero de
  caracteristicas
  y: Vector de etiquetas de longitud n correspondiente a cada una de las
  observaciones de X.
  -Salida-
  Retorna un subconjunto consistente reducido S = [S(X),s(y)] en forma de
  Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce
  como labeled point, la etiqueta se retorna en la ultima columna.
  """
              #Por defecto utilizaremos el parametro k=1, pero puede ser modificado
  parametro_k=1
  k = parametro_k
              #Escalamos los datos de la matriz X
  datosTrain = X_datos
  #Nota: Si no se desea escalar para este momento, simplemente #datosTrain = X#
  clasesTrain = y_etiquetas

  nClases = 0 #Contar el numero de clases diferentes que tenemos
  for i in range(len(clasesTrain)):
    if clasesTrain[i]>nClases:
      nClases = clasesTrain[i];
  nClases+=1

              #Inicializar el vector nearest como -1's
  nearest = np.random.randint(1, size=(len(datosTrain),k))-1

              #Inicializamos al conjunto S como un conjunto vacio
              # y tamS es un contador del nunero de elementos en S
  MAX_VALUE= 1000000000
  S = np.random.randint(1, size=(len(datosTrain)))+MAX_VALUE
  tamS = 0

              #Inicializamos a dS como las observaciones mas cercanas
              #a los centroides
  deltaS = []
  for i in range(int(nClases)):
    nCentroid = 0;
    centroid = np.zeros(len(datosTrain[0]))
    for j in range(len(datosTrain)):
      if clasesTrain[j]==i:
        for l in range(len(datosTrain[j])):
          centroid[l] += datosTrain[j][l];
        nCentroid+=1;
    for j in range(len(centroid)):
      centroid[j] /= nCentroid
    pos = -1;
    minDist = MAX_VALUE
    for j in range(len(datosTrain)):
      if (clasesTrain[j]==i):
          dist = np.linalg.norm(centroid-datosTrain[j])
          if dist<minDist:
            minDist = dist
            pos = j
    if (pos>=0):
      deltaS.append(pos)

              #Validacion de numero de clases diferentes
  if (nClases < 2):
      print("Todos los datos pertenecen a una unica clase");
      nClases = 1;
      return np.append(X_datos[int(deltaS[0]):int(deltaS[0]+1)],np.array(y_etiquetas[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)

            #Una vez inicializado deltaS, procedemos a buscar en cada iteración
            #los elementos de los vectores nearest y rep
  while (len(deltaS)>0):
    for i in range(len(deltaS)):
      S[tamS] = deltaS[i]
      tamS+=1
    S = np.sort(S)
    rep = np.random.randint(1, size=len(datosTrain))-1
    for i in range(len(datosTrain)):
      if not(i in S):
        for j in range(len(deltaS)):
          insert = False
          for l in (l for l in range(len(nearest[i])) if not insert):
            if nearest[i][l]<0:
              nearest[i][l] = deltaS[j]
              insert = True
            else:
              if (np.linalg.norm(datosTrain[nearest[i][l]]-datosTrain[i]) >=  np.linalg.norm(datosTrain[deltaS[j]] - datosTrain[i] )):
                for m in range(k-1,l,-1):
                  nearest[i][m] = nearest[i][m-1]
                nearest[i][l] = deltaS[j]
                insert = True
        votes = np.random.randint(1, size=int(nClases))
        for j in range(len(nearest[i])):
          if nearest[i][j] >= 0:
            votes[ int(clasesTrain[nearest[i][j]]) ] += 1
        max=votes[0]
        pos=0
        for j in range(0,len(votes)):
          if votes[j]>max:
            max = votes[j]
            pos = j
        if clasesTrain[i] != pos:
          for j in range(len(nearest[i])):
            if nearest[i][j] >=0:
              if rep[nearest[i][j]]<0:
                rep[nearest[i][j]]=i
              else:
                if (np.linalg.linalg.norm(datosTrain[nearest[i][j]]-datosTrain[i]) <= np.linalg.linalg.norm(datosTrain[nearest[i][j]] - datosTrain[rep[nearest[i][j]] ])):
                  rep[nearest[i][j]] = i

              #Una vez finalizado el calculo de elementos en T respecto a cada
              #elemento del conjunto S, los candidatos en rep son examinados
              #tal que se agregan a delta S si el i'esimo elemento en rep fue declarado
              #y si ademas dicho elemento aun no ha sido nombrado como candidato por
              #otra observación [evitando de esta manera agregar a dicho candidato 2 veces]
    deltaS = []
    for i in range(tamS): #(rep[S[i]] in S)==False
      if (rep[S[i]]>=0 and not( rep[S[i]] in deltaS) ) :
        deltaS.append(rep[S[i]])
              #A partir de los indices almacenados en el vector S, y considerando
              #ademas la longitud del mismo, aquellas observaciones en S, se recopilan
              #tal que podamos obtener el conjunto de etiquetas S final.
  y_final = []
  X_final = []
  datosTrain
  for j in range(tamS):
    y_final.append(clasesTrain[int(S[j]) ])
    X_final.append(datosTrain[int(S[j])])
  return np.append(X_final,np.array(y_final).reshape(-1,1),axis=1)








































































def KFCNN(X_datos,y_etiquetas,parametro_gamma=0.001):  
  """
  Funcion KFCNN, tiene como objetivo reducir el numero de instancias considerando
  la distancia euclideana en un espacio de caracteristicas donde dichos datos
  sean linealmente separables, lo anterior se hace para posteriormente
  entrenar un clasificador, bajo la idea de tener una perdida minima en el 
  rendimiento del mismo
  -Entrada- 
  X: Matriz de nxp tal que n es el numero de observaciones y p el numero de 
  caracteristicas
  y: Vector de etiquetas de longitud n correspondiente a cada una de las 
  observaciones de X.
  Parametro_gamma: corresponde al parametro que utiliza la función kernel rbf 
  su rango es (0,+ inf )
  -Salida- 
  Retorna un subconjunto consistente reducido S = [S(X),s(y)] en forma de 
  Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce 
  como labeled point, la etiqueta se retorna en la ultima columna.
  """
              #Por defecto utilizaremos el parametro k=1, pero puede ser modificado
  parametro_k=1
  k = parametro_k
              #Realizamos el calculo de las distancias en el espacio kernel
              #Nota: Si no se desea escalar para este momento, simplemente 
              ##K = rbf_kernel(X,gamma=parametro_gamma)
  K = rbf_kernel(X_datos,gamma=parametro_gamma)
  t=np.diag(K).reshape(-1,1)@(np.repeat(1,len(K)).reshape(1,-1))
  dXij = (t+t.T-2*K)
              #dXij, es la matriz utilizada para hacer las comparaciones mas adelante
  
  datosTrain = X_datos
  clasesTrain = y_etiquetas

  nClases = 0 #Contar el numero de clases diferentes que tenemos 
  for i in range(len(clasesTrain)):
    if clasesTrain[i]>nClases:
      nClases = clasesTrain[i];
  nClases+=1

              #Inicializar el vector nearest como -1's
  nearest = np.random.randint(1, size=(len(datosTrain),k))-1


              #Inicializamos al conjunto S como un conjunto vacio
              # y tamS es un contador del nunero de elementos en S
  MAX_VALUE= 1000000000 
  S = np.random.randint(1, size=(len(datosTrain)))+MAX_VALUE
  tamS = 0

              #Inicializamos a dS como las observaciones mas cercanas 
              #a los centroides
  deltaS = []
  for i in range(int(nClases)):
    nCentroid = 0;
    centroid = np.zeros(len(datosTrain[0]))
    for j in range(len(datosTrain)):
      if clasesTrain[j]==i: 
        for l in range(len(datosTrain[j])):
          centroid[l] += datosTrain[j][l];
        nCentroid+=1;
    for j in range(len(centroid)):
      centroid[j] /= nCentroid
    pos = -1;
    minDist = MAX_VALUE
    for j in range(len(datosTrain)):
      if (clasesTrain[j]==i):
          dist = np.linalg.norm(centroid-datosTrain[j])
          if dist<minDist:
            minDist = dist
            pos = j
    if (pos>=0):
      deltaS.append(pos)


              #Validacion de numero de clases diferentes
  if (nClases < 2):
      print("Todos los datos pertenecen a una unica clase");
      nClases = 1;      
      return np.append(X[int(deltaS[0]):int(deltaS[0]+1)],np.array(y[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)


            #Una vez inicializado deltaS, procedemos a buscar en cada iteración
            #los elementos de los vectores nearest y rep
  while (len(deltaS)>0):
    for i in range(len(deltaS)):
      S[tamS] = deltaS[i]
      tamS+=1
    S = np.sort(S)  
    rep = np.random.randint(1, size=(len(datosTrain)))-1
    for i in range(len(datosTrain)):
      if not(i in S):
        for j in range(len(deltaS)):
          insert = False
          for l in (l for l in range(len(nearest[i])) if not insert):
            if nearest[i][l]<0:
              nearest[i][l] = deltaS[j]
              insert = True
            else:
            #Linea que es sustituida respecto al codigo original
              if dXij[nearest[i][l],i] >= dXij[deltaS[j],i]:
                for m in range(k-1,l,-1): 
                  nearest[i][m] = nearest[i][m-1]
                nearest[i][l] = deltaS[j]
                insert = True

        votes = np.random.randint(1, size=int(nClases))
        for j in range(len(nearest[i])):
          if nearest[i][j] >= 0:
            votes[int(clasesTrain[nearest[i][j]])]+=1
        max=votes[0]
        pos=0
        for j in range(0,len(votes)):
          if votes[j]>max:
            max = votes[j]
            pos = j
        if clasesTrain[i] != pos:
          for j in range(len(nearest[i])):
            if nearest[i][j] >=0:
              if rep[nearest[i][j]]<0:
                rep[nearest[i][j]]=i
              else:
                #Cambio respecto al codigo original
                if dXij[nearest[i][j], i] <= dXij[nearest[i][j],rep[nearest[i][j]]]:
                  rep[nearest[i][j]] = i

              #Una vez finalizado el calculo de elementos en T respecto a cada 
              #elemento del conjunto S, los candidatos en rep son examinados
              #tal que se agregan a delta S si el i'esimo elemento en rep fue declarado
              #y si ademas dicho elemento aun no ha sido nombrado como candidato por
              #otra observación [evitando de esta manera agregar a dicho candidato 2 veces]
    deltaS = []
    for i in range(tamS): #(rep[S[i]] in S)==False
      if (rep[S[i]]>=0 and not( rep[S[i]] in deltaS) ) :
        deltaS.append(rep[S[i]])
              #A partir de los indices almacenados en el vector S, y considerando 
              #ademas la longitud del mismo, aquellas observaciones en S, se recopilan 
              #tal que podamos obtener el conjunto de etiquetas S final.
  y_final = []
  X_final = []
  for j in range(tamS):
    y_final.append(clasesTrain[S[j]])
    X_final.append(datosTrain[S[j]])
  return np.append(X_final,np.array(y_final).reshape(-1,1),axis=1)

























































def KPCAFCNN(X_datos,y_etiquetas,parametro_gamma=0.001):
  """
  Funcion KPCAFCNN, tiene como objetivo reducir el numero de instancias considerando
  la distancia euclideana en un espacio de caracteristicas donde dichos datos
  sean linealmente separables. 
  A diferencia de KFCNN, la idea primero es reducir la dimensionalidad no lineal 
  mediante el uso de la matriz de gram, para posteriormente calcular la distancia
  de las observaciones y llevar a cabo FCNN de manera normal.
  -Entrada- 
  X: Matriz de nxp tal que n es el numero de observaciones y p el numero de 
  caracteristicas
  y: Vector de etiquetas de longitud n correspondiente a cada una de las 
  observaciones de X.
  Parametro_gamma: corresponde al parametro que utiliza la función kernel rbf 
  su rango es (0,+ inf )
  -Salida- 
  Retorna un subconjunto consistente reducido S = [S(X),s(y)] en forma de 
  Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce 
  como labeled point, la etiqueta se retorna en la ultima columna.
  """
              #Por defecto utilizaremos el parametro k=1, pero puede ser modificado
  parametro_k=1
  k = parametro_k
  #No se realiza un escalamiento interno
  #############KPCA
  transformer = KernelPCA(kernel='rbf',n_components=10,gamma=parametro_gamma)
  datosTrain = transformer.fit_transform(X_datos)
  clasesTrain = y_etiquetas

  nClases = 0 #Contar el numero de clases diferentes que tenemos 
  for i in range(len(clasesTrain)):
    if clasesTrain[i]>nClases:
      nClases = clasesTrain[i];
  nClases+=1

              #Inicializar el vector nearest como -1's
  nearest = np.random.randint(1, size=(len(datosTrain),k))-1

              #Inicializamos al conjunto S como un conjunto vacio
              # y tamS es un contador del nunero de elementos en S
  MAX_VALUE= 1000000000 
  S = np.random.randint(1, size=(len(datosTrain)))+MAX_VALUE
  tamS = 0

              #Inicializamos a dS como las observaciones mas cercanas 
              #a los centroides
  deltaS = []
  for i in range(int(nClases)):
    nCentroid = 0;
    centroid = np.zeros(len(datosTrain[0]))
    for j in range(len(datosTrain)):
      if clasesTrain[j]==i: 
        for l in range(len(datosTrain[j])):
          centroid[l] += datosTrain[j][l];
        nCentroid+=1;
    for j in range(len(centroid)):
      centroid[j] /= nCentroid
    pos = -1;
    minDist = MAX_VALUE
    for j in range(len(datosTrain)):
      if (clasesTrain[j]==i):
          dist = np.linalg.norm(centroid-datosTrain[j])
          if dist<minDist:
            minDist = dist
            pos = j
    if (pos>=0):
      deltaS.append(pos)

              #Validacion de numero de clases diferentes
  if (nClases < 2):
      print("Todos los datos pertenecen a una unica clase");
      nClases = 1;      
      return np.append(X_datos[int(deltaS[0]):int(deltaS[0]+1)],np.array(y_etiquetas[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)

            #Una vez inicializado deltaS, procedemos a buscar en cada iteración
            #los elementos de los vectores nearest y rep
  while (len(deltaS)>0):
    for i in range(len(deltaS)):
      S[tamS] = deltaS[i]
      tamS+=1
    S = np.sort(S)  
    rep = np.random.randint(1, size=(len(datosTrain)))-1

    for i in range(len(datosTrain)):
      if not(i in S):
        for j in range(len(deltaS)):
          insert = False
          for l in (l for l in range(len(nearest[i])) if not insert):
            if nearest[i][l]<0:
              nearest[i][l] = deltaS[j]
              insert = True
            else:
              if (np.linalg.linalg.norm(datosTrain[nearest[i][l]]-datosTrain[i])>=np.linalg.linalg.norm(datosTrain[deltaS[j]]-datosTrain[i])):
                for m in range(k-1,l,-1): 
                  nearest[i][m] = nearest[i][m-1]
                nearest[i][l] = deltaS[j]
                insert = True

        votes = np.random.randint(1, size=int(nClases))
        for j in range(len(nearest[i])):
          if nearest[i][j] >= 0:
            votes[int(clasesTrain[nearest[i][j]])]+=1
        max=votes[0]
        pos=0
        for j in range(0,len(votes)):
          if votes[j]>max:
            max = votes[j]
            pos = j
        if clasesTrain[i] != pos:
          for j in range(len(nearest[i])):
            if nearest[i][j] >=0:
              if rep[nearest[i][j]]<0:
                rep[nearest[i][j]]=i
              else:
                if (np.linalg.linalg.norm(datosTrain[nearest[i][j]]-datosTrain[i])<=np.linalg.linalg.norm(datosTrain[nearest[i][j]]-datosTrain[rep[nearest[i][j]]])):
                  rep[nearest[i][j]] = i

              #Una vez finalizado el calculo de elementos en T respecto a cada 
              #elemento del conjunto S, los candidatos en rep son examinados
              #tal que se agregan a delta S si el i'esimo elemento en rep fue declarado
              #y si ademas dicho elemento aun no ha sido nombrado como candidato por
              #otra observación [evitando de esta manera agregar a dicho candidato 2 veces]
    deltaS = []
    for i in range(tamS): #(rep[S[i]] in S)==False
      if (rep[S[i]]>=0 and not( rep[S[i]] in deltaS) ) :
        deltaS.append(rep[S[i]])

              #A partir de los indices almacenados en el vector S, y considerando 
              #ademas la longitud del mismo, aquellas observaciones en S, se recopilan 
              #tal que podamos obtener el conjunto de etiquetas S final.
  y_final = []
  X_final = []
  for j in range(tamS):
    y_final.append(y_etiquetas[S[j]]) 
    X_final.append(X_datos[S[j]])
  return np.append(X_final,np.array(y_final).reshape(-1,1),axis=1)














def KPCAFCNN2(X_datos,y_etiquetas,parametro_gamma=0.001):  
  """
  Funcion KFCNN, tiene como objetivo reducir el numero de instancias considerando
  la distancia euclideana en un espacio de caracteristicas donde dichos datos
  sean linealmente separables, lo anterior se hace para posteriormente
  entrenar un clasificador, bajo la idea de tener una perdida minima en el 
  rendimiento del mismo
  -Entrada- 
  X: Matriz de nxp tal que n es el numero de observaciones y p el numero de 
  caracteristicas
  y: Vector de etiquetas de longitud n correspondiente a cada una de las 
  observaciones de X.
  Parametro_gamma: corresponde al parametro que utiliza la función kernel rbf 
  su rango es (0,+ inf )
  -Salida- 
  Retorna un subconjunto consistente reducido S = [S(X),s(y)] en forma de 
  Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce 
  como labeled point, la etiqueta se retorna en la ultima columna.
  """
              #Por defecto utilizaremos el parametro k=1, pero puede ser modificado
  parametro_k=1
  k = parametro_k
              #Realizamos el calculo de las distancias en el espacio kernel
              #Nota: Si no se desea escalar para este momento, simplemente 
              ##K = rbf_kernel(X,gamma=parametro_gamma)
  transformer = KernelPCA(kernel='rbf',n_components=10,gamma=parametro_gamma)
  datosTrain = transformer.fit_transform(X_datos)
  K = rbf_kernel(datosTrain,gamma=parametro_gamma)
  t=np.diag(K).reshape(-1,1)@(np.repeat(1,len(K)).reshape(1,-1))
  dXij = (t+t.T-2*K)
              #dXij, es la matriz utilizada para hacer las comparaciones mas adelante
  
  clasesTrain = y_etiquetas

  nClases = 0 #Contar el numero de clases diferentes que tenemos 
  for i in range(len(clasesTrain)):
    if clasesTrain[i]>nClases:
      nClases = clasesTrain[i];
  nClases+=1

              #Inicializar el vector nearest como -1's
  nearest = np.random.randint(1, size=(len(datosTrain),k))-1


              #Inicializamos al conjunto S como un conjunto vacio
              # y tamS es un contador del nunero de elementos en S
  MAX_VALUE= 1000000000 
  S = np.random.randint(1, size=(len(datosTrain)))+MAX_VALUE
  tamS = 0

              #Inicializamos a dS como las observaciones mas cercanas 
              #a los centroides
  deltaS = []
  for i in range(int(nClases)):
    nCentroid = 0;
    centroid = np.zeros(len(datosTrain[0]))
    for j in range(len(datosTrain)):
      if clasesTrain[j]==i: 
        for l in range(len(datosTrain[j])):
          centroid[l] += datosTrain[j][l];
        nCentroid+=1;
    for j in range(len(centroid)):
      centroid[j] /= nCentroid
    pos = -1;
    minDist = MAX_VALUE
    for j in range(len(datosTrain)):
      if (clasesTrain[j]==i):
          dist = np.linalg.norm(centroid-datosTrain[j])
          if dist<minDist:
            minDist = dist
            pos = j
    if (pos>=0):
      deltaS.append(pos)


              #Validacion de numero de clases diferentes
  if (nClases < 2):
      print("Todos los datos pertenecen a una unica clase");
      nClases = 1;      
      return np.append(X_datos[int(deltaS[0]):int(deltaS[0]+1)],np.array(y_etiquetas[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)


            #Una vez inicializado deltaS, procedemos a buscar en cada iteración
            #los elementos de los vectores nearest y rep
  while (len(deltaS)>0):
    for i in range(len(deltaS)):
      S[tamS] = deltaS[i]
      tamS+=1
    S = np.sort(S)  
    rep = np.random.randint(1, size=(len(datosTrain)))-1
    for i in range(len(datosTrain)):
      if not(i in S):
        for j in range(len(deltaS)):
          insert = False
          for l in (l for l in range(len(nearest[i])) if not insert):
            if nearest[i][l]<0:
              nearest[i][l] = deltaS[j]
              insert = True
            else:
            #Linea que es sustituida respecto al codigo original
              if dXij[nearest[i][l],i] >= dXij[deltaS[j],i]:
                for m in range(k-1,l,-1): 
                  nearest[i][m] = nearest[i][m-1]
                nearest[i][l] = deltaS[j]
                insert = True

        votes = np.random.randint(1, size=int(nClases))
        for j in range(len(nearest[i])):
          if nearest[i][j] >= 0:
            votes[int(clasesTrain[nearest[i][j]])]+=1
        max=votes[0]
        pos=0
        for j in range(0,len(votes)):
          if votes[j]>max:
            max = votes[j]
            pos = j
        if clasesTrain[i] != pos:
          for j in range(len(nearest[i])):
            if nearest[i][j] >=0:
              if rep[nearest[i][j]]<0:
                rep[nearest[i][j]]=i
              else:
                #Cambio respecto al codigo original
                if dXij[nearest[i][j], i] <= dXij[nearest[i][j],rep[nearest[i][j]]]:
                  rep[nearest[i][j]] = i

              #Una vez finalizado el calculo de elementos en T respecto a cada 
              #elemento del conjunto S, los candidatos en rep son examinados
              #tal que se agregan a delta S si el i'esimo elemento en rep fue declarado
              #y si ademas dicho elemento aun no ha sido nombrado como candidato por
              #otra observación [evitando de esta manera agregar a dicho candidato 2 veces]
    deltaS = []
    for i in range(tamS): #(rep[S[i]] in S)==False
      if (rep[S[i]]>=0 and not( rep[S[i]] in deltaS) ) :
        deltaS.append(rep[S[i]])
              #A partir de los indices almacenados en el vector S, y considerando 
              #ademas la longitud del mismo, aquellas observaciones en S, se recopilan 
              #tal que podamos obtener el conjunto de etiquetas S final.
  y_final = []
  X_final = []
  for j in range(tamS):
    y_final.append(y_etiquetas[S[j]])
    X_final.append(X_datos[S[j]])
  return np.append(X_final,np.array(y_final).reshape(-1,1),axis=1)































































def DROP3(X_datos,y_etiquetas):
  """
  Funcion DROP3, tiene como objetivo reducir el numero de instancias para 
  entrenar un clasificador, es un metodo decremental.
  -Entrada- 
  X_datos: Matriz de nxp tal que n es el numero de observaciones y p el numero de 
  caracteristicas
  y_etiquetas: Vector de etiquetas de longitud n correspondiente a cada una de las 
  observaciones de X.
  -Salida- 
  Retorna un subconjunto consistente reducido S = [S(X_datos),s(y_etiquetas)] en forma de 
  Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce 
  como labeled point, la etiqueta se retorna en la ultima columna.
  """
  parametro_k=3
  parametro_k_filtro_enn=3
  ##Validacion del numero de clases
  conteo = np.unique(y_etiquetas,return_index=True,return_counts=True)
  clase_menor = np.argmin(conteo[2])
  if len(conteo[0])>1 and conteo[2][clase_menor]<=3:
    return(np.append(X_datos[list(conteo[1])],np.array(y_etiquetas[list(conteo[1])]).reshape(-1,1),axis=1))

  k = 1
              #Escalamiento interno para realizar la selección de instancias
#  X_escalado = scaler.fit_transform(X)
  datosTrain = X_datos
  clasesTrain = y_etiquetas
  nClases = 0 #Contar el numero de clases diferentes que tenemos 
  for i in range(len(clasesTrain)):
    if clasesTrain[i]>nClases:
      nClases = clasesTrain[i];
  nClases+=1

              #Inicializar el vector nearest como -1's
  nearest = np.random.randint(1, size=(len(datosTrain),k))-1

              #Inicializamos al conjunto S como un conjunto vacio
              # y tamS es un contador del nunero de elementos en S
  MAX_VALUE= 1000000000 
#  S = np.random.randint(1, size=(len(datosTrain)))+MAX_VALUE
#  tamS = 0

              #Inicializamos a dS como las observaciones mas cercanas 
              #a los centroides
  deltaS = []
  for i in range(int(nClases)):
    nCentroid = 0;
    centroid = np.zeros(len(datosTrain[0]))
    for j in range(len(datosTrain)):
      if clasesTrain[j]==i: 
        for l in range(len(datosTrain[j])):
          centroid[l] += datosTrain[j][l];
        nCentroid+=1;
    for j in range(len(centroid)):
      centroid[j] /= nCentroid
    pos = -1;
    minDist = MAX_VALUE
    for j in range(len(datosTrain)):
      if (clasesTrain[j]==i):
          dist = np.linalg.norm(centroid-datosTrain[j])
          if dist<minDist:
            minDist = dist
            pos = j
    if (pos>=0):
      deltaS.append(pos)

              #Validacion de numero de clases diferentes
  if (nClases < 2):
      print("Una clase");
      nClases = 1;
      return np.append(X_datos[int(deltaS[0]):int(deltaS[0]+1)],np.array(y_etiquetas[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)
  ##Termina

  def knn_euclideana(xTrain, xTest, k):
      """
      Encuentra los k vecinos mas cercanos de Xtest en Xtrain
      Entrada:
      xTrain = n x p
      xTest = m x p
      k = numero de vecinos a considerar
      Salida:
      dists = distancias entre xTrain y xTest de tamaño Size of n x m
      indices = matriz de kxm con los indices correspondientes a Xtrain
      """
      distances = euclidean_distances(xTrain,xTest)
      distances[distances < 0] = 0
      indices = np.argsort(distances, 0) #get indices of sorted items
      distances = np.sort(distances,0)   #distances sorted in axis 0
      #returning the top-k closest distances.
      return indices[0:k, : ].T , distances[0:k, : ].T  #

  knn= knn_euclideana

  def knn_predictions(xTrain,yTrain,xTest,k):
      """
      Entrada
      xTrain : n x p matriz. n=renglones p=caracteristicas
      yTrain : n x 1 vector. n=renglones de etiquetas de clase
      xTest : m x p matriz. m=renglones
      k : Numero de vecinos mas cercanos
      Salida
      predictions : etiquetas predichas para los m renglones de xTest 
      distancia : euclideana, rbf and poly
      """

      indices, distances = knn_euclideana(xTrain,xTest,k)    
      yTrain = yTrain.flatten()
      rows,columns  = indices.shape
      predictions = list()
      for j in range(rows):
          temp = list()
          for i in range(columns):
              cell = indices[j][i]
              temp.append(yTrain[cell])
          predictions.append(max(temp,key=temp.count)) #this is the key function, brings the mode value
      predictions=np.array(predictions)
      return predictions

  def distancias_enemigomascercano(X_filtrado,y_filtrado):
    """
    Funcion que computa para cada instancia la instancia 
    mas cercana de etiqueta diferente a el
    """
    vecinos,distancias = knn(X_filtrado, X_filtrado, k = X_filtrado.shape[0])
    def indice_enemigo(row,yvalues=y_filtrado):
      for c,i in enumerate(row):
        if yvalues[row[0]]!=yvalues[i]:
          return(c)
          break
    indice_ene=np.apply_along_axis(indice_enemigo,1,vecinos)
    distancia_enemigo=np.zeros(len(distancias))
    for i in range(len(distancias)):
      distancia_enemigo[i]=distancias[i][indice_ene[i]]
    return distancia_enemigo

  def suponer_no_esta(T,T_label,indice,parametro_k):
    """
    La idea es calcular el numero de observaciones correctamente clasificados
    cuando la i-esima instancia no esta en el conjunto de entrenamiento
    """
    T_virt=T.copy()
    T_virt[indice]=np.repeat(1000,T.shape[1])
    pnearest_virt , dd = knn(T_virt, T, parametro_k)
    n_filtrado=X_filtrado.shape[0]
    pasociados_virt=[[] for i in range(n_filtrado)]
    return sum(T_label[pnearest[pasociados[indice]][:,1]]==T_label[pnearest_virt[pasociados[indice]][:,-1]])

  def no_esta(T,T_label,indice,parametro_k):
    T_virt=T.copy()
    T_virt[indice]=np.repeat(1000000,T.shape[1])
    #clasificador.fit(T_virt,T_label)
    #dd,pnearest_virt=clasificador.kneighbors(T)
    pnearest_virt , dd = knn(T_virt, T, parametro_k)
    n_filtrado=X_filtrado.shape[0]
    pasociados_virt=[[] for i in range(n_filtrado)]
    for i in range(n_filtrado):
      for j in pnearest[i]:
          if i!=j:
            pasociados_virt[j].append(i)  
    return T_virt,pnearest_virt,pasociados_virt


################################################################################Comienza algoritmo
  ###########Filtro ENN
  y_estimado=knn_predictions(X_datos,y_etiquetas,X_datos,parametro_k_filtro_enn)
  X_filtrado=X_datos[y_etiquetas==y_estimado]
  y_filtrado=y_etiquetas[y_etiquetas==y_estimado]
  indices_filtrado=list(range(len(y_filtrado)))
  #############Ordenar
  d=distancias_enemigomascercano(X_filtrado,y_filtrado)
  y_filtrado=y_filtrado[np.argsort(d)[::-1]]  #Primero los mas alejados, al final los puntos fronterizos
  X_filtrado=X_filtrado[np.argsort(d)[::-1]]

  T=X_filtrado
  T_label=y_filtrado

  pnearest,dd = knn(T, T, k = parametro_k)
  n_filtrado=X_filtrado.shape[0]
  pasociados=[[] for i in range(n_filtrado)]
  for i in range(n_filtrado):
    for j in pnearest[i]:
        if i!=j:
          pasociados[j].append(i)

  recolector1=[]#tqdm
  for i in (range(len(X_filtrado))):
    if len(pasociados[i])>0:
      with_=sum(y_filtrado[i]==y_filtrado[pasociados[i]])
      without_=suponer_no_esta(T=T,T_label=T_label,indice=i,parametro_k=parametro_k)  
    else:
      without_=0
      with_=30
  #  print(without_-with_>=0)
    if without_-with_>=0:
      recolector1.append(i)
      T,pnearest,pasociados=no_esta(T=T,T_label=T_label,indice=i,parametro_k=parametro_k)    
  id_select=set(range(len(X_filtrado)))-set(recolector1)
  id_select=list(id_select)
  return np.append(X_filtrado[id_select] , (y_filtrado[id_select]).reshape(-1,1),axis=1)











def KDROP3(X_datos,y_etiquetas,gamma_rbf=0.001):  
  """
  Funcion KDROP3, tiene como objetivo reducir el numero de instancias
  utilizando una distancia en el espacio de caractetisticas  
  Se considera en la primera etapa del algoritmo un filtro ENN basado en
  la distancia euclideana.
  En la segunda etapa del algoritmo se utiliza la distancia en el espacio de 
  caracteristicas
  -Entrada- 
  X: Matriz de nxp tal que n es el numero de observaciones y p el numero de 
  caracteristicas
  y: Vector de etiquetas de longitud n correspondiente a cada una de las 
  observaciones de X.
  gamma_rbf: corresponde al parametro que utiliza la función kernel rbf,
  el rango del parametro es (0,+ inf )
  """  
  parametro_k=3
  parametro_k_filtro_enn=3
  ##Validacion del numero de clases
  conteo = np.unique(y_etiquetas,return_index=True,return_counts=True)
  clase_menor = np.argmin(conteo[2])
  if len(conteo[0])>1 and conteo[2][clase_menor]<=3:
    return(np.append(X_datos[list(conteo[1])],np.array(y_etiquetas[list(conteo[1])]).reshape(-1,1),axis=1))

  k = 1
              #Escalamiento interno para realizar la selección de instancias
  datosTrain = X_datos
  clasesTrain = y_etiquetas
  nClases = 0 #Contar el numero de clases diferentes que tenemos 
  for i in range(len(clasesTrain)):
    if clasesTrain[i]>nClases:
      nClases = clasesTrain[i];
  nClases+=1

              #Inicializar el vector nearest como -1's
  nearest = np.random.randint(1, size=(len(datosTrain),k))-1

              #Inicializamos al conjunto S como un conjunto vacio
              # y tamS es un contador del nunero de elementos en S
  MAX_VALUE= 1000000000 
#  S = np.random.randint(1, size=(len(datosTrain)))+MAX_VALUE
#  tamS = 0

              #Inicializamos a dS como las observaciones mas cercanas 
              #a los centroides
  deltaS = []
  for i in range(int(nClases)):
    nCentroid = 0;
    centroid = np.zeros(len(datosTrain[0]))
    for j in range(len(datosTrain)):
      if clasesTrain[j]==i: 
        for l in range(len(datosTrain[j])):
          centroid[l] += datosTrain[j][l];
        nCentroid+=1;
    for j in range(len(centroid)):
      centroid[j] /= nCentroid
    pos = -1;
    minDist = MAX_VALUE
    for j in range(len(datosTrain)):
      if (clasesTrain[j]==i):
          dist = np.linalg.norm(centroid-datosTrain[j])
          if dist<minDist:
            minDist = dist
            pos = j
    if (pos>=0):
      deltaS.append(pos)

              #Validacion de numero de clases diferentes
  if (nClases < 2):
      print("Una clase");
      nClases = 1;
      return np.append(X_datos[int(deltaS[0]):int(deltaS[0]+1)],np.array(y_etiquetas[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)
  ##Termina validacion

  def knn_euclideana(xTrain, xTest, k):
      """
      Encuentra los k vecinos mas cercanos de Xtest en Xtrain
      Entrada:
      xTrain = n x p
      xTest = m x p
      k = numero de vecinos a considerar
      Salida:
      dists = distancias entre xTrain y xTest de tamaño Size of n x m
      indices = matriz de kxm con los indices correspondientes a Xtrain
      """
      distances = euclidean_distances(xTrain,xTest)
      distances[distances < 0] = 0
      indices = np.argsort(distances, 0) #get indices of sorted items
      distances = np.sort(distances,0)   #distances sorted in axis 0
      #returning the top-k closest distances.
      return indices[0:k, : ].T , distances[0:k, : ].T  #

  def knn_predictions_euclideana(xTrain,yTrain,xTest,k):
      """
      Entrada
      xTrain : n x p matriz. n=renglones p=caracteristicas
      yTrain : n x 1 vector. n=renglones de etiquetas de clase
      xTest : m x p matriz. m=renglones
      k : Numero de vecinos mas cercanos
      Salida
      predictions : etiquetas predichas para los m renglones de xTest 
      distancia : euclideana, rbf and poly
      """

      indices, distances = knn_euclideana(xTrain,xTest,k)    
      yTrain = yTrain.flatten()
      rows,columns  = indices.shape
      predictions = list()
      for j in range(rows):
          temp = list()
          for i in range(columns):
              cell = indices[j][i]
              temp.append(yTrain[cell])
          predictions.append(max(temp,key=temp.count)) #this is the key function, brings the mode value
      predictions=np.array(predictions)
      return predictions

  def knn_rbf(xTrain, xTest, k,gamma_rbf):
      """
      """
      distances = distancia_kernel_rbf(xTrain,xTest,gamma_rbf)
      distances[distances < 0] = 0
      indices = np.argsort(distances, 0) #get indices of sorted items
      distances = np.sort(distances,0)   #distances sorted in axis 0
      #returning the top-k closest distances.
      return indices[0:k, : ].T , distances[0:k, : ].T  #

  knn = knn_rbf

  def knn_predictions(xTrain,yTrain,xTest,k,gamma_rbf):
      """
      Entrada
      xTrain : n x p matriz. n=renglones p=caracteristicas
      yTrain : n x 1 vector. n=renglones de etiquetas de clase
      xTest : m x p matriz. m=renglones
      k : Numero de vecinos mas cercanos
      Salida
      predictions : etiquetas predichas para los m renglones de xTest 
      distancia : euclideana, rbf and poly
      """

      indices, distances = knn_rbf(xTrain,xTest,k,gamma_rbf)    
      yTrain = yTrain.flatten()
      rows,columns  = indices.shape
      predictions = list()
      for j in range(rows):
          temp = list()
          for i in range(columns):
              cell = indices[j][i]
              temp.append(yTrain[cell])
          predictions.append(max(temp,key=temp.count)) #this is the key function, brings the mode value
      predictions=np.array(predictions)
      return predictions

  def distancias_enemigomascercano(X_filtrado,y_filtrado,gamma_rbf):
    """
    Funcion que computa para cada instancia la instancia 
    mas cercana de etiqueta diferente a el
    """
    vecinos,distancias = knn_euclideana(X_filtrado, X_filtrado, k = X_filtrado.shape[0])
    def indice_enemigo(row,yvalues=y_filtrado):
      for c,i in enumerate(row):
        if yvalues[row[0]]!=yvalues[i]:
          return(c)
          break
    indice_ene=np.apply_along_axis(indice_enemigo,1,vecinos)
    distancia_enemigo=np.zeros(len(distancias))
    for i in range(len(distancias)):
      distancia_enemigo[i]=distancias[i][indice_ene[i]]
    return distancia_enemigo

  def suponer_no_esta(T,T_label,indice,parametro_k,gamma_rbf):
    """
    La idea es calcular el numero de observaciones correctamente clasificados
    cuando la i-esima instancia no esta en el conjunto de entrenamiento
    """
    T_virt=T.copy()
    T_virt[indice]=np.repeat(1000,T.shape[1])
    pnearest_virt , dd = knn(T_virt, T, parametro_k,gamma_rbf)
    n_filtrado=X_filtrado.shape[0]
    pasociados_virt=[[] for i in range(n_filtrado)]
    return sum(T_label[pnearest[pasociados[indice]][:,1]]==T_label[pnearest_virt[pasociados[indice]][:,-1]])

  def no_esta(T,T_label,indice,parametro_k,gamma_rbf):
    T_virt=T.copy()
    T_virt[indice]=np.repeat(1000000,T.shape[1])
    pnearest_virt , dd = knn(T_virt, T, parametro_k,gamma_rbf)
    n_filtrado=X_filtrado.shape[0]
    pasociados_virt=[[] for i in range(n_filtrado)]
    for i in range(n_filtrado):
      for j in pnearest[i]:
          if i!=j:
            pasociados_virt[j].append(i)  
    return T_virt,pnearest_virt,pasociados_virt


################################################################################Comienza algoritmo
  ###########Filtro ENN  
  y_estimado=knn_predictions_euclideana(X_datos,y_etiquetas,X_datos,parametro_k_filtro_enn)
  X_filtrado=X_datos[y_etiquetas==y_estimado]
  y_filtrado=y_etiquetas[y_etiquetas==y_estimado]
  indices_filtrado=list(range(len(y_filtrado)))
  #############Ordenar
  d=distancias_enemigomascercano(X_filtrado,y_filtrado,gamma_rbf=gamma_rbf)
  y_filtrado=y_filtrado[np.argsort(d)[::-1]]  #Primero los mas alejados, al final los puntos fronterizos
  X_filtrado=X_filtrado[np.argsort(d)[::-1]]
  T=X_filtrado
  T_label=y_filtrado
  pnearest,dd = knn(T, T, k = parametro_k,gamma_rbf=gamma_rbf)
  n_filtrado=X_filtrado.shape[0]
  pasociados=[[] for i in range(n_filtrado)]
  for i in range(n_filtrado):
    for j in pnearest[i]:
        if i!=j:
          pasociados[j].append(i)

  recolector1=[]#tqdm
  for i in (range(len(X_filtrado))):
    if len(pasociados[i])>0:
      with_=sum(y_filtrado[i]==y_filtrado[pasociados[i]])
      without_=suponer_no_esta(T=T,T_label=T_label,indice=i,parametro_k=parametro_k,gamma_rbf=gamma_rbf)
    else:
      without_=0
      with_=30
    if without_-with_>=0:
      recolector1.append(i)
      T,pnearest,pasociados=no_esta(T=T,T_label=T_label,indice=i,parametro_k=parametro_k,gamma_rbf=gamma_rbf)
  id_select=set(range(len(X_filtrado)))-set(recolector1)
  id_select=list(id_select)
  return np.append(X_filtrado[id_select] , (y_filtrado[id_select]).reshape(-1,1),axis=1)




































def KPCADROP3(X_datos,y_etiquetas,gamma_rbf=0.01):
  parametro_k=3
  parametro_k_filtro_enn=3
  ##Validacion del numero de clases
  conteo = np.unique(y_etiquetas,return_index=True,return_counts=True)
  clase_menor = np.argmin(conteo[2])
  if len(conteo[0])>1 and conteo[2][clase_menor]<=3:
    return(np.append(X_datos[list(conteo[1])],np.array(y_etiquetas[list(conteo[1])]).reshape(-1,1),axis=1))

  k = 1
  datosTrain = X_datos
  clasesTrain = y_etiquetas
  nClases = 0 #Contar el numero de clases diferentes que tenemos 
  for i in range(len(clasesTrain)):
    if clasesTrain[i]>nClases:
      nClases = clasesTrain[i];
  nClases+=1

              #Inicializar el vector nearest como -1's
  nearest = np.random.randint(1, size=(len(datosTrain),k))-1

              #Inicializamos al conjunto S como un conjunto vacio
              # y tamS es un contador del nunero de elementos en S
  MAX_VALUE= 1000000000 
#  S = np.random.randint(1, size=(len(datosTrain)))+MAX_VALUE
#  tamS = 0

              #Inicializamos a dS como las observaciones mas cercanas 
              #a los centroides
  deltaS = []
  for i in range(int(nClases)):
    nCentroid = 0;
    centroid = np.zeros(len(datosTrain[0]))
    for j in range(len(datosTrain)):
      if clasesTrain[j]==i: 
        for l in range(len(datosTrain[j])):
          centroid[l] += datosTrain[j][l];
        nCentroid+=1;
    for j in range(len(centroid)):
      centroid[j] /= nCentroid
    pos = -1;
    minDist = MAX_VALUE
    for j in range(len(datosTrain)):
      if (clasesTrain[j]==i):
          dist = np.linalg.norm(centroid-datosTrain[j])
          if dist<minDist:
            minDist = dist
            pos = j
    if (pos>=0):
      deltaS.append(pos)

              #Validacion de numero de clases diferentes
  if (nClases < 2):
      print("Una clase");
      nClases = 1;
      return np.append(X_datos[int(deltaS[0]):int(deltaS[0]+1)],np.array(y_etiquetas[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)
  ##Termina validacion

  def knn_euclideana(xTrain, xTest, k):
      """
      Encuentra los k vecinos mas cercanos de Xtest en Xtrain
      Entrada:
      xTrain = n x p
      xTest = m x p
      k = numero de vecinos a considerar
      Salida:
      dists = distancias entre xTrain y xTest de tamaño Size of n x m
      indices = matriz de kxm con los indices correspondientes a Xtrain
      """
      distances = euclidean_distances(xTrain,xTest)
      distances[distances < 0] = 0
      indices = np.argsort(distances, 0) #get indices of sorted items
      distances = np.sort(distances,0)   #distances sorted in axis 0
      #returning the top-k closest distances.
      return indices[0:k, : ].T , distances[0:k, : ].T  #

  knn= knn_euclideana

  def knn_predictions(xTrain,yTrain,xTest,k):
      """
      Entrada
      xTrain : n x p matriz. n=renglones p=caracteristicas
      yTrain : n x 1 vector. n=renglones de etiquetas de clase
      xTest : m x p matriz. m=renglones
      k : Numero de vecinos mas cercanos
      Salida
      predictions : etiquetas predichas para los m renglones de xTest 
      distancia : euclideana, rbf and poly
      """

      indices, distances = knn_euclideana(xTrain,xTest,k)    
      yTrain = yTrain.flatten()
      rows,columns  = indices.shape
      predictions = list()
      for j in range(rows):
          temp = list()
          for i in range(columns):
              cell = indices[j][i]
              temp.append(yTrain[cell])
          predictions.append(max(temp,key=temp.count)) #this is the key function, brings the mode value
      predictions=np.array(predictions)
      return predictions

  def distancias_enemigomascercano(X_filtrado,y_filtrado):
    """
    Funcion que computa para cada instancia la instancia 
    mas cercana de etiqueta diferente a el
    """
    vecinos,distancias = knn(X_filtrado, X_filtrado, k = X_filtrado.shape[0])
    def indice_enemigo(row,yvalues=y_filtrado):
      for c,i in enumerate(row):
        if yvalues[row[0]]!=yvalues[i]:
          return(c)
          break
    indice_ene=np.apply_along_axis(indice_enemigo,1,vecinos)
    distancia_enemigo=np.zeros(len(distancias))
    for i in range(len(distancias)):
      distancia_enemigo[i]=distancias[i][indice_ene[i]]
    return distancia_enemigo

  def suponer_no_esta(T,T_label,indice,parametro_k):
    """
    La idea es calcular el numero de observaciones correctamente clasificados
    cuando la i-esima instancia no esta en el conjunto de entrenamiento
    """
    T_virt=T.copy()
    T_virt[indice]=np.repeat(1000,T.shape[1])
    pnearest_virt , dd = knn(T_virt, T, parametro_k)
    n_filtrado=X_filtrado.shape[0]
    pasociados_virt=[[] for i in range(n_filtrado)]
    return sum(T_label[pnearest[pasociados[indice]][:,1]]==T_label[pnearest_virt[pasociados[indice]][:,-1]])

  def no_esta(T,T_label,indice,parametro_k):
    T_virt=T.copy()
    T_virt[indice]=np.repeat(10000000,T.shape[1])
    #clasificador.fit(T_virt,T_label)
    #dd,pnearest_virt=clasificador.kneighbors(T)
    pnearest_virt , dd = knn(T_virt, T, parametro_k)
    n_filtrado=X_filtrado.shape[0]
    pasociados_virt=[[] for i in range(n_filtrado)]
    for i in range(n_filtrado):
      for j in pnearest[i]:
          if i!=j:
            pasociados_virt[j].append(i)  
    return T_virt,pnearest_virt,pasociados_virt

################################################################################Comienza algoritmo
  ###########Filtro ENN
  transformador=KernelPCA(n_components=10,kernel='rbf',gamma=gamma_rbf)
  y_estimado=knn_predictions(X_datos,y_etiquetas,X_datos,parametro_k_filtro_enn)
  X_filtrado=transformador.fit_transform(X_datos[y_etiquetas==y_estimado])
  y_filtrado=y_etiquetas[y_etiquetas==y_estimado]
  indices_filtrado=list(range(len(y_filtrado)))
  #############Ordenar
  X_inicial = X_datos[y_etiquetas==y_estimado]
  y_inicial = y_etiquetas[y_etiquetas==y_estimado]
  d=distancias_enemigomascercano(X_filtrado,y_filtrado)
  y_filtrado=y_filtrado[np.argsort(d)[::-1]]  #Primero los mas alejados, al final los puntos fronterizos
  X_filtrado=X_filtrado[np.argsort(d)[::-1]]
  T=X_filtrado
  T_label=y_filtrado
  #T= KernelPCA(kernel='poly',n_components=45,gamma=0.5,degree=3).fit_transform(X_filtrado)
  #T_label=y_filtrado
  #clasificador.fit(X_filtrado,y_filtrado)
  #dd,pnearest=clasificador.kneighbors(T)
  pnearest,dd = knn(T, T, k = parametro_k)
  n_filtrado=X_filtrado.shape[0]
  pasociados=[[] for i in range(n_filtrado)]
  for i in range(n_filtrado):
    for j in pnearest[i]:
        if i!=j:
          pasociados[j].append(i)

  recolector1=[]#tqdm
  for i in (range(len(X_filtrado))):
    if len(pasociados[i])>0:
      with_=sum(y_filtrado[i]==y_filtrado[pasociados[i]])
      without_=suponer_no_esta(T=T,T_label=T_label,indice=i,parametro_k=parametro_k)  
    else:
      without_=0
      with_=30
  #  print(without_-with_>=0)
    if without_-with_>=0:
      recolector1.append(i)
      T,pnearest,pasociados=no_esta(T=T,T_label=T_label,indice=i,parametro_k=parametro_k)    
  id_select=set(range(len(X_filtrado)))-set(recolector1)
  id_select=list(id_select)
  return np.append(X_inicial[id_select] , (y_inicial[id_select]).reshape(-1,1),axis=1)