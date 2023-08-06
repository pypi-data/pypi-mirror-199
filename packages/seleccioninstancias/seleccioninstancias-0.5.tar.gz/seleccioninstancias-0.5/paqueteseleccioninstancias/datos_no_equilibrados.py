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
































def FCNN_NE(X_datos,y_etiquetas):
  """
  Funcion FCNN, tiene como objetivo reducir el numero de instancias para 
  entrenar un clasificador, bajo la idea de tener una perdida minima en el 
  rendimiento del mismo, para datos no equilibrados.
  La idea es inicilizar el algoritmo FCNN_MR incluyendo todas las observaciones
  de la clase minoritaria, tal que la  selección o reducción se hace sobre la clase mayoritaria
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
             #Aqui se podria escalar los datos de la matriz x, 
             #Nosotros trabajaremos con datos estandarizados
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
      return np.append(datosTrain[int(deltaS[0]):int(deltaS[0]+1)],np.array(clasesTrain[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)
      
  else:
    clase_minoritaria = np.argmin(np.unique(clasesTrain,return_counts=True)[1])
    for j in range(len(datosTrain)):
      if clase_minoritaria == clasesTrain[j] and not( j in deltaS):
        deltaS.append(j)

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































































def KFCNN_NE(X_datos,y_etiquetas,parametro_gamma=0.005):  
  """
  Funcion KFCNN, tiene como objetivo reducir el numero de instancias considerando
  la distancia euclideana en un espacio de caracteristicas donde dichos datos
  sean linealmente separables, lo anterior se hace para posteriormente
  entrenar un clasificador, bajo la idea de tener una perdida minima en el 
  rendimiento.
  La idea es inicilizar el algoritmo KFCNN incluyendo todas las observaciones
  de la clase minoritaria, tal que la  selección o reducción se hace sobre la clase mayoritaria
  -Entrada- 
  X_datos: Matriz de nxp tal que n es el numero de observaciones y_etiquetas p el numero de 
  caracteristicas
  y_etiquetas: Vector de etiquetas de longitud n correspondiente a cada una de las 
  observaciones de X_datos.
  Parametro_gamma: corresponde al parametro que utiliza la función kernel rbf 
  su rango es (0,+ inf )
  -Salida- 
  Retorna un subconjunto consistente reducido S = [S(X_datos),s(y_etiquetas)] en forma de 
  Vector de Caracteristicas - Etiquetas de Clase, lo que tambien se conoce 
  como labeled point, la etiqueta se retorna en la ultima columna.
  """
              #Por defecto utilizaremos el parametro k=1, pero puede ser modificado
  parametro_k=1
  k = parametro_k
              #Realizamos el calculo de las distancias en el espacio kernel
              #Nota: Si no se desea escalar para este momento, simplemente 
              ##K = rbf_kernel(X_datos,gamma=parametro_gamma)
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


  if (nClases < 2):
      print("Todos los datos pertenecen a una unica clase");
      nClases = 1;      
      return np.append(X_datos[int(deltaS[0]):int(deltaS[0]+1)],np.array(y_etiquetas[int(deltaS[0]):int(deltaS[0]+1)]).reshape(-1,1),axis=1)
      
  else:
    clase_minoritaria = np.argmin(np.unique(clasesTrain,return_counts=True)[1])
    for j in range(len(datosTrain)):
      if clase_minoritaria == clasesTrain[j] and not( j in deltaS):
        deltaS.append(j)

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



















































def KPCAFCNN_NE(X_datos,y_etiquetas,parametro_gamma=0.0005):
  """
  Funcion KPCAFCNN para datos no equilibrados, en ese sentido lo unico que 
  cambia es la inicialización del metodo.
  tiene como objetivo reducir el numero de instancias considerando  
  A diferencia de KFCNN, la idea primero es reducir la dimensionalidad no lineal 
  mediante el uso de la matriz de gram, para posteriormente calcular la distancia
  de las observaciones y llevar a cabo FCNN de manera normal.
  La idea es inicilizar el algoritmo KFCNN incluyendo todas las observaciones
  de la clase minoritaria, tal que la  selección o reducción se hace sobre la clase mayoritaria
  -Entrada- 
  X_datos: Matriz de nxp tal que n es el numero de observaciones y p el numero de 
  caracteristicas
  y_etiquetas: Vector de etiquetas de longitud n correspondiente a cada una de las 
  observaciones de X_datos.
  Parametro_gamma: corresponde al parametro que utiliza la función kernel rbf 
  su rango es (0,+ inf )
  -Salida- 
  Retorna un subconjunto consistente reducido S = [S(X_datos),s(y_etiquetas)] en forma de 
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
      
  else:
    clase_minoritaria = np.argmin(np.unique(clasesTrain,return_counts=True)[1])
    for j in range(len(datosTrain)):
      if clase_minoritaria == clasesTrain[j] and not( j in deltaS):
        deltaS.append(j)

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
              if (np.linalg.linalg.norm(datosTrain[nearest[i][l]]-datosTrain[i]) >= np.linalg.linalg.norm(datosTrain[deltaS[j]]-datosTrain[i])):
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