import os
import numpy as np
import pandas as pd
import sklearn

# from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_similarity(directory_path):
        
    ext = ('.py', '.c', '.cpp', '.txt', '.ipynb','.java','.html')
    lst=[]
    file_names=[]

    #implement stopwords later

    #parsing files from dir try to optimize plz
    for filename in os.listdir(p):
        if filename.endswith('.pdf'):
            file_path = os.path.join(p, filename)
            file_names.append(filename)
            import PyPDF2
            pdfFileObject = open(file_path, 'rb')
            reader = PyPDF2.PdfReader(pdfFileObject)
            count = len(reader.pages)
            output=""
            for i in range(count):
                page = reader.pages[i]
                output += page.extract_text()
            lst.append(output)
            
        if filename.endswith(ext):
            file_path = os.path.join(p, filename)
            try:
                with open(file_path, encoding='utf-8') as f:
                    file_names.append(filename)
                    content = f.read()
                    lst.append(content)
            except UnicodeDecodeError:
                print(f"UnicodeDecodeError: Unable to decode '{filename}'")

    # vectorizer = TfidfVectorizer()
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)

    vectorizer.fit(lst)

    #comment this out l8r
    # print("Vocabulary: ", vectorizer.vocabulary_)

    #sm
    vector = vectorizer.transform(lst)

    #sparse matrix to df and dict
    df = pd.DataFrame(vector.toarray(), columns=vectorizer.get_feature_names_out(), index=file_names)
    vectordc={}
    for index, values in df.iterrows():
        vectordc[index] = values.tolist()

    #export to xlsx to make it easier to read vsc cant handle dataframes well 
    file_name = 'Sparsematrix.csv'

    print("Encoded Document is:",file_name)

    df.to_csv(file_name)

    from sklearn.metrics.pairwise import cosine_similarity

    #function to calculate cosine similarity between all pairs of vectors
    def pairwise_cosine_similarity(vector_list):
        similarities = []
        n = len(vector_list)
        for i in range(n):
            for j in range(i + 1, n):
                similarity = cosine_similarity([vector_list[i]], [vector_list[j]])[0][0]
                similarities.append((i, j, similarity))  #storing indices and similarity score
        return similarities

    vector_list = df.values.tolist()

    #call rows from dataframe
    similarities = pairwise_cosine_similarity(vector_list)

    #print cosine similarities for each pair of vectors
    simlist=[]
    for pair in similarities:
        index1 = df.index[pair[0]]
        index2 = df.index[pair[1]]
        similarity_score = pair[2]
        # print(f"Similarity between vectors {index1} and {index2}: {similarity_score}")
        simlist.append([index1,index2,similarity_score])
    
    return simlist

p=input("Enter the directory path: ")
print(calculate_similarity(p))