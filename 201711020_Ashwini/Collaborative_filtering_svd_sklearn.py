##30.90s

import numpy as np
import pandas as pd
import csv
import sklearn.preprocessing as sk
from numpy.linalg import matrix_rank

from sklearn.decomposition import TruncatedSVD
from sklearn.random_projection import sparse_random_matrix
from sklearn.utils.extmath import randomized_svd

##Fetching the ratings data from csv file
ratings_list = [i.strip().split(",") for i in open('C:\\Users\\Dimple Shah\\Desktop\\mtech\\reco\\ratings_1m.csv', 'r').readlines()]
#print(ratings_list)

##Creating the dataframe from the ratings data
ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'BookID', 'Rating'], dtype = float)

## Normalizing the values of the ratings in betweeen 0 to 1
ratings_df.loc[:,'Rating'] = sk.minmax_scale( ratings_df.loc[:,'Rating'] )
##print(ratings_df.loc[:,'Rating'])

## Creating the user-item matrix form the dataframe and finding its rank to reduce the dimension of the matrix
R_df = ratings_df.pivot(index = 'UserID', columns ='BookID', values = 'Rating').fillna(0)
U_R_matrix = R_df.as_matrix()
rank = matrix_rank(U_R_matrix)

## performing the truncated SVD on the user-item matrix
svd = TruncatedSVD(n_components=rank, n_iter=7)
transformed_mat = svd.fit_transform(U_R_matrix)

Sigma_mat = np.diag(svd.singular_values_)

##printing the values of the decomposed components
print("VT")
print(svd.components_)  
print("Sigma")
print(svd.singular_values_)

##If we want to know the U component of the decomposition then we need to use the randomized_svd method which is used by the tuncated_svd in the implementation
##U, Sigma, VT = randomized_svd(U_R_matrix,n_components=rank)
##print("U")
##print(U)
##print("Sigma")
##print(Sigma)
##print("VT")
##print(VT)

##Finding the error in the decomposition
print("error in the approximation")
print((svd.inverse_transform(transformed_mat) - U_R_matrix).sum())
