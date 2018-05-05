import numpy as np
import pandas as pd
import csv
from sklearn.metrics.pairwise import linear_kernel
#CSV FILE VARIABLES
BOOK_RATING_CSV = 'C:/Users/DELL/AppData/Local/Programs/Python/Python36-32/programs/recommendation/ratings_books.csv'
ITEM_ITEM_SIMILARITY_CSV = 'C:/Users/DELL/AppData/Local/Programs/Python/Python36-32/programs/recommendation/book_similarity.csv'
#load csv
header = ['user_id', 'book_id', 'rating']
df = pd.read_csv(BOOK_RATING_CSV, sep=',', names=header)
n_users = df.user_id.max();
n_items = df.book_id.max();
print ('Number of users = ' + str(n_users) + ' | Number of movies = ' + str(n_items))
    
user_item_matrix = np.zeros((n_users, n_items))
for line in df.itertuples():
    user_item_matrix[line[1]-1, line[2]-1] = line[3]
print(user_item_matrix[3][69])
#cosine_sim = linear_kernel(user_item_matrix, user_item_matrix)
#print(cosine_sim)

similarity_matrix = np.zeros((n_items, n_items))
avg_rating_i_item = []

for i in range(n_items):
    avg_rating = 0
    total=0
    for j in range(n_users):
        if(user_item_matrix[j][i]!=0):
            total=total+1
            avg_rating =avg_rating + user_item_matrix[j][i]
    if(total!=0):
        avg_rating_i_item.append(avg_rating/total)
    else:
        avg_rating_i_item.append(0);

print(len(avg_rating_i_item))
for i in range(n_items):
    for j in range(n_items):
        r_i = []
        r_j=[]
        for u in range(n_users):
            if(user_item_matrix[u][i]!=0 and user_item_matrix[u][j]!=0):
                r_i.append(user_item_matrix[u][i]-avg_rating_i_item[i])
                r_j.append(user_item_matrix[u][j]-avg_rating_i_item[j])
        if(len(r_i)!=0 and len(r_j)!=0):
            r_i=np.array(r_i)
            r_j=np.array(r_j)
            numerator = np.sum(r_i*r_j)
            denominator = np.sqrt(np.sum(r_i**2))*np.sqrt(np.sum(r_j**2))
            if(denominator!=0):
                similarity_matrix[i][j] = numerator/denominator
        #print(similarity_matrix[i][j])
'''
    with open(ITEM_ITEM_SIMILARITY_CSV, "a", newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(similarity_matrix[i])'''
#print(similarity_matrix.shape)

