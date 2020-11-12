import json
from statistics import mean,stdev,median
from self_play_1nt_opening_analysis import distribution_of,points_of,is_balanced,human_readable
import xlsxwriter
workbook = xlsxwriter.Workbook('Bidding Analysis.xlsx')
worksheet = workbook.add_worksheet('Opening Strategy')
writing_lines=[('Opening Bid','Min HCP','Max HCP','Min Suit Length','Max Suit Length','Mean of Suit Lengths')]


with open("4kselfgames.json") as fp:
    all_plays=json.load(fp)


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
        if bid=='4N':
            print(deal['history'])
            print(human_readable(deal[abbr[bidder]]))
            print(human_readable(deal[abbr[order[(bid_index+1)%4]]]))
            break