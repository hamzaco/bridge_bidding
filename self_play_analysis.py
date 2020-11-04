import json
from statistics import mean,stdev,median
import xlsxwriter
workbook = xlsxwriter.Workbook('Bidding Analysis.xlsx')
worksheet = workbook.add_worksheet('Opening Strategy')
writing_lines=[('Opening Bid','Min HCP','Max HCP','Min Suit Length','Max Suit Length','Mean of Suit Lengths')]
def points_of(hand):
    p=0
    for card in hand:
        if 'A' in card:
            p += 4
        elif 'K' in card:
            p +=3
        elif 'Q' in card:
            p +=2
        elif 'J' in card:
            p +=1
    return p

def distribution_of(hand):
    dist=[0,0,0,0]
    for card in hand:
        if 'S' in card:
            dist[0] += 1
        elif 'H' in card:
            dist[1] += 1
        elif 'D' in card:
            dist[2] += 1
        elif 'C' in card:
            dist[3] += 1
    dist=[str(i) for i in dist]
    return "".join(dist)


with open("4kselfgames.json") as fp:
    all_plays=json.load(fp)

opening_hands={} # (bid, hcp, dist)
order = ['N', 'E', 'S', 'W']
suit_order={'S':0,'H':1,'D':2,'C':3,'N':None}
print(len(all_plays))
for deal in all_plays:
    abbr={'N':'north','S':'south','E':'east','W':'west'}
    bid_index=order.index(deal['dealer'])
    for i in range(len(deal['history'])):
        bid=deal['history'][i]
        bidder=order[bid_index%4]
        bid_index +=1
        if bid != 'PA':
            hand=deal[abbr[bidder]]
            try:
                opening_hands[bid].append((hand,points_of(hand),distribution_of(hand)))
            except:
                opening_hands[bid]=[(hand,points_of(hand),distribution_of(hand))]
            break
for opening_bid in opening_hands:
    hcp_list=[]
    suit_length_list=[]
    opening_suit=opening_bid[1]
    for opening_hand in opening_hands[opening_bid]:
        hcp_list.append(opening_hand[1])
        if opening_suit=='N':
            continue
        suit_length_list.append(int(opening_hand[2][suit_order[opening_suit]]))
    hcp_list.sort()
    edges=int(len(hcp_list)/10)
    if edges == 0:
        edges=1
    if opening_bid=='5D':
        continue
    if opening_suit=='N' or opening_bid=='2C':
        writing_lines.append((opening_bid,min(hcp_list[edges:-edges]),max(hcp_list[edges:-edges]),'N/A','N/A','N/A'))
    else:
        suit_length_list.sort()
        writing_lines.append((opening_bid,min(hcp_list[edges:-edges]),max(hcp_list[edges:-edges]),
                              min(suit_length_list[edges:-edges]),max(suit_length_list[edges:-edges]),mean(suit_length_list[edges:-edges])))

for row in range(len(writing_lines)):
    for col in range(6):
        worksheet.write(row,col,writing_lines[row][col])
workbook.close()