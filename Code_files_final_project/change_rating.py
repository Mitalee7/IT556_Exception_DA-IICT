import csv
import pandas as pd
import numpy as np

#function to change predicted rating through SVD
def change_rating(user_id, item_id,rating):
    df = pd.read_pickle("C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\User_Item_ratings.pkl")
    #print(item)
 #   print(user_id not in df.index+1)
    if(user_id in df.index+1):
        df.loc[user_id-1,item_id-1]=rating
        #print("\n",df.loc[user-1,item].values)
        df.to_pickle("C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\User_Item_ratings.pkl")
        #df1 = pd.read_pickle("C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\User_Item_ratings.pkl")
#        print(df)

#change_rating(5,5,5)
