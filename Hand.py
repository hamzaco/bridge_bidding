
import random
class Hand:
    def __init__(self,spades='',hearts='',diamonds='',clubs=''):
        self.spades=spades
        self.hearts=hearts
        self.diamonds=diamonds
        self.clubs=clubs
        self.all_cards=[] # 'SJ' 'D2'
        self.hcp=0

    def get_hcp(self):
        all_cards=self.spades+self.clubs+self.hearts+self.diamonds
        hcp=0
        for card in all_cards:
            if card=='J':
                hcp +=1
            elif card=='Q':
                hcp +=2
            elif card == 'K':
                hcp +=3
            elif card == 'A':
                hcp +=4
        self.hcp=hcp
        return hcp

    def get_suits(self):
        return [self.spades,self.hearts,self.diamonds,self.clubs]
    def add_card(self,card):
        self.all_cards.append(card)
        if card[0]=='S':
            self.spades += card[1]
        elif card[0]=='H':
            self.hearts += card[1]
        elif card[0]=='D':
            self.diamonds += card[1]
        else:
            self.clubs += card[1]
    def get_distribution(self):
        return [len(self.spades),len(self.hearts),len(self.diamonds),len(self.clubs)]
    def __str__(self):
        return 'S'+self.spades+'H'+self.hearts+'D'+self.diamonds+'C'+self.clubs
    def to_String(self):
        return 'S' + self.spades + 'H' + self.hearts + 'D' + self.diamonds + 'C' + self.clubs
the_deck=[]
a_suit='23456789TJQKA'
suits=['spades','hearts','diamonds','clubs']
point_of={'J':1, 'Q':2, 'K':3, 'A':4}
honours=['A','A','A','A','K','K','K','K','Q','Q','Q','Q','J','J','J','J']
honour_with_suit=['SA','HA','DA','CA','SK','HK','DK','CK','SQ','HQ','DQ','CQ','SJ','HJ','DJ','CJ']
non_honours_super=['2','3','4','5','6','7','8','9','T']
POS = {c:p for (p, c) in enumerate(a_suit)}
for card in a_suit:
    the_deck.append('S'+card)
    the_deck.append('H'+card)
    the_deck.append('D'+card)
    the_deck.append('C'+card)

def random_hand(the_deck):
    hand=Hand()
    spades=''
    clubs=''
    hearts=''
    diamonds=''
    a_deck=the_deck.copy()
    random.shuffle(a_deck)
    for i in range(13):
        card=a_deck.pop()
        if card[0]=='S':
            spades += card[1]
        elif card[0]=='H':
            hearts += card[1]
        elif card[0]=='D':
            diamonds += card[1]
        elif card[0]=='C':
            clubs += card[1]
    spades = list(spades)
    hearts = list(hearts)
    diamonds = list(diamonds)
    clubs = list(clubs)
    spades.sort(key=POS.get)
    hearts.sort(key=POS.get)
    clubs.sort(key=POS.get)
    diamonds.sort(key=POS.get)
    hand.spades=''.join(spades)
    hand.hearts=''.join(hearts)
    hand.diamonds=''.join(diamonds)
    hand.clubs=''.join(clubs)
    return hand,a_deck

def random_hand_restrictions(the_deck,restrictions): # restrictions (a suit,number of cards) , (hcp,points), (hand dist,a distribution)
    for restriction in restrictions:
        if restriction[0]=='hcp':
            current=0
            hand_honours=[]
            objective=restriction[1]
            deficit= objective-current
            left_honours=honours.copy()
            while deficit != 0:
                if deficit<0:
                    current = 0
                    hand_honours = []
                    objective = restriction[1]
                    deficit = objective - current
                    left_honours = honours.copy()
                if deficit==1:
                    if 'J' in left_honours:
                        deficit=0
                        hand_honours.append('J')
                    else:
                        current = 0
                        hand_honours = []
                        objective = restriction[1]
                        deficit = objective - current
                        left_honours = honours.copy()
                random.shuffle(left_honours)
                honour=left_honours.pop()
                hand_honours.append(honour)

        elif restriction[0]=='S':
            random.shuffle(a_suit)
            spades=a_suit[0:restriction-1]
            spades=''.join(spades)

        elif restriction[0]=='H':
            random.shuffle(a_suit)
            hearts=a_suit[0:restriction-1]
            hearts=''.join(hearts)

        elif restriction[0]=='D':
            random.shuffle(a_suit)
            dia=a_suit[0:restriction-1]
            dia=''.join(dia)

        elif restriction[0]=='C':
            random.shuffle(a_suit)
            clubs=a_suit[0:restriction-1]
            clubs=''.join(clubs)

