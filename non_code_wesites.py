from bs4 import BeautifulSoup
import requests
import random
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
def byjus(link,file):
    
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

def general(link,file):
    l = link.get_text()
    with open(filename, 'w') as file:
        for paragraph in l:
            text = paragraph.get_text() + "\n"
            file.write(text + '\n')
    

def wikipedia(link,file):
    paragraphs = link.find_all('p')
    with open(filename, 'w') as file:
        for paragraph in paragraphs:
            text = paragraph.get_text() + "\n"
            file.write(text + '\n')
    # ele = link.find('div', attrs={'class':'mw-page-container'})

    
    # with open(filename, 'w') as file:
    #     for e in ele:
    #         text = e.get_text() + '\n'
    #     if "Examples" in text:
    #         return
    #     file.write(text + '\n')
        

    


URL = "https://www.google.com/search?q="

HEADERS = ({'User-Agent' : random.choice(user_agents),
            'Accepted-Language' : 'en-US, en;q=0.5'})
# headers = {'User-Agent': }


print("Enter query to search")
str = input()
str = str.replace(" ","+")

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
    print(a)

q = 0
    
for a in answers:
    link_to_open = a
    filename = "answer{}.txt".format(q)
    q += 1
    print(filename)

    
    print("Opening link:", link_to_open)
    try:
        html_response = requests.get(link_to_open, headers=HEADERS)

        if (html_response.status_code != 200):
            continue
        #time.sleep(5)
        bs = BeautifulSoup(html_response.content, 'html.parser')

        if "byjus" in link_to_open: #https://byjus.com/biology/photosynthesis/
            byjus(bs,filename)

        elif "wikipedia" in link_to_open:
            wikipedia(bs,filename)
        
        # elif "blog.hubspot" in link_to_open:
        #     blog(bs,filename)
        
        # elif "stackoverflow" in link_to_open:
        #     freeCode(bs,filename)

        # elif "geeksforgeeks" in link_to_open:    
        #     gfg(bs,filename)

        else:
            general(bs,filename)

    except Exception as e:
        print(f"Failed to open link {link_to_open}: {e}")
