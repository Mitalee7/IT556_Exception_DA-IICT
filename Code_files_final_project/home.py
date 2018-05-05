import book_details
from  book_details import goto_label
import fetch_reco_records
import csv
import pandas as pd
import numpy as np
import random_reco
#CSV Files Variables
NEW_USER_CREATE_CSV = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\state_table\\state_user_'
EXISTING_USER_CSV = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\state_table\\state_user_'
#other Variables
show_books=10
flag=False
delete_top_num=10
state_rows=30
cols = ['book_id','title','reward']

temp =int(input('1. New User?\n2. Existing User?\n'))
#For New User
if temp==1:
    random_rec=random_reco.random_reco_list
    user_id=10000
    csv_file_name = NEW_USER_CREATE_CSV +str(user_id)+'.csv'

    with open (csv_file_name,'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
    #get Recommendation list
    df =random_rec(user_id)
    df2 = pd.DataFrame([],columns=cols)
    df2['book_id']=df['book_id']
    df2['title']=df['title']
    df2['reward']= -1
    
    choice = 0
    reward=np.full(10,-1)
    while choice != 12 :
        if (choice == 11) and flag==False :
            # Show the list of 10 books according to rank calculated for that user
            reco_books = fetch_reco_records.reco_list
            df2 = pd.DataFrame([],columns=cols)
            df = reco_books(user_id)
            #print(df)
            df2['book_id']=df['book_id']
            df2['title']=df['title']
            df2['reward']= -1
            #print(df2)
        print("Book List (Select interesting book ) :")
        for i in range(show_books):
            print(i+1," ",df['title'].iloc[i])
        print(show_books+1," Refresh ")
        print(show_books+2," Exit")
        choice = int(input('Choose an option : '))
        switcher = {
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 4,
            6: 5,
            7: 6,
            8: 7,
            9: 8,
            10: 9,
            11: "ref",
            12: "exit"
        }
        #print(switcher.get(choice, "Invalid Option"))
        choice_output=switcher.get(choice)
        #print(choice_output)
        #print(df.iloc[choice_output].values)
        #print(type(choice_output))
        #print(choice_output != "ref")
        if(choice_output != "ref" and choice_output!="exit"):
            show_book_details = book_details.show_book_details
##            temp=df2['reward'].iloc[choice_output]
##            temp=temp+show_book_details(user_id,df.iloc[choice_output])
##            df2['reward'].iloc[choice_output].copy(temp)
            reward[choice_output]+=show_book_details(user_id,df.iloc[choice_output])
            if(goto_label):
                flag = goto_label
                print(flag)
        else:
            flag=False
            df2['reward']=reward
##            print(df2['reward'])
            reward=np.full(10,-1)
            #csv_file_name = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\state_table\\state_user_'+str(user_id)+'.csv'
##            print(csv_file_name)
            '''with open (csv_file_name,'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')'''
                
            df1 = pd.read_csv(csv_file_name,names=cols,encoding='latin-1')
            #print(df1)
            rows,columns = df1.shape
            #print(rows)
            if(rows==state_rows):
                df1.drop(df1.head(delete_top_num).index, inplace=True)
                #print(df1)
            df3=pd.concat([df1, df2],ignore_index=True)
            #print(df3)
            df3.to_csv(csv_file_name,header=False,columns=None,index=False)


#For existing User
if temp == 2:
    user_id = int(input('Enter User ID\n'))
    choice = 0
    reward=np.full(10,-1)
    while choice != 12 :
        if (choice == 11 or choice == 0) and flag==False :
            # Show the list of 10 books according to rank calculated for that user
            reco_books = fetch_reco_records.reco_list
            df2 = pd.DataFrame([],columns=cols)
            df = reco_books(user_id)
            #print(df)
            df2['book_id']=df['book_id']
            df2['title']=df['title']
            df2['reward']= -1
            #print(df2)
        print("Book List (Select interesting book ) :")
        for i in range(show_books):
            print(i+1," ",df['title'].iloc[i])
        print(show_books+1," Refresh ")
        print(show_books+2," Exit")
        choice = int(input('Choose an option : '))
        switcher = {
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 4,
            6: 5,
            7: 6,
            8: 7,
            9: 8,
            10: 9,
            11: "ref",
            12: "exit"
        }
        #print(switcher.get(choice, "Invalid Option"))
        choice_output=switcher.get(choice)
        #print(choice_output)
        #print(df.iloc[choice_output].values)
        #print(type(choice_output))
        #print(choice_output != "ref")
        if(choice_output != "ref" and choice_output!="exit"):
            show_book_details = book_details.show_book_details
##            temp=df2['reward'].iloc[choice_output]
##            temp=temp+show_book_details(user_id,df.iloc[choice_output])
##            df2['reward'].iloc[choice_output].copy(temp)
            reward[choice_output]+=show_book_details(user_id,df.iloc[choice_output])
            if(goto_label):
                flag = goto_label
                print(flag)
        else:
            flag=False
            df2['reward']=reward
##            print(df2['reward'])
            reward=np.full(10,-1)
            csv_file_name = EXISTING_USER_CSV +str(user_id)+'.csv'
##            print(csv_file_name)
            '''with open (csv_file_name,'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')'''
                
            df1 = pd.read_csv(csv_file_name,names=cols,encoding='latin-1')
            #print(df1)
            rows,columns = df1.shape
            #print(rows)
            if(rows==state_rows):
                df1.drop(df1.head(delete_top_num).index, inplace=True)
                #print(df1)
            df3=pd.concat([df1, df2],ignore_index=True)
            #print(df3)
            df3.to_csv(csv_file_name,header=False,columns=None,index=False)
                




