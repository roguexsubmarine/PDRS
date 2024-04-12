import os
import numpy as np
import pandas as pd
import sklearn

# from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_similarity(p):
    print("checking similarity ...")
        
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
    
    unique_words_count = []

    for _, row in df.iterrows():
        unique_word_count = sum(1 for value in row.values if value > 0)
        unique_words_count.append(unique_word_count)
    # print(unique_words_count)
    
    
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
        
    import matplotlib.pyplot as plt
    import seaborn as sns 

    index=df.index

    #matrix of similarity scores
    n = len(index)
    similarity_matrix = np.zeros((n, n))
    for pair in similarities:
        i, j, similarity_score = pair
        similarity_matrix[i, j] = similarity_score
        similarity_matrix[j, i] = similarity_score

    #check colormaps once
    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_matrix, annot=True, fmt=".2f", xticklabels=index, yticklabels=index, cmap="YlGnBu")
    plt.title("Similarity Matrix")
    plt.xlabel("Files")
    plt.ylabel("Files")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    output_filename = "./static/similarityheatmap.png"
    plt.savefig(output_filename, format="png")
    plt.close() 
    

    # print(simlist)
    return simlist

# p=input("Enter the directory path: ")

# print(calculate_similarity(p)) #comment out later
print("...similarity checked")