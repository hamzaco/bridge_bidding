import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import Hand
from selenium.webdriver.chrome.options import Options
from Hand import the_deck
import os
import json
import io
import shutil
def alter_hands(hands):
    hands = "".join(hands)
    hands = hands.replace('S', ',')
    hands = hands.replace('H', ',')
    hands = hands.replace('D', ',')
    hands = hands.replace('C', ',')
    hands = hands.split(',')
    dealer = hands.pop(0)
    temp = ['S', 'W', 'N', 'E']
    dealer = temp[int(dealer) - 1]
    for i in hands:
        if i=='':
            hands.remove('')
    for i in range(len(hands), -1, -1):
        if i % 4 == 0:
            hands.insert(i, ' ')
        else:
            hands.insert(i, '.')
    hands.insert(0,'N:')
    hands = "".join(hands)
    return dealer,hands

def alter_play(play_line,hands_c):
    l=play_line
    if len(l)==0:
        return []

    for i in range(len(l)):
        l[i]=l[i][0:2]
    for a in l:
        a=a[0:2]
        try:
            a=int(a)
        except:
            a=a
        if isinstance(a,int):
            l.remove(str(a))

    if len(l)==0:
        return ""
    index=find_the_card(l[0],hands_c)
    while len(l)<4:
        l.append('-')
    l=[l[i-index] for i in range(len(l))]

    l = " ".join(l)
    return l


def find_the_card(card,hands):
    suit=card[0]
    suit_index={'S':0,'H':1,'D':2,'C':3}
    ind=suit_index[suit]
    for i in range(len(hands)):
        if card[1] in hands[i][ind]:
            return i
    return 3
def determine_the_winner(four_cards,contract,current_suit):
    distinct_cards=four_cards.copy()
    trump=contract[1]
    legit_cards=[]
    trump_cards=[]
    if trump=='N':
        for a_card in distinct_cards:
            if current_suit==a_card[0]:
                if a_card[1]=='A':
                    legit_cards.append((a_card,14))
                elif a_card[1]=='K':
                    legit_cards.append((a_card,13))
                elif a_card[1] == 'Q':
                    legit_cards.append((a_card,12))
                elif a_card[1] == 'J':
                    legit_cards.append((a_card,11))
                elif a_card[1] == 'T':
                    legit_cards.append((a_card,10))
                else:
                    legit_cards.append((a_card,int(a_card[1])))
        sorted_by_second = sorted(legit_cards, key=lambda tup: tup[1])
        return sorted_by_second[-1]
    else:
        for a_card in distinct_cards:
            if current_suit==a_card[0]:
                if a_card[1]=='A':
                    legit_cards.append((a_card,14))
                elif a_card[1]=='K':
                    legit_cards.append((a_card,13))
                elif a_card[1] == 'Q':
                    legit_cards.append((a_card,12))
                elif a_card[1] == 'J':
                    legit_cards.append((a_card,11))
                elif a_card[1] == 'T':
                    legit_cards.append((a_card,10))
                else:
                    legit_cards.append((a_card,int(a_card[1])))
            elif trump==a_card[0]:
                if a_card[1]=='A':
                    trump_cards.append((a_card,14))
                elif a_card[1]=='K':
                    trump_cards.append((a_card,13))
                elif a_card[1] == 'Q':
                    trump_cards.append((a_card,12))
                elif a_card[1] == 'J':
                    trump_cards.append((a_card,11))
                elif a_card[1] == 'T':
                    trump_cards.append((a_card,10))
                else:
                    trump_cards.append((a_card,int(a_card[1])))
        if len(trump_cards)>0:
            sorted_by_second = sorted(trump_cards, key=lambda tup: tup[1])
        else:
            sorted_by_second = sorted(legit_cards, key=lambda tup: tup[1])
        return sorted_by_second[-1]
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    l=[]
    for i in range(0, len(lst), n):
        l.append(" ".join(lst[i:i + n]))
    return l