class Deal:
    def __init__(self,south=None,west=None,north=None,east=None,number=0,vulnerability=None):
        self.south=south
        self.west=west
        self.north=north
        self.east=east
        self.number=number
        self.vulnerability=vulnerability # b: both, o: none, w: EW, n: NS
    def get_distribution_of_suit(self,suit):
        if suit=='S':
            return [len(self.south.spades),len(self.west.spades),len(self.north.spades),len(self.east.spades)]
        if suit=='H':
            return [len(self.south.hearts),len(self.west.hearts),len(self.north.hearts),len(self.east.hearts)]
        if suit=='D':
            return [len(self.south.diamonds),len(self.west.diamonds),len(self.north.diamonds),len(self.east.diamonds)]
        if suit=='C':
            return [len(self.south.clubs),len(self.west.clubs),len(self.north.clubs),len(self.east.clubs)]

    def get_distribution_of_hcp(self):
        return [self.south.get_hcp(),self.west.get_hcp(),self.north.get_hcp(),self.east.get_hcp()]

    def to_String(self):
        return self.south.to_String()+'%2C'+self.west.to_String()+'%2C'+self.north.to_String()+'%2C'
def random_deal():
    S,left=random_hand(the_deck)
    W,left=random_hand(left)
    N,left=random_hand(left)
    E,left=random_hand(left)
    return Deal(S,W,N,E)

