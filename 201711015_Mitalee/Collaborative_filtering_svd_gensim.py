import numpy as np
import pandas as pd
import csv
import sklearn.preprocessing as sk
from gensim.corpora import MmCorpus
from gensim.test.utils import get_tmpfile
from numpy.linalg import matrix_rank
import gensim
import gensim.models.lsimodel as ls
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

## creating the corpus from the user-item matrix
Z=gensim.matutils.Dense2Corpus(U_R_matrix, documents_columns=True)
##print(Z)
## performing the truncated SVD on the user-item matrix
lsi=ls.LsiModel(Z, num_topics=3)


##printing the values of the decomposed components
print("Sigma")
print(lsi.projection.s)
Sigma_mat = np.diag(lsi.projection.s)

print("U")
print(lsi.projection.u)

print("VT")
V = gensim.matutils.corpus2dense(lsi[Z], len(lsi.projection.s)).T / lsi.projection.s
print(V)

a=np.matmul(lsi.projection.u,Sigma_mat)
approx=np.matmul(a,V.T)
##print(approx)

##Finding the error in the decomposition
print("error in the approximation")
print((approx - U_R_matrix).sum())