def get_raw_score(record,vul):
    is_vul=False
    if record=="" or record[0]=='P' :
        return 'None',str(0),'Pass',str(0)
    level=int(record[0])
    trump=record[1]
    result=level+6
    factor=1
    is_doubled = 'X' in record
    if is_doubled:
        factor=2
    is_redoubled = 'XX' in record
    if is_redoubled:
        factor=4
    record.replace('X', '')
    record.replace('XX', '')
    declarer=record[2]
    if is_doubled:
        contract=record[0:1]+'X'
    elif is_redoubled:
        contract=record[0:1]+'X'
    else:
        contract=record[0:1]
    if declarer in vul:
        is_vul=True
    made=True
    over_trick=0
    if len(record)==3:
        record=record+'='
    if record[3]=='+':
        over_trick=int(record[4])
        result += over_trick
    elif record[3]=='-':
        under_trick=int(record[4])
        result -= under_trick

        made=False
    if made:
        if trump in ['H','S']:
            contract_points=(level+over_trick)*30*factor
        elif trump in ['D','C']:
            contract_points=(level+over_trick)*20*factor
        else:
            contract_points=(40+(level+over_trick-1)*30)*factor

        over_trick_points=0
        made_bonus=0
        game_points=0
        slam_bonus=0
        part_score_bonus=0

        if contract_points >= 100:
            game_points=300
            if is_vul:
                game_points +=200
        else:
            part_score_bonus=50
        if level==6:
            slam_bonus=750 if is_vul else 500
        elif level == 7:
            slam_bonus=1500 if is_vul else 1000
        if is_doubled or is_redoubled:
            made_bonus=25*factor
            over_trick_points = over_trick * factor * 50
        score= made_bonus+game_points+slam_bonus+over_trick_points+part_score_bonus+contract_points
        if declarer in ['N','S']:
            return declarer,'+'+str(score),contract,result
        return declarer, '-' + str(score),contract,result
    else:
        penalty=0
        if is_doubled or is_redoubled:
            temp=[100,300,500]
            temp_vul=[200,500,800]
            if under_trick<4:
                if is_vul:
                    penalty=temp_vul[under_trick-1]
                else:
                    penalty=temp[under_trick-1]
            else:
                if is_vul:
                    penalty=temp_vul[2]*(under_trick-3)*300
                else:
                    penalty=temp[2]*(under_trick-3)*300

            if is_redoubled:
                penalty *=2
        else:
            if is_vul:
                penalty=100*under_trick
            else:
                penalty=50*under_trick
        if declarer in ['E', 'W']:
            return declarer, '+' + str(penalty),contract,result
        return declarer, '-' + str(penalty),contract,result
path=os.getcwd()+'/All records'

tournaments= os.listdir(path)

