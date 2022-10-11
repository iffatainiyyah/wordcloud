import numpy as np
from apps.home.website import euclideanDistance


# Class K-Medoids Clustering
class k_medoids:

  # Class constructor
  def __init__(self, k = 9, max_iter = 300, has_converged = False):
    self.k = k
    self.max_iter = max_iter
    self.has_converged = has_converged
    self.medoids_cost = []
  
  # Inisialisasi Medoids
  def initMedoids(self,X):
    self.medoids =[]

    # Menentukan medoid scr acak dari dataset
    indexs = np.random.randint(0, len(X)-1, self.k)
    self.medoids = X[indexs]
    
    for i in range (0, self.k):
      self.medoids_cost.append(0)
  
  # Memeriksa apakah medoids masih mengalami perpindahan atau tdk
  def isConverged(self, new_medoids):
    # param new_medoids = medoids baru yang sudah dibandingkan dengan medoid yang sudah ada
    return set([tuple(x) for x in self.medoids]) == set([tuple(x) for x in new_medoids])
  
  # Melakukan update jika ada perubahan medoids
  def updateMedoids(self, X, labels):
    self.has_converged = True

    #Menyimpan titik data pada cluster awalnya
    clusters = []

    for i in range(0, self.k):
      cluster = []
      
      for j in range(len(X)):
        if(labels[j] == i):
          cluster.append(X[j])
      clusters.append(cluster)
      

    
    # Menghitung nilai medoids baru
    new_medoids = []

    for m in range(0, self.k):
      new_medoid = self.medoids[m]
      old_medoids_cost = self.medoids_cost[m]
    #   print("Total cost :")
    #   print(old_medoids_cost)
      

      for n in range (len(clusters[m])):

        # total jarak anggota klaster baru akan dibandingkan dengan total jarak klaster lama
        cur_medoids_cost = 0
        for dpoint_index in range (len(clusters[m])):
          cur_medoids_cost += euclideanDistance(clusters[m][n], clusters[m][dpoint_index])
        
        '''
        jika total jarak baru lebih kecil dari total jarak lama,
        maka nilai titik data baru akan dijadikan sebagai titik data medoids baru dan 
        akan ditukar sehinggan total jarak lama = total jarak baru
        '''
        if cur_medoids_cost < old_medoids_cost:
          new_medoid = clusters[m][n]
          old_medoids_cost = cur_medoids_cost

      # Medoid optimal dalam klaster saat ini
      new_medoids.append(new_medoid)
      
      
    
    # Jika not converged, maka terima medoids baru
    if not self.isConverged(new_medoids):
      self.medoids = new_medoids
      self.has_converged = False
    #   print(np.array(new_medoids))
      

  # Membuat function fit untuk menemukan klaster tiap data
  def fit(self, X):
    
    self.initMedoids(X)
    print(self.medoids)
    

    for i in range(self.max_iter):
      # Labels untuk iterasi ini
      cur_labels = []

      for medoid in range (0, self.k): 
        # Ketidaksamaan/Dissimilarity nilai klaster saat ini 
        self.medoids_cost[medoid] = 0

        for k in range (len(X)):
          # Jarak dari titik data ke masing-masing medoid
          ed_list = []

          for j in range(0, self.k):
            ed_list.append(euclideanDistance(self.medoids[j], X[k]))

          
          # labels poin data merupakan medoids yang memiliki jarak yang paling minimum
          cur_labels.append(ed_list.index(min (ed_list)))

          self.medoids_cost[medoid] += min(ed_list)
          
      
      self.updateMedoids(X, cur_labels)

      if self.has_converged:
        break
    
    return np.array(self.medoids)

  # Membuat function predict untuk mendapatkan list klaster index pada data input
  def predict(self, data):
    pred = []

    for i in range (len(data)):
      # Jarak dari poin data ke setiap medoids
      ed_list = []
      
      for j in range(len(self.medoids)):
        ed_list.append(euclideanDistance(self.medoids[j], data[i] ))

      pred.append(ed_list.index(min(ed_list)))
    
    return np.array(pred)