
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options,
                              executable_path='C:/Users/Lenovo/Desktop/chromedriver')  # Optional argument, if not specified will search path.
link="http://www.sarantakos.com/bridge/vugraph/newer.html"
path=os.getcwd()

driver.get(link)
total_match=0
tournaments=driver.find_elements_by_tag_name('a')
temp=[]
for tournament in tournaments:
    temp.append((tournament.text,tournament.get_attribute('href')))
tournaments=temp
print(len(tournaments))
for tournament in tournaments:
    driver.get(tournament[1])
    try:
        os.mkdir(os.path.join(path,tournament[0]))
    except OSError as error:
        continue
    matches=driver.find_elements_by_tag_name('a')
    temp=[]
    for match in matches:
        temp.append((match.text,match.get_attribute('href')))
    print(tournament[0])
    matches=temp
    try:
        matches.pop(-1)
    except:
        print('empty')
    print(matches)
    for match in matches:
        if isinstance(match[1],str):
            driver.get(match[1])
        else:
            continue
        try:
            records=driver.find_element_by_tag_name('pre').text
        except:
            print(match[1])
            continue
        try:
            f= open(os.path.join(path,tournament[0],match[0]+'.txt'),'x',encoding="utf-8")
        except:
            name=list(match[1])
            temp=name.copy()
            for char in name:
                if char == '.' or char=='/' or char==':':
                    temp.remove(char)
            name="".join(temp)
            f= open(os.path.join(path,tournament[0],name+'.txt'),'w',encoding="utf-8")
        f.write(records)
        total_match += 1
        f.close()



print(total_match)