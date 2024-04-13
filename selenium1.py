from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service 
from bs4 import BeautifulSoup 
import time
import os

def gptscrape(initialprompt,gecko_driver_path1,p):
    i = 0
    print(p,"\n\n\n")

    def search(path,p,i):   #path prompt i

        gecko_driver_path = gecko_driver_path1 
        firefox_binary_path = '/usr/bin/firefox'

        firefox_options = webdriver.FirefoxOptions() 
        firefox_options.binary_location = firefox_binary_path

        service = Service(executable_path=gecko_driver_path) 
        driver = webdriver.Firefox(options=firefox_options, service=service)

        url = "https://chat.openai.com/" 
        driver.get(url)

        search_box = driver.find_element(By.CSS_SELECTOR, "textarea#prompt-textarea") 
        search_box.send_keys(p)

        search_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='send-button']") 
        search_button.click()

        time.sleep(10)

        page_source = driver.page_source 
        soup = BeautifulSoup(page_source, 'html.parser')
        # print(soup)

        div_element = soup.find("div", attrs={'class':'relative flex w-full flex-col agent-turn'}) 
        # print(div_element)
        # print("..................................................................................................")
        print(path,"\n\n\n")

        # subdirectory = p
        # new_path = str(subdirectory) + str(os.listdir(p))
        # print(new_path)

        # if not os.path.exists(new_path):
        #     os.makedirs(new_path)

        with open(os.path.join(path, 'chatgpt{}.txt'.format(i)), 'w') as file:
            # Write some text to the file
            for d in div_element:
                file.write(d.get_text()+"\n")

        # time.sleep(5) 
        driver.quit()


    # p = input("Enter string: ")
    prompt1 = "generate 3 ways to ask the question : " + initialprompt
    search(p,prompt1,i)
    i+=1

    file_path1 = os.path.join(p, 'chatgpt0.txt')
    with open(file_path1, 'r') as file:
        text = file.read()
        parts = text.split('"')
        print(parts)
        for part in parts[1::2] :
            print(part)
            search(p,part, i)
            i+=1

def ai_detection(prompt, filepath):
    with open("geco.txt", "r") as file:
        first_line = file.readline().strip()
    gptscrape(str(prompt),first_line, filepath)
