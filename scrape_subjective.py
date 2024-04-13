from bs4 import BeautifulSoup
import requests
import random
import os
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
]
# import time

HEADERS = ({'User-Agent' : random.choice(user_agents),
            'Accepted-Language' : 'en-US, en;q=0.5'})

def byjus(link,filename):
    # filename="byjus.txt"
    #code_elements = bs.find_all('code', class_='language-css')
    ele = link.find('article')
    first_p_tag = ele.find('p')
    ptags=ele.find_all('p')
    # code_elements = link.find('div',attrs={'class':'bgc-white p30 mb20 pm15'})

    current_tag = first_p_tag
    with open(filename, 'w') as file:
        text = current_tag.get_text() + '\n'
        if "also read" in text:
            return
        file.write(text + '\n')
        for p in ptags:
            p1 = p.get_text()
            if(p1 == text):
                continue
            elif("also read" in p1):
                return
        
            else:
               file.write(p1 + '\n') 
# Function to save general content to a file
def general(link, filename):
    try:
        all_text = link.get_text()
        lines = all_text.splitlines()
        stripped_lines = [line.strip() for line in lines]
        non_empty_lines = [line for line in stripped_lines if line]

        print("Creating a file - ",filename)
        with open(filename, 'w') as file:
            for string in non_empty_lines:
                file.write(string + '\n')
        # l = all_text.splitlines()
        # l = link.get_text()
        # with open(filename, 'w') as file:
        #     for paragraph in all_text:
        #         text = paragraph.get_text() + "\n"
        #         file.write(text + '\n')
    except AttributeError as e:
        print("Error occurred while extracting text:", e)

# def general(link,filename):
#     # filename="gen.txt"
#     all_text = link.get_text()

#     # l = all_text.splitlines()
#     # l = link.get_text()
#     with open(filename, 'w') as file:
#         for paragraph in all_text:
#             text = paragraph.get_text() + "\n"
#             file.write(text + '\n')

def britannica(link,filename):
    # filename="brit.txt"
    text_all = link.find_all('p',attrs={'class':'topic-paragraph'})
    
    with open(filename, 'w') as file:
        for paragraph in text_all:
            text = paragraph.get_text() + "\n"
            file.write(text + '\n')

def khanacademy(link,filename):
    # filename="khanacademy.txt"
    l=link.find_all('div',attrs={'class':"perseus-renderer perseus-renderer-responsive"})
    with open(filename,'w') as file:
        for paragraph in l:
            text = paragraph.get_text() + "\n"
            file.write(text + '\n')
    

def wikipedia(link,filename):
    # filename="wiki.txt"
    paragraphs = link.find_all('p')
    with open(filename, 'w') as file:
        for paragraph in paragraphs:
            text = paragraph.get_text() + "\n"
            file.write(text + '\n')


def get_data(str):   
        str = str.replace(" ","+")
        URL = "https://www.google.com/search?q="
        URL += str
        print(URL)

        webpage = requests.get(URL,headers=HEADERS) 

        soup = BeautifulSoup(webpage.content, 'html.parser')

        links = soup.find_all('a',attrs={'jsname' : 'UWckNb'})

        answers = []

        for l in links:
            page_href = l['href']
            answers.append(page_href) 
            
        for a in answers:
            link_to_open = a
            print("Opening link:", link_to_open)
            html_response = requests.get(link_to_open, headers=HEADERS)
            #time.sleep(5)
            bs = BeautifulSoup(html_response.content, 'html.parser')
    
            if "byjus" in link_to_open: #https://byjus.com/biology/photosynthesis/
                # filename=a[12:16]
                filename = os.path.join('submissions', 'testdir', 'byjus.txt')
                byjus(bs,filename)

            elif "wikipedia" in link_to_open:
                # filename=a[11:16]
                filename = os.path.join('submissions', 'testdir', 'wikipedia.txt')
                wikipedia(bs,filename)
            
            elif "britannica" in link_to_open:
                # filename=a[12:16]
                filename = os.path.join('submissions', 'testdir', 'britannica.txt')
                britannica(bs,filename)
            
            elif "khanaacademy" in link_to_open:
                # filename=a[12:16]
                filename = os.path.join('submissions', 'testdir', 'khanaacademy.txt')
                khanacademy(bs,filename)
            
            else:
                filename=os.path.join('submissions', 'testdir',a[12:16] + '.txt')
                # filename = os.path.join('submissions', 'bloghubspot.txt')
                general(bs,filename)
