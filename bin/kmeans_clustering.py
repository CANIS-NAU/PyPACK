import numpy as np
import pandas as pd
from io import StringIO
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.interpolate import interp1d
import json
from collections import Counter
import sys

def cluster(file):
    #Declaring lists and dictionaries
    final_dict = {}
    userID_list = []
    ks_list = []
    sil_list = []
    wcss_list = []
    cluster_sizes_dict = {}
    cluster_sizes_list = []
    cluster_centroids = {}
    cluster_centroids_list = []
    
    #Creating dataframe from file
    df = pd.read_csv(file, sep='\t', names=['userID', 'Locations'])
    
    #Converts data to a list of tuples
    def parse_data(df):
        x = StringIO(df['Locations'])
        y = np.genfromtxt(x, delimiter=')', dtype= tuple)
        elements = [ele.decode() for ele in y]
        return [x.strip(" (),{}()").split(',') for x in elements]
    
    #Returns an altered temporary dataframe with a new column of a list of tuples
    def merge(df):
        df['LocationsTup'] = df.apply(parse_data, axis=1)
        x_new = df.groupby("userID", as_index=False).sum()
        x_new['LocationsTup'] = x_new.apply(parse_data, axis=1)
        return x_new

    x_new = merge(df)
    
    #Iterrating through rows in dataframe
    for index, row in x_new.iterrows():
        x = row['LocationsTup']
        del x[len(x)-1]

        def removeDuplicates(ls): 
            return [t for t in (set(tuple(i) for i in ls))]

        coordinates = np.array(removeDuplicates(x), dtype = float)
        
        #Silhouette Method
        sil = []
        kmax = len(coordinates)
        for k in range(2, kmax):
            kmeans = KMeans(n_clusters = k).fit(coordinates)
            labels = kmeans.labels_
            sil.append(silhouette_score(coordinates, labels, metric = 'euclidean'))
        
        #Elbow Method
        wcss = []
        kmax = len(coordinates)
        for i in range(1, kmax - 1):
            kmeans = KMeans(n_clusters=i)
            kmeans.fit(coordinates)
            wcss.append(kmeans.inertia_)
        
        #Getting number of clusters from silhouette method
        clusters = interp1d(sil, range(1, len(sil) + 1))
        result_cluster = clusters(max(sil))
        
        #Getting the wcss score
        wcss_score = interp1d(range(1, kmax - 1), wcss)
        result_score = wcss_score(int(result_cluster))
        
        #Finding the centroids
        kmeans = KMeans(n_clusters=int(result_cluster), random_state=0)
        predict = kmeans.fit_predict(coordinates)

        list_of_centroids = kmeans.cluster_centers_.tolist()

        #Getting the size of each cluster
        cluster_sizes = list(Counter(np.sort(predict)).values())
        
        #Adding to the list of users
        userID_list.append(row['userID'])
        
        #Adding to the list of clusters
        ks_list.append(int(result_cluster))
        
        #Adding to the list of silhouette scores
        sil_list.append(max(sil))
        
        #Adding to the list of wcss scores
        wcss_list.append(float(result_score))
        
        index = 0
        for i in cluster_sizes:
            cluster_sizes_dict[index] = cluster_sizes[index]
            index += 1
        
        #Adding to the list of cluster sizes
        cluster_sizes_list.append(json.dumps(cluster_sizes_dict))
        
        index = 0
        for i in list_of_centroids:
            cluster_centroids[index] = list_of_centroids[index]
            index += 1
        
        #Adding to the list of cluster centroids
        cluster_centroids_list.append(json.dumps(cluster_centroids))
        
        
        
def main():
    
    cluster(sys.argv[1])
    
    #Updating dictionary
    final_dict['userID'] = userID_list
    final_dict['k'] = ks_list
    final_dict['Silhouette Score'] = sil_list
    final_dict['WCSS Score'] = wcss_list
    final_dict['Cluster Sizes'] = cluster_sizes_list
    final_dict['Cluster Centroids'] = cluster_centroids_list
        
    #Saving to a tab separated file
    pd.DataFrame(final_dict).to_csv('cluster_csv_data_test.csv', sep = '\t')

if __name__ == "__main__":
    main()
