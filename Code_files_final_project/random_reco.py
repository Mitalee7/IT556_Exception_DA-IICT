import random
import csv
import pandas as pd
import numpy as np
#CSV FILE VARIABLES
USER_STATE_TABLE_CSV = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\state_table\\state_user_'
BOOK_DATA_CSV = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\Book1_reduced_data.csv"

def random_reco_list(user_id):
    csv_file_name = USER_STATE_TABLE_CSV +str(user_id)+'.csv'
    ds = pd.read_csv(BOOK_DATA_CSV)
    rating_cols=['book_id' , 'title' , 'reward']
       
    rating_df=pd.read_csv(csv_file_name , names=rating_cols , encoding='latin-1')
    #print(rating_df['book_id']-1)
    idx1=pd.Index(rating_df['book_id']-1)
    idx2=pd.Index(np.random.randint(0,999,size=40))
    book_id=idx2.difference(idx1)

    ##print(ds.iloc[book_id[0:10]])
    return ds.iloc[book_id[0:10]]
