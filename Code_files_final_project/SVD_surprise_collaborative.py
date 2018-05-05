import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVD
import numpy as np
import pickle
   #.prediction_algorithms.matrix_factorization.SVD


rating_cols=['user_id' , 'book_id' , 'rating']
rating_df=pd.read_csv('C:\\Users\\Dimple Shah\\Desktop\\mtech\\reco\\dataset\\ratings_shrink.csv' , names=rating_cols , encoding='latin-1')


print(max(rating_df['user_id']))
usr=max(rating_df['user_id'])
itm=max(rating_df['book_id'])
mtx=np.zeros((usr,itm))
reader= Reader(rating_scale=(1,5))
data=Dataset.load_from_df(rating_df[['user_id' , 'book_id' ,'rating']] , reader)
rat= rating_df.pivot(index = 'user_id', columns ='book_id', values = 'rating').fillna(0)
trainset = data.build_full_trainset()
print("Svd enter")
algo = SVD()
algo.fit(trainset)
print("train")
# Than predict ratings for all pairs (u, i) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)
print("tsted")

labels=['uid', 'iid', 'r_ui', 'est', 'details']
predicted_rat=pd.DataFrame.from_records(predictions,columns=labels)
pp= predicted_rat.pivot(index = 'uid', columns ='iid', values = 'est').fillna(0)
pp.index.name='user_id'
pp.columns.name='book_id'
fnl=pp.add(rat)
u_ind=np.asarray(fnl.index)
i_ind=np.asarray(fnl.columns)
print("dataframe done")#,u_ind,i_ind)
for i in u_ind:
   # print(i)
    for j in i_ind:
    #    print(j)
        mtx[i-1][j-1]=fnl.loc[i,j]
    print("*")
print("pickle")
dd=pd.DataFrame(mtx,index=np.arange(mtx.shape[0]),columns=np.arange(mtx.shape[1]))
dd.to_pickle("demo.pkl")  # where to save it, usually as a .pkl
print("pickle write_done")
df = pd.read_pickle("demo.pkl")
print("pickle raed doen")

# =============================================================================
# m2=pp.as_matrix()
# m1=rat.as_matrix()
# fnl=m1+m2
# 
# =============================================================================
'''
a=predictions[0][1]
for i in range(len(predictions)):
      x=predictions[i][0]
      y=predictions[i][1]
    #  print(i)
      #print(predictions[i][3])
      mtx[x-1][y-1]=predictions[i][3]
      rat.loc[x,y]=predictions[i][3]
print("**")
#print(3 in rating_df['book_id'].values )#.index.get_level_values('book_id'))
mm=rat.as_matrix()

for i in range(usr):
    for j in range(itm):
          if((i+1 in rating_df['user_id'].values) and (j+1 in rating_df['book_id'].values) and (mtx[i][j]==0)):
              a=rat.loc[i+1,j+1]
              if(a!=0):
                 # print("inside")
                  mtx[i][j]=a
  #  print("*")
print("matrix",mtx,"\nrat df",rat.values)
pred=algo.predict(uid=1,iid=2,r_ui=0,verbose=True)
print("pred\n",pred)
dd=pd.DataFrame(mtx,index=np.arange(mtx.shape[0]),columns=np.arange(mtx.shape[1]))
dd.to_pickle("demo.pkl")  # where to save it, usually as a .pkl
df = pd.read_pickle("demo.pkl")
dif=mm-fnl
'''