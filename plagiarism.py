import os
import numpy as np
import pandas as pd
import sklearn

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_similarity(p):
    print("checking similarity ...")
        
    ext = ('.py', '.c', '.cpp', '.txt','.java','.html','.rs')
    lst=[]
    prog_lst=[]
    file_names=[]
    #implement stopwords later

    #parsing files from dir try to optimize plz
    for filename in os.listdir(p):
        if filename.endswith('.docx'):
            file_path = os.path.join(p, filename)
            file_names.append(filename)
            import docx
            doc = docx.Document(file_path)
            text = ''
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            lst.append(text)
                
                
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
        
        if filename.endswith('.ipynb'):
            file_path = os.path.join(p, filename)
            file_names.append(filename)
            import nbformat
            notebook = nbformat.read(file_path, as_version=4)
            source_code = []
            for cell in notebook.cells:
                if cell.cell_type == 'code':
                    source_code.append(cell.source)
    
            notebook_text = '\n'.join(source_code)
            lst.append(notebook_text)
            
        if filename.endswith(ext):
            file_path = os.path.join(p, filename)
            try:
                with open(file_path, encoding='utf-8') as f:
                    file_names.append(filename)
                    content = f.read()
                    lst.append(content)
                    prog_lst.append(content)
            except UnicodeDecodeError:
                print(f"UnicodeDecodeError: Unable to decode '{filename}'")

    cvectorizer = CountVectorizer()
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)

    vectorizer.fit(lst)
    cvectorizer.fit(lst)



    #comment this out l8r
    # print("Vocabulary: ", vectorizer.vocabulary_)

    #sm
    vector = vectorizer.transform(lst)
    cvector = cvectorizer.transform(lst)

    #sparse matrix to df and dict
    df = pd.DataFrame(vector.toarray(), columns=vectorizer.get_feature_names_out(), index=file_names)
    cdf = pd.DataFrame(cvector.toarray(), columns=cvectorizer.get_feature_names_out(), index=file_names)
    unique_words_count = []

    for _, row in df.iterrows():
        unique_word_count = sum(1 for value in row.values if value > 0)
        unique_words_count.append(unique_word_count)
    # print(unique_words_count)
    
    
    #export to xlsx to make it easier to read vsc cant handle dataframes well 
    file_name = 'Sparsematrix.csv'

    print("Encoded Document is:",file_name)

    df.to_csv(file_name)
    cdf.to_csv('countmatrix.csv')

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
        similarity_score = round(pair[2] * 100, 2)
        # print(f"Similarity between vectors {index1} and {index2}: {similarity_score}")
        simlist.append([index1,index2,similarity_score])
        
    
    #top prog langs below, check for accuracy cuz im not sure
    topkeywordslist=[]
    def read_keyword_files(directory):
        keyword_contents = {}
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    lines = [line.strip() for line in lines]
                    file_name = os.path.splitext(filename)[0]
                    keyword_contents[file_name] = lines
        return keyword_contents
    

    keywords_folder = r'./keywords' #add path
    check_list=prog_lst
    keyword_contents = {}
    for filename in os.listdir(keywords_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(keywords_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                file_name = os.path.splitext(filename)[0]
                keyword_contents[file_name] = lines

    max_keywords_language = {}
    for wrd in check_list:
        max_keywords = 0
        max_language = None
        for language, keywords in keyword_contents.items():
            keywords_found = sum(1 for keyword in keywords if keyword in wrd)
            if keywords_found > max_keywords:
                max_keywords = keywords_found
                max_language = language
        if max_language:
            max_keywords_language[wrd] = max_language

    topkeywordslist = []
    for wrd, language in max_keywords_language.items():
        topkeywordslist.append(language)
        
    from collections import Counter
    counts=Counter(topkeywordslist)
    toplang=counts.most_common(1)[0][0]
    
    #plots below from here, this is heatmap
    import matplotlib.pyplot as plt
    import seaborn as sns 

    index=df.index
    hdf=df
    hdf.index = np.arange(1,len(hdf)+1)
    hindex=hdf.index


    n = len(index)
    similarity_matrix = np.zeros((n, n))
    for pair in similarities:
        i, j, similarity_score = pair
        similarity_matrix[i, j] = similarity_score
        similarity_matrix[j, i] = similarity_score
        
    #top 50 words barplot
    frequency_df = pd.DataFrame(cdf.sum(), columns=['Frequency'])
    frequency_df = frequency_df.sort_values(by='Frequency', ascending=False)

    top = frequency_df.head(50)
    top.plot(kind='bar')
    plt.title('Top 50 Words by Frequency')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    output_filename = "./static/top50words.png"
    plt.savefig(output_filename, format="png")
    plt.close() 


    import networkx as nx
    from matplotlib.patches import Rectangle

    G = nx.Graph()

    for i in range(len(similarity_matrix)):
        G.add_node(i)



    for i in range(len(similarity_matrix)):
        for j in range(i + 1, len(similarity_matrix[i])):
            similarity = similarity_matrix[i][j]
            if similarity > 0.1:
                G.add_edge(i, j, weight=similarity, label=f'{1 - similarity:.2f}')
                
    n = len(index)
    pos = nx.spring_layout(G, center=[0.5,0.5],k=0.3,scale=15)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=250, font_size=6, font_color='black',
            edge_color='gray', width=2)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=4,font_color='black')
    # Create a border around the plot
    border = Rectangle((plt.xlim()[0], plt.ylim()[0]), plt.xlim()[1] - plt.xlim()[0], plt.ylim()[1] - plt.ylim()[0],
                    edgecolor='black', linewidth=2, facecolor='none')
    plt.gca().add_patch(border)
        #plt.axis('on')  # Show axes
    plt.title('Graph of Cosine Similarity')
    output_filename = "./static/clustermap.png"
    plt.savefig(output_filename, format="png")

    # plt.show()
    #matrix of similarity scores
    n = len(index)
    similarity_matrix = np.zeros((n, n))
    for pair in similarities:
        i, j, similarity_score = pair
        similarity_matrix[i, j] = similarity_score
        similarity_matrix[j, i] = similarity_score
    print(hdf.head())
    #check colormaps once
    plt.figure(figsize=(10,8))
    sns.heatmap(similarity_matrix, annot=True, fmt=".2f", xticklabels=hindex, yticklabels=hindex, cmap="YlGnBu")
    plt.title("Similarity Matrix")
    plt.xlabel("Files")
    plt.ylabel("Files")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    output_filename = "./static/similarityheatmap.png"
    plt.savefig(output_filename, format="png")
    plt.close() 

    third_elements = [sublist[2] for sublist in simlist]
    plaghighest = max(third_elements)

    

    # print(simlist)
    return simlist, lst, plaghighest, toplang

# p=input("Enter the directory path: ")

# print(calculate_similarity(p)) #comment out later
print("...similarity checked")