#! /usr/bin/env python


#pid is the key

players={}
myid=''
myseat=0
myjetton=0
mymoney=0
num_player=0
numhand=0
totalplay=0
value={'A':14,'J':11,'Q':12,'K':13}
for val in range(9):
	value[str(val+2)]=val+2

color=('SPADES','HEARTS','CLUBS','DIAMONDS')

nut_hand=('HIGH_CARD','ONE_PAIR','TWO_PAIR','THREE_OF_A_KIND','STRAIGHT','FLUSH','FULL_HOUSE','FOUR_OF_A_KIND','STRAIGHT_FLUSH')

verystrong=('AA','AAs','KK','KKs','QQ','QQs','AKs','AK')

strong=('JJ','JJs','1010','1010s','99','99s','AQs','AQ','AJs')

medio=('AJ','A10s','A10o','KQs','KQ')

gamble=('88','88s','77','77s','66','66s','55','55s','44','44s','33','33s','22','22s','KJs','K10s','QJs','Q10s','J10s','109s')

mingle=('KJ','K10','QJ','Q10','J10','A9s','A8s','A7s','A6s','A5s','A4s','A3s','A2s','K9s','98s','97s','87s')
#yi xia shi yi lun yao bei chu shi hua de 
last_action=''
stage=''
community=[]
communityvalue=[]
commonvalue=[]
communitycolor={'SPADES':0,'HEARTS':0,'CLUBS':0,'DIAMONDS':0}
communitynumcolor=[communitycolor['SPADES'],communitycolor['HEARTS'],communitycolor['CLUBS'],communitycolor['DIAMONDS']]
turn=''
river='' 
big_blind=''
small_blind=''
button=''
hold=[]
current_pot=0
current_bb=0
current_bet=0
bets=0
isstrong=0
current_playerid=[]
color=''
numcolor=0
myhands=''
my_nut_hand=''
signature_sequence=''
common_sequence=''
gaplist=[]
commongaplist=[]
numraise=0
numcall=0
numfold=0
numcheck=0
numallin=0
seatchange=0
