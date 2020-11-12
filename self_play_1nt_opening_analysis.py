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

def human_readable(hand):
    suits=[[],[],[],[]]
    for card in hand:
        if 'S' in card:
            temp=suits[0]
            temp.append(card[0])
            suits[0]=temp
        elif 'H' in card:
            temp = suits[1]
            temp.append(card[0])
            suits[1] = temp
        elif 'D' in card:
            temp = suits[2]
            temp.append(card[0])
            suits[2] = temp
        elif 'C' in card:
            temp = suits[3]
            temp.append(card[0])
            suits[3] = temp
    suits= ["".join(suit) for suit in suits]
    return suits

def is_stayman(hcp,dist):
    if hcp<9:
        return False
    if int(dist[0])==4 and int(dist[1])<5:
        return True
    if int(dist[1])==4 and int(dist[0])<5:
        return True
    return False

def is_balanced(hcp,dist):
    if '0' in dist or '1' in dist or '6' in dist:
        return False
    return True
def is_transfer(hcp,dist):
    if int(dist[0])>4 and int(dist[1])<4:
        return True
    if int(dist[1])>4 and int(dist[0])<4:
        return True
    return False

stayman_hands=[] # (bid, hcp, dist)
transfer_hands=[]
order = ['N', 'E', 'S', 'W']
suit_order={'S':0,'H':1,'D':2,'C':3,'N':None}
fake_transfers = 0
fake_staymans=0
for deal in all_plays:
    abbr={'N':'north','S':'south','E':'east','W':'west'}
    bid_index=order.index(deal['dealer'])
    n_opening=False
    for i in range(len(deal['history'])):
        bid=deal['history'][i]
        bidder=order[bid_index%4]
        bid_index +=1
        opening_index=i
        if bid == 'PA':
            continue
        if bid == '1N':
            opening_hand = deal[abbr[bidder]]
            n_opening=True
            break
        else:
            break
    if not n_opening:
        continue
    if not deal['history'][opening_index+1] =='PA':
        continue
    opener=order[(bid_index-1)%4]
    partner=order[(bid_index+1)%4]
    partner_hand=deal[abbr[partner]]
    partner_bid=deal['history'][opening_index+2]
    hcp_of_partner=points_of(partner_hand)
    dist_of_partner=distribution_of(partner_hand)

    if is_stayman(hcp_of_partner,dist_of_partner):
            #and not is_balanced(hcp_of_partner,dist_of_partner):
        stayman_hands.append((partner_bid,hcp_of_partner,dist_of_partner,deal['history'],human_readable(partner_hand)))

    elif is_transfer(hcp_of_partner,dist_of_partner):
        transfer_hands.append((partner_bid,hcp_of_partner,dist_of_partner,deal['history'],human_readable(partner_hand)))

    if partner_bid=='2D' and int(dist_of_partner[1])<5:
        fake_transfers +=1
    elif partner_bid=='2H' and int(dist_of_partner[0])<5:
        fake_transfers +=1
    elif partner_bid=='4H' and int(dist_of_partner[0])<5:
        fake_transfers +=1
    elif partner_bid=='4D' and int(dist_of_partner[1])<5:
        fake_transfers +=1
    elif partner_bid=='2C' and int(dist_of_partner[1])<4 and int(dist_of_partner[0])<4:
        fake_staymans += 1
count=0
for stayman_hand in stayman_hands:
    if stayman_hand[0]=='2C':
        count +=1
print('Stayman made when it is possible',count/len(stayman_hands))
print('Fake stayman rate:',fake_staymans/(fake_transfers+count))


count=0
for transfer_hand in transfer_hands:
    transfers=['2D','2H','4D','4H']
    if transfer_hand[0] in transfers:
        count +=1
print('Transfer made when it is possible: ',count/len(transfer_hands))
print('Fake transfer rate:',fake_transfers/(fake_transfers+count))

