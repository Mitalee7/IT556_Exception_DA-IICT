import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import csv
#CSV FILE VARIABLES
BOOK_DATA_CSV = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\Book1_reduced_data.csv"
CONTENT_BASED_SIMILARITY_CSV = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\book_tfidf_similarity.csv'

ds = pd.read_csv(BOOK_DATA_CSV)
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 8), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['title'])
#print(tfidf_matrix.shape)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print(cosine_sim.size)
with open(CONTENT_BASED_SIMILARITY_CSV, "a", newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerows(cosine_sim)
'''
for i in range(len(cosine_sim)):
    with open('C:/Users/DELL/AppData/Local/Programs/Python/Python36-32/programs/recommendation/book_tfidf_similarity.csv', "a", newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(cosine_sim[i])
        filewriter.writerows(cosine_sim)
'''
