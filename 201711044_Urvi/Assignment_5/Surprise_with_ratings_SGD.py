# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 23:19:28 2018

@author: Dimple Shah
"""

import surprise
import numpy as np
import pandas as pd
import sklearn.preprocessing as sk
from surprise import Dataset
from surprise import Reader
#from memory_profiler import profile

import os
import psutil
import time
import matplotlib.pyplot as plt
start = time.time()

process = psutil.Process(os.getpid())
m1=process.memory_full_info().uss

x=[]
timex=[]
mem=[]

class MatrixFacto(surprise.AlgoBase):
    '''A basic rating prediction algorithm based on matrix factorization.'''
    
    def __init__(self, learning_rate, n_epochs, n_factors):
        
        self.lr = learning_rate  # learning rate for SGD
        self.n_epochs = n_epochs  # number of iterations of SGD
        self.n_factors = n_factors  # number of factors
        self.skip_train = False
        
    def train(self, trainset):
        '''Learn the vectors p_u and q_i with SGD'''
        
        print('Fitting data with SGD...')
        
        # Randomly initialize the user and item factors.
        p = np.random.normal(0, .1, (trainset.n_users, self.n_factors))
        q = np.random.normal(0, .1, (trainset.n_items, self.n_factors))
        
        # SGD procedure
        for _ in range(self.n_epochs):
            for u, i, r_ui in trainset.all_ratings():
                err = r_ui - np.dot(p[u], q[i])
                # Update vectors p_u and q_i
                p[u] += self.lr * err * q[i]
                q[i] += self.lr * err * p[u]
                # Note: in the update of q_i, we should actually use the previous (non-updated) value of p_u.
                # In practice it makes almost no difference.
        
        self.p, self.q = p, q
        self.trainset = trainset

    def estimate(self, u, i):
        '''Return the estmimated rating of user u for item i.'''
        
        # return scalar product between p_u and q_i if user and item are known,
        # else return the average of all ratings
        if self.trainset.knows_user(u) and self.trainset.knows_item(i):
            return np.dot(self.p[u], self.q[i])
        else:
            return self.trainset.global_mean


reader = Reader(rating_scale=(0, 1))


#Checking RMSE with 300k data records

ratings_list1 = [i.strip().split(",") for i in open('C:\\Users\\Dimple Shah\\Desktop\\mtech\\reco\\3l.csv', 'r').readlines()]
ratings_df1 = pd.DataFrame(ratings_list1, columns = ['UserID', 'BookID', 'Rating'], dtype = float)

ratings_df1.loc[:,'Rating'] = sk.minmax_scale( ratings_df1.loc[:,'Rating'] )


data1 = Dataset.load_from_df(ratings_df1[['UserID', 'BookID', 'Rating']], reader)

data1.split(2)  # split data for 2-folds cross validation
algo1 = MatrixFacto(learning_rate=.01, n_epochs=10, n_factors=10)#print(algo)
#test_rms=
result1=surprise.evaluate(algo1, data1, measures=['RMSE'])#print(test_rms)
x.append(np.mean(result1['RMSE']))
end = time.time()
#print("Time1",end - start)
timex.append(end-start)
process=psutil.Process(os.getpid())
m2=process.memory_full_info().uss
#m2=m2-m1
print(m2)
mem.append(m2)


#Checking RMSE with 500k data records


start = time.time()
ratings_list2 = [i.strip().split(",") for i in open('C:\\Users\\Dimple Shah\\Desktop\\mtech\\reco\\5l.csv', 'r').readlines()]
ratings_df2 = pd.DataFrame(ratings_list2, columns = ['UserID', 'BookID', 'Rating'], dtype = float)

ratings_df2.loc[:,'Rating'] = sk.minmax_scale( ratings_df2.loc[:,'Rating'] )


data2 = Dataset.load_from_df(ratings_df2[['UserID', 'BookID', 'Rating']], reader)

data2.split(2)  # split data for 2-folds cross validation
algo2 = MatrixFacto(learning_rate=.01, n_epochs=10, n_factors=10)#print(algo)
result2= surprise.evaluate(algo2, data2, measures=['RMSE'])#print(test_rms)
x.append(np.mean(result2['RMSE']))
end = time.time()
#print("Time2",end - start)
timex.append(end-start)
process=psutil.Process(os.getpid())
m3=process.memory_full_info().uss
#m3=m3-m1
print(m3)
mem.append(m3)


#Checking RMSE with 600k data records


start = time.time()
ratings_list3 = [i.strip().split(",") for i in open('C:\\Users\\Dimple Shah\\Desktop\\mtech\\reco\\6l.csv', 'r').readlines()]
ratings_df3 = pd.DataFrame(ratings_list3, columns = ['UserID', 'BookID', 'Rating'], dtype = float)

ratings_df3.loc[:,'Rating'] = sk.minmax_scale( ratings_df3.loc[:,'Rating'] )


data3 = Dataset.load_from_df(ratings_df3[['UserID', 'BookID', 'Rating']], reader)

data3.split(2)  # split data for 2-folds cross validation
algo3 = MatrixFacto(learning_rate=.01, n_epochs=10, n_factors=10)#print(algo)
result3= surprise.evaluate(algo3, data3, measures=['RMSE'])#print(test_rms)
x.append(np.mean(result3['RMSE']))
end = time.time()
#print("Time3",end - start)
timex.append(end-start)
process=psutil.Process(os.getpid())
m4=process.memory_full_info().uss
#m4=m4-m1
print(m4)
mem.append(m4)


#plotting graph for the time taken for different number of records

y = [len(ratings_list1),len(ratings_list2),len(ratings_list3)]
plt.plot( timex[0],y[0],'ro',label='300000 records')
plt.plot( timex[1], y[1],'bo',label='500000 records')
plt.plot( timex[2],y[2],'go',label='600000 records')
legend = plt.legend(loc='upper left')
frame = legend.get_frame()
plt.xlabel('Time(in sec)')
plt.ylabel('Number of records')
plt.title('Time Vs Number of Records')
plt.legend()
plt.show()

#plotting graph for the RMSE for different number of records

y = [len(ratings_list1),len(ratings_list2),len(ratings_list3)]
plt.plot( x[0],y[0],'gs',label='300000 records')
plt.plot( x[1],y[1],'rs',label='500000 records')
plt.plot( x[2],y[2],'bs',label='600000 records')
legend = plt.legend(loc='upper left')
frame = legend.get_frame()
plt.xlabel('Mean RMSE')
plt.ylabel('Number of records')
plt.title('Mean RMSE Vs Number of Records')
plt.legend()

plt.show()


#plotting graph for the memory space taken for different number of records

y = [len(ratings_list1),len(ratings_list2),len(ratings_list3)]
plt.plot( mem[0],y[0],'g^',label='30000 records')
plt.plot( mem[1],y[1],'r^',label='500000 records')
plt.plot( mem[2],y[2],'b^',label='600000 records')
legend = plt.legend(loc='upper left')
frame = legend.get_frame()
plt.xlabel('Memory Usage')
plt.ylabel('Number of records')
plt.title('Memory Usage Vs Number of Records')
plt.legend()

plt.show()