def random_balanced_hand(hcp,four_major=True,left=[]):
    current = 0
    hand= Hand()
    hand_honours = []
    left_honours = honour_with_suit.copy()
    left_honours= list(set(left_honours).intersection(set(left)))
    non_honours_spades = ['S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'ST']
    non_honours_hearts = ['H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'HT']
    non_honours_diamonds = ['D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DT']
    non_honours_clubs = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CT']
    non_honours_spades= list(set(non_honours_spades).intersection(set(left)))
    non_honours_hearts= list(set(non_honours_hearts).intersection(set(left)))
    non_honours_diamonds= list(set(non_honours_diamonds).intersection(set(left)))
    non_honours_clubs= list(set(non_honours_clubs).intersection(set(left)))

    #first choose honours
    while current< hcp[0] or current > hcp[1] :
        if current > hcp[1]:
            current = 0
            hand_honours = []
            hand = Hand()
            left_honours = honour_with_suit.copy()
            left_honours = list(set(left_honours).intersection(set(left)))
        random.shuffle(left_honours)
        honour = left_honours.pop()
        current += point_of[honour[1]]
        hand_honours.append(honour)
        hand.add_card(honour)

    #prevent any shortness
    random.shuffle(non_honours_spades)
    while len(hand.spades)<2 or (four_major=='spades' and len(hand.spades)<4):
        hand.add_card(non_honours_spades.pop())

    random.shuffle(non_honours_hearts)
    while len(hand.hearts) < 2 or (four_major=='hearts' and len(hand.hearts)<4):
        hand.add_card(non_honours_hearts.pop())

    random.shuffle(non_honours_diamonds)
    while len(hand.diamonds) < 2:
        hand.add_card(non_honours_diamonds.pop())

    random.shuffle(non_honours_clubs)
    while len(hand.clubs) < 2:
        hand.add_card(non_honours_clubs.pop())

    #coomplete the hand
    while len(hand.all_cards) < 13:
        suit=random.choice(suits)
        any_5_card_suit=0
        if suit=='spades' and len(hand.spades) <4-any_5_card_suit:
            if not four_major and len(hand.spades)>=4:
                continue
            hand.add_card(non_honours_spades.pop())
        elif suit=='hearts' and len(hand.hearts) <4-any_5_card_suit:
            if not four_major and len(hand.hearts)>=4:
                continue
            hand.add_card(non_honours_hearts.pop())
        elif suit=='diamonds' and len(hand.diamonds) <5-(any_5_card_suit*2):
            hand.add_card(non_honours_diamonds.pop())
            if len(hand.diamonds)==5:
                any_5_card_suit=1
        elif suit=='clubs' and len(hand.clubs)<5-(any_5_card_suit*2):
            hand.add_card(non_honours_clubs.pop())
            if len(hand.clubs)==5:
                any_5_card_suit=1
    left= set(left).difference(set(hand.all_cards))
    return hand,list(left)

def is_a_opening_hand(hand):
    if hand.get_hcp()>11:
        return True
    return is_a_weak_opening_hand(hand)

def is_a_weak_opening_hand(hand):
    return is_2_weak_opening_hand(hand) or is_3_weak_opening_hand(hand) or is_4_weak_opening_hand(hand)

def is_2_weak_opening_hand(hand):
    suits=hand.get_suits()
    hcp=hand.get_hcp()
    if hcp <= 5:
        return False
    possibles=['A','KJT','QJT','KQ','KT9','QT9']
    colors=['S','H','D','C']
    i=0
    for any_suit in suits:
        if len(any_suit)==6:
            for a in possibles:
                if set(a).issubset(set(any_suit)):
                    return True,colors[i]
        i +=1
    return False, None


def is_3_weak_opening_hand(hand):
    suits=hand.get_suits()
    hcp=hand.get_hcp()
    if hcp <= 5:
        return False
    possibles=['A','KJT','QJT','KQ','KT9','QT9']
    colors=['S','H','D','C']
    i=0
    for any_suit in suits:
        if len(any_suit)==7:
            for a in possibles:
                if set(a).issubset(set(any_suit)):
                    return True,colors[i]
        i +=1
    return False, None

def is_4_weak_opening_hand(hand):
    suits=hand.get_suits()
    hcp=hand.get_hcp()
    if hcp <= 5:
        return False
    possibles=['A','KJT','QJT','KQ','KT9','QT9']
    colors=['S','H','D','C']
    i=0
    for any_suit in suits:
        if len(any_suit)==8:
            for a in possibles:
                if set(a).issubset(set(any_suit)):
                    return True,colors[i]
        i +=1
    return False, None

def is_1N_opening(hand):
    dist=hand.get_distribution()
    if dist[0] >4:
        return False
    if dist[1] >4:
        return False
    dist.sort()
    balanced_distributions=[[2,3,4,4],[2,3,3,5],[3,3,3,4]]
    if dist in balanced_distributions and hand.get_hcp()>=15 and hand.get_hcp()<=17:
        return True
    return False

def is_2N_opening(hand):
    dist=hand.get_distribution()
    dist.sort()
    balanced_distributions=[[2,3,4,4],[2,3,3,5],[3,3,3,4]]
    if dist in balanced_distributions and hand.get_hcp()>=20 and hand.get_hcp()<=21:
        return True
    return False

def is_2C_opening(hand):
    dist=hand.get_distribution()
    dist.sort()
    balanced_distributions=[[2,3,4,4],[2,3,3,5],[3,3,3,4]]
    if hand.get_hcp()>=22:
        return True
    return False

def get_opening(hand):
    if is_1N_opening(hand):
        return '1N'
    if is_2C_opening(hand):
        return '2C'
    if is_2N_opening(hand):
        return '2N'
    if is_a_opening_hand(hand):
        dist=hand.get_distribution()
        if dist[0]>=5:
            return '1S'
        elif dist[1]>=5:
            return '1H'
        else:
            if dist[2]>dist[3]:
                return '1D'
            elif dist[2]<dist[3]:
                return '1C'
            elif dist[2]==dist[3]:
                if dist[2]==3:
                    return '1C'
                else:
                    return '1D'
    check, suit = is_2_weak_opening_hand()
    if check:
        return '2'+suit
    check, suit = is_3_weak_opening_hand()
    if check:
        return '3' + suit
    check, suit = is_4_weak_opening_hand()
    if check:
        return '4' + suit
    return 'p'
