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
def general(soup,filename):
    
    all_text = soup.get_text()
    
    #q+=1
    lines = all_text.splitlines()
    with open(filename, 'w') as file:
        for string in lines:
            file.write(string + '\n')
    print("Completed the file - \n",filename)


def blog(link,filename):
    
    code_elements = link.find_all('CodeMirror-code')
    with open(filename, 'w') as file:
        for code_element in code_elements:
            code_text = code_element.get_text()
            file.write(code_text + '\n')
    print("Completed the file - \n",filename)


def freeCode(link,filename):
    
    #code_elements = bs.find_all('code', class_='language-css')
    code_elements = link.find_all('code')
    with open(filename, 'w') as file:
        for code_element in code_elements:
            code_text = code_element.get_text()
            file.write(code_text + '\n')
    print("Completed the file - \n",filename)

def programiz(link,filename):
    # filename="programiz.txt"
    #code_elements = bs.find_all('code', class_='language-css')
    code_elements = link.find_all('code')
    with open(filename, 'w') as file:
        for code_element in code_elements:
            code_text = code_element.get_text()
            file.write(code_text + '\n')
    print("Completed the file - \n",filename)

def w3(link,filename):
    # filename="w3.txt"
    code_content= link.find_all('div',attrs={'class':'w3-example'})
    with open(filename, 'w') as file:
        for c in code_content:
            code_text = c.get_text()
            file.write(code_text + '\n')
    print("Completed the file - \n",filename)

def gfg(link,filename):
    # filename="gfg.txt"
    td_snips = link.find_all('td',attrs={'class':'code'})
    if td_snips:
        with open(filename, 'w') as file:
            for t in td_snips:
                code_text = t.get_text()
                file.write(code_text + '\n')
        print("Completed the file - \n",filename)  
    else:
        code_elements = link.find_all('code')
        with open(filename, 'w') as file:
            for t in code_elements:
                code_text = t.get_text()
                file.write(code_text + '\n')
        print("Completed the file - \n",filename) 

def happycoding(link,filename):
    # filename="happycoding.txt"
    code_content= link.find_all('div',{'class':'language-java highlighter-rouge'})
    with open(filename, 'w') as file:
        for c in code_content:
            code_text = c.get_text()
            file.write(code_text + '\n')
    print("Completed the file - \n",filename)  



def get_code(str):
       
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

            if "freecodecamp" in link_to_open:
                filename = os.path.join('submissions', 'testdir', 'freecodecamp.txt')
                freeCode(bs,filename)

            elif "w3schools" in link_to_open:
                # filename=a[12:16] + '.txt'
                filename = os.path.join('submissions', 'testdir', 'w3schools.txt')
                w3(bs,filename)
            
            elif "blog.hubspot" in link_to_open:
                # filename=a[12:16] + '.txt'
                filename = os.path.join('submissions', 'testdir', 'bloghubspot.txt')
                blog(bs,filename)
            
            elif "stackoverflow" in link_to_open:
                # filename=a[12:16] + '.txt'
                filename = os.path.join('submissions', 'testdir', 'stackoverflow.txt')
                freeCode(bs,filename)

            elif "geeksforgeeks" in link_to_open:  
                # filename=a[12:20] + '.txt'  
                filename = os.path.join('submissions', 'testdir', 'geeksforgeeks.txt')
                gfg(bs,filename)

            elif "happycoding" in link_to_open:
                # filename=a[12:16] + '.txt'
                filename = os.path.join('submissions', 'testdir', 'happycoding.txt')
                happycoding(bs,filename)


            elif "programiz" in link_to_open:
                # filename=a[12:16] + '.txt'
                filename = os.path.join('submissions', 'testdir', 'programiz.txt')
                programiz(bs,filename)
            else:
                filename=os.path.join('submissions', 'testdir',a[12:16] + '.txt')
                # filename = os.path.join('submissions', 'freecodecamp.txt')
                general(bs,filename)

    # except Exception as e:
    #     print(f"Failed to open link {link_to_open}: {e}")