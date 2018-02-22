import csv
import spacy
import textacy

nlp = spacy.load('en_core_web_sm')# <-- an instance of `English` with data loaded in

with open ('/media/mit/Local Disk/DA-IICT/sem 2/Recomm.Engine/nlp_assg3/book_data.csv','r') as File:
    csv_file_object = csv.reader(File)
    for row in csv_file_object:
        print("\nBook Name : ",row[1],"\n")
        doc=nlp(row[1])
#Noun phrase extraction from item description(i.e book title)
        print("\nNoun phrase extraction from item description:")
        for np in doc.noun_chunks:
            print(np.text)
#Lemmatization of verb phrases.
        pattern = r'<VERB>?<ADV>*<VERB>+'
        lists = textacy.extract.pos_regex_matches(doc, pattern)
        print("\nLemmatization of verb phrases:")
        for token in lists:
            print(token.text," --> ", token.lemma_)
#Named Entity extraction and recognition in item description.
        print("\nNamed Entity extraction and recognition in item description:")
        for entity in doc.ents:
            print(entity.text, entity.start_char, entity.end_char, entity.label_)