matches_c=0
boards=0
bids=0
keywords=['vg','qx','mb','rs','pn','mc','pc','md','sv','pg','nt',]
keywords_wo_pg=['vg','qx','mb','rs','pn','mc','pc','md','sv']
for tournament in tournaments:
    print(tournament)
    matches=os.listdir(path+'/'+tournament)
    try:
        os.mkdir(path+' pbn/'+tournament)
    except:
        print("File exists")
        continue
    for match in matches:
        writing_lines = []
        f= open(path+'/'+tournament+'/'+match,'r',  errors='ignore')
        lines= f.read()
        f.close()
        matches_c +=1
        lines=lines.replace('\n','|')
        lines=lines.split('|',)
        temp=[]
        reading=False
        reading_decleration= False
        reading_play= False
        seperate_datas=[]
        for line in lines:
            if reading_decleration:
                if line =='mb':
                    continue
                temp.append(line)

                if line in keywords:
                    seperate_datas.append(temp)
                    temp = []
                    temp.append(line)
                    reading_decleration = False
                continue
            elif line=='mb':
                seperate_datas.append(temp)
                temp=[]
                temp.append(line)
                reading_decleration=True
                continue

            if reading_play:
                if line =='pc':
                    continue
                temp.append(line.upper())
                if line in keywords:
                    seperate_datas.append(temp)
                    temp = []
                    temp.append(line.upper())
                    reading_play = False
                continue
            elif line == 'pc':
                seperate_datas.append(temp)
                temp = []
                temp.append(line.upper())
                reading_play = True
                continue

            if line in keywords and not reading:
                temp.append(line)
                reading=True
            elif reading and line not in keywords:
                temp.append(line)
            elif line in keywords and reading:
                seperate_datas.append(temp)
                temp=[]
                temp.append(line)
                reading=True
            else:
                continue
        play_temp=[]
        play_records=[]
        declaration_records=[]
        writing_lines=[]
        writing_lines.append('% PBN 1.0')
        writing_lines.append('% EXPORT')
        writing_lines.append('%')
        vul_dic = {'b': 'All', 'o': 'None', 'e': 'EW', 'n': 'NS', 'w': 'EW', 's': 'NS', '0': 'None',
                   'B': 'All', 'O': 'None', 'E': 'EW', 'N': 'NS', 'W': 'EW', 'S': 'NS'}
        lead = {'S': 'W', 'W': 'N', 'N': 'E', 'E': 'S', 'None': 'None'}
        is_first=True
        is_first_rs=True
        vulnerability='o'
        for data in seperate_datas:
            if data[0]=='pg':
                continue
            elif data[0]=='mb':
                l=data[1:-1]
                l = ",".join(l)
                l = l.replace('p', 'Pass')
                l = l.replace('d', 'X')
                l = l.replace('r', 'XX')
                l = l.split(',')
                bids += len(l)
                l = [dec[0:2] if dec != 'Pass' else dec for dec in l]
                declaration_records=chunks(l,4)
            elif data[0]=='qx':
                #------------WRITING-------------------
                if is_first:
                    board_no = data[1][1:]
                    is_first=False
                    continue

                writing_lines.append('[Event \"' + tournament + '\"]')
                writing_lines.append('[Site \"00\"]')
                writing_lines.append('[Date \"00\"]')
                writing_lines.append('[Board ' + '\"' + board_no + "\"]")
                writing_lines.append('[West ' + '\"' + West1 + '\"]')
                writing_lines.append('[North ' + '\"' + North1 + '\"]')
                writing_lines.append('[East ' + '\"' + East1 + '\"]')
                writing_lines.append('[South ' + '\"' + South1 + '\"]')
                writing_lines.append('[Dealer \"' + dealer + '\"]')
                writing_lines.append('[Vulnerable \"' + vul_dic[vulnerability] + '\"]')
                writing_lines.append('[Deal \"' + hands + "\"]")
                record = hand_results.pop(0)
                declarer, score, contract, result = get_raw_score(record, vul_dic[vulnerability])
                writing_lines.append('[Declarer \"' + declarer + "\"]")
                writing_lines.append('[Contract \"' + contract + '\"]')
                writing_lines.append('[Result \"' + str(result) + '\"]')
                writing_lines.append('[HomeTeam \"' + home_team + '\"]')
                writing_lines.append('[Room \"Closed\"]')
                writing_lines.append('[Round \"00\"]')
                writing_lines.append('[Score \"NS ' + score + "\"]")
                writing_lines.append('[Section \"00\"]')
                writing_lines.append('[Table \"00\"]')
                writing_lines.append('[VisitTeam \"' + away_team + '\"]')
                writing_lines.append('[Auction \"' + dealer + '\"]')
                writing_lines.extend(declaration_records)
                writing_lines.append('[Play \"' + lead[declarer] + '\"]')
                writing_lines.extend(play_records)
                writing_lines.append('*')
                writing_lines.append('\n')
                #--------------------------------------
                board_no=data[1][1:]
                play_records = []
                declaration_records = []
            elif data[0]=='md':
                boards +=1
                dealer,hands=alter_hands(data[1])
                hands_c = hands.split(" ")
                hands_c.pop(0)
                hands_c.pop()
                hands_c = [hand.split(".") for hand in hands_c]
            elif data[0] == 'vg':
                temp=data[1].split(',')
                board_no=temp[3]
                home_team=temp[5]
                away_team=temp[7]
            elif data[0] == 'rs':
                if is_first_rs:
                    hand_results=data[1].split(',')
                    is_first_rs=False
            elif data[0] == 'pn':
                if is_first:
                    l=data[1].split(',')
                    if len(l)>=8:
                        North1 = l[0]
                        West1 = l[1]
                        South1 = l[2]
                        East1 = l[3]
                        North2 = l[4]
                        West2 = l[5]
                        South2 = l[6]
                        East2 = l[7]
            elif data[0]=='sv':
                vulnerability=data[1]
            elif data[0]=='PC':
                if len(play_temp)<4:
                    play_temp.extend(data[1:-1])
                if len(play_temp)==4:
                    l=alter_play(play_temp, hands_c)
                    play_records.append(l)
                    play_temp=[]

        f = open(path + ' pbn/' + tournament + '/' + match + '', 'w')
        for line in writing_lines:
            f.write(line + '\n')

        f.close()

print('Matches: '+str(matches_c))
print('Boards: '+str(boards))
print('Bids: '+str(bids))
