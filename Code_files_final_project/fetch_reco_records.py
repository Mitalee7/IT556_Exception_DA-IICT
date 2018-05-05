import csv
import pandas as pd
import numpy as np
import random_reco
#CSV FILES VARIABLES
USER_ITEM_RATING_PKL = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\User_Item_ratings.pkl"
USER_STATE_TABLE_CSV = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\state_table\\state_user_'
ITEM_ITEM_SIMILARITY_CSV = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\book_similarity.csv'
CONTENT_BASED_SIMILARITY_CSV = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\book_tfidf_similarity.csv'
BOOK_DATA_CSV = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\Book1_reduced_data.csv"

#function to return predicted rating through SVD
def predicted_rating(user, item):
    df = pd.read_pickle(USER_ITEM_RATING_PKL)
    #print(item)
    item=item-np.full(len(item),1)
    #print("\n",df.loc[user-1,item].values)
    if(user in df.index):
        #print("\n",df.loc[user-1,item].values)
        return df.loc[user-1,item].values
    return np.zeros(len(item))


def reco_list(user):
    #variable to choose books
    state_fetch_value = 10
    #item_similarity_value = 11
    
###########
    kn=100  #constant
    a=0.01  #learning rate
    n=5  #without reward recoomendation that we require
########

    book_list = []
    rank_list = []

    #get values form state table
    rating_cols=['book_id' , 'title' , 'reward']
    csv_file_name = USER_STATE_TABLE_CSV +str(user)+'.csv'
    rating_df=pd.read_csv(csv_file_name, names=rating_cols , encoding='latin-1')
    book_ids=rating_df['book_id'].values

    #get sorted list of books from state table vased on the reward
    sorted_list = rating_df.nlargest(state_fetch_value,'reward')
    if(sorted_list['reward'].iloc[3]<0):
        random_rec=random_reco.random_reco_list
        #print("random")
        r_list=random_rec(user)
        return r_list
    #print(sorted_list)

    
    #open item item similarity csv
    with open(ITEM_ITEM_SIMILARITY_CSV) as csvfile:
        readCSV = csv.reader(csvfile,delimiter=',')
        j = state_fetch_value
        rows = list(readCSV)
        for i in range (state_fetch_value):

###########
            item_similarity_value= int(n+(j*a*kn))+1
            #print(item_similarity_value)
            j-=1
##############


            temp = np.array(rows[(sorted_list['book_id'].iloc[i]) - 1])  # toselecting the row of the similarity matrix and get maximum similar items
           # print('The value of temp',temp)
            rr =  list(map(float,sorted(temp,key = float,reverse = True)))
            rr = rr[1:item_similarity_value]  #item_sim value added to rank
            rr = rr + (sorted_list['reward'].iloc[i]) #reward added to rank
            arr = temp.argsort()[-item_similarity_value:][::-1] + 1
            rating=predicted_rating(1,arr[1:item_similarity_value])
            rr = rr + rating  # predicted rating added to rank
            book_list = book_list+ arr[1:].tolist()
            rank_list = rank_list + rr.tolist()
    #open tf_idf similarity matrix and added to rank
    with open(CONTENT_BASED_SIMILARITY_CSV) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        rows = list(readCSV)
        for i in range (state_fetch_value):
            k = 0
            for j in book_list:
                temp = np.array(rows[(sorted_list['book_id'].iloc[i]) - 1])
                temp = temp.astype(float)
                rank_list[k] = rank_list[k] + temp[j-1]
                k = k+1           
    #dataframe of the book_list and rank list
    book_list = book_list-np.full(len(book_list),1)
    ds = pd.read_csv(BOOK_DATA_CSV)
    rank_list = rank_list + (ds.iloc[book_list]['average_rating'].values)
    book_list = book_list+np.full(len(book_list),1)
    data_list = (pd.DataFrame({'booklist': book_list,
         'ranklist': rank_list,
        }))

    ##print(data_list)
    #Sorting the dataframe by rank
    data_list=data_list.sort_values(by='ranklist',ascending=False)
    #computing frequenct count of the recommended books
    data_list['freq']=(data_list.groupby('booklist')['booklist'].transform('count')-1)/30
    #adding the weight of the frequeny to reward
    ##print("before",data_list,"\n",)
    data_list['ranklist']=data_list['ranklist']+data_list['freq']
    ##print(data_list,"\n",)
    #finding unique books from the data list
    d=data_list['booklist'].drop_duplicates().index
    uniq=data_list.loc[d]
    uniq['booklist']=uniq['booklist'].astype(int)

    #deleting the items which are already i the state table
    idx1=pd.Index(uniq['booklist'])
    idx2=pd.Index(book_ids)
    book_id=idx1.difference(idx2)
    uniq=uniq.loc[uniq['booklist'].isin(book_id)]
    uniq=uniq.sort_values(by='ranklist',ascending=False)
    
    unique=pd.DataFrame(uniq.as_matrix(),columns=['book_id','rank','freq_w']) # to set the index
    unique['book_id']=unique['book_id'].astype(int)
    #print(unique['book_id'][0:10])


##############
    b=0.8 #exploitation rate
    top_k=10
    exploit=int(top_k*b)
    explore=top_k-exploit
    rndm=random_reco.random_reco_list
    ran_list=rndm(user)
    ran_list=ran_list.drop(['books_count','image_url'],1)
    #print(ran_list['book_id'])

    #fetching top k items to display
    top_k_r_books=unique['book_id'][0:top_k]
    #print(top_k_r_books)

   
    flag=False
    randm_bid=np.zeros(2)
    r_list=ds.iloc[top_k_r_books].drop(['books_count','image_url'],1)
    cnt=0
    for j in range(len(ran_list)):
        if(ran_list['book_id'].iloc[j] not in top_k_r_books and ran_list['book_id'].iloc[j] not in sorted_list['book_id']  ):
             randm_bid[cnt]=j
             cnt+=1
        if(cnt==2):
             flag=True
             break
    #print(randm_bid)
    top_k_r_books = top_k_r_books-np.full(top_k_r_books.size,1)

    if(flag==False):
        r_list=ds.iloc[top_k_r_books].drop(['books_count','image_url'],1)
    else:
        r_list=ds.iloc[top_k_r_books[0:exploit]].drop(['books_count','image_url'],1)
        r_list=r_list.append(ran_list.iloc[randm_bid])

##############

    #fetching top k items to display
 #   top_k_r_books=unique['book_id'][0:10]
  #  top_k_r_books = top_k_r_books-np.full(top_k_r_books.size,1)
   # #print(top_k_r_books)
    #r_list=ds.iloc[top_k_r_books].drop(['books_count','image_url'],1)
    return(r_list)
