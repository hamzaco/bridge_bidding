


import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import Hand
from selenium.webdriver.chrome.options import Options
from Hand import the_deck
"""
t=time.time()
driver = webdriver.Chrome('C:/Users/Lenovo/Desktop/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://dds.bridgewebs.com/bsol2/ddummy.htm?club=chrome_ext&file=https://mirgo2.co.uk/bridgesolver/blank_pbn/blank.pbn')"""

"""print('Give me a bord pls:')

button = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/div/table[1]/tbody/tr/th/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/button[2]")
ActionChains(driver).click(button).perform()

vul=input('Vulnerability(All, None, EW, NS): ')
button=driver.find_element(vul)
button.click()
contract= input('Contract (S:spades, H: hearts, D: diamonds, C: clubs: N: nt) : ')
declarer= input('Declarer(N,S,E,W): ')
if declarer=='S':
    declarer='1'
elif declarer=='W':
    declarer='2'
elif declarer=='N':
    declarer='3'
else:
    declarer='4'


hand_records=''
print("Give me the hand of SOUTH please. 23456789TJQKA descending order")
spades= input("Spades: ")
hand_records +='S'+spades
hearts= input("Hearts: ")
hand_records +='H'+hearts
dia= input("Diamonds: ")
hand_records +='D'+dia
clubs= input("Clubs: ")
hand_records +='C'+clubs+'%2C'
print("Give me the hand of WEST please. 23456789TJQKA descending order")
spades= input("Spades: ")
hand_records +='S'+spades
hearts= input("Hearts: ")
hand_records +='H'+hearts
dia= input("Diamonds: ")
hand_records +='D'+dia
clubs= input("Clubs: ")
hand_records +='C'+clubs+'%2C'
print("Give me the hand of NORTH please. 23456789TJQKA descending order")
spades= input("Spades: ")
hand_records +='S'+spades
hearts= input("Hearts: ")
hand_records +='H'+hearts
dia= input("Diamonds: ")
hand_records +='D'+dia
clubs= input("Clubs: ")
hand_records +='C'+clubs+'%2C'
"""
made_count_w_5_card=0
all_count_w_5_card=0
made_count_other=0
sample_size=100
declarer='1'
board_no='1'
vul='o'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options,
                              executable_path='C:/Users/Lenovo/Desktop/chromedriver')  # Optional argument, if not specified will search path.
for i in range(100):
    deal=Hand.random_deal()
    a_deck=the_deck.copy()
    #1NT opening analysis
    deal.south,a_deck=Hand.random_balanced_hand(hcp=(16,17), four_major= 0, left=a_deck)
    deal.north,a_deck= Hand.random_balanced_hand(hcp=(8,8),four_major=0, left=a_deck)
    deal.west,_= Hand.random_hand(a_deck)
    hand_records= deal.to_String()
    print(deal.north.get_hcp())
    link = 'https://www.bridgebase.com/tools/handviewer.html?bbo=y&lin=pn|a,a,a,a|st%7C%7Cmd%7C'
    contract='3N'
    link = link+declarer+hand_records+'%7Crh%7C%7Cah%7CBoard%20'+board_no+'%7Csv%7C'+vul+'%7Cmb%7C'+contract+'%7Cmb'

    driver.get(link+'%7Cp%7Cmb%7Cp%7Cmb%7Cp%7Cpc')

    gib= driver.find_element_by_id("gibButton")
    gib.click()
    tricks= driver.find_elements_by_class_name("gibDivStyle")
    while len(tricks)==0:
        tricks = driver.find_elements_by_class_name("gibDivStyle")
    made=True
    good_lead=0
    for trick in tricks:
        color = trick.get_attribute("style")
        if color[16:19] == '203':
            good_lead +=1
            made=False
    print(made)
    made_prob=(13-good_lead)/13
    dist = deal.north.get_distribution()
    dist.sort()
    if dist[-1]==5:
        all_count_w_5_card += 1
        print('ahha')
        if made:
            made_count_w_5_card += made_prob
    elif made:
        made_count_other += made_prob
print(made_count_w_5_card/all_count_w_5_card)
print(made_count_other/(sample_size-all_count_w_5_card))







