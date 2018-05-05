import urllib.request
import csv
def downloader(image_url,i):
    full_file_name = str(i) + '.jpg'
    #print(image_url)
    urllib.request.urlretrieve(image_url,full_file_name)
    print(i)
    
i = 1
with open('C:/Users/DELL/Downloads/image_books.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        t = row[0]
        downloader(t,i)
        #print(row[0])
        i = i+1

'''
downloader('ds.loc[7]')
'''
