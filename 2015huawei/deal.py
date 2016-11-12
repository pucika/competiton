#! /usr/bin/env python
import statistic
import sys
import judge
import time
import re
class player:
	def __init__(self,s):
		if s[0]=='button:':
			#print(s)
			self.pid=s[1]
			self.jetton=int(s[2])
			self.money=int(s[3])
			self.seat=0
			self.bet=0
			statistic.button=self.pid
		elif s[0]=='small':
			#print(s)
			self.pid=s[2]
			self.jetton=int(s[3])
			self.money=int(s[4])
			self.seat=0
			self.bet=0
			statistic.small_blind=self.pid
		elif s[0]=='big':
			#print(s)
			self.pid=s[2]
			self.jetton=int(s[3])
			self.money=int(s[4])
			self.seat=0
			self.bet=0
			statistic.big_blind=self.pid
		else:
			#print(s)
			self.pid=s[0]
			self.jetton=int(s[1])
			self.money=int(s[2])
			self.seat=0
			self.bet=0
class cards:
	def __init__(self,s):
		s=s.split(' ')
		self.value=s[1]
		self.color=s[0]

def cardclass():
	statistic.communityvalue=[]
	statistic.numcolor=0
	for s in statistic.community:
		statistic.communityvalue.append(statistic.value[s.value])
	#print(statistic.communityvalue)
	statistic.communityvalue.sort()
	statistic.gaplist=[]
	statistic.gaplist.append(statistic.communityvalue[0])
	for s in statistic.community:
		if statistic.color==s.color:
			statistic.numcolor=statistic.numcolor+1
	for i in range(1,len(statistic.communityvalue)):
		statistic.gaplist.append(statistic.communityvalue[i]-statistic.communityvalue[i-1])
	statistic.signature_sequence=''
	for s in statistic.gaplist:
		statistic.signature_sequence=statistic.signature_sequence+str(s)
	statistic.communityvalue=statistic.communityvalue[::-1]
	if re.match(r'^(\d*)1111(\d*)$',statistic.signature_sequence) and statistic.numcolor==5:
		statistic.my_nut_hand='STRAIGHT_FLUSH'
	elif re.match(r'^(\d*)000(\d*)$',statistic.signature_sequence):
		statistic.my_nut_hand='FOUR_OF_A_KIND'
	elif re.match(r'^(\d*)00(\d)0(\d*)$',statistic.signature_sequence) or re.match(r'^(\d*)0(\d)00(\d*)$',statistic.signature_sequence):
		statistic.my_nut_hand='FULL_HOUSE'
	elif statistic.numcolor==5:
		statistic.my_nut_hand='FLUSH'
	elif re.match(r'^(\d*)1111(\d*)$',statistic.signature_sequence):
		statistic.my_nut_hand='STRAIGHT'
	elif re.match(r'^(\d*)00(\d*)$',statistic.signature_sequence):
		statistic.my_nut_hand='THREE_OF_A_KIND'
	elif re.match(r'^(\d*)0(\d*)0(\d*)$',statistic.signature_sequence):
		statistic.my_nut_hand='TWO_PAIR'
	elif re.match(r'^(\d*)0(\d*)$',statistic.signature_sequence):
		statistic.my_nut_hand='ONE_PAIR'
	else:
		statistic.my_nut_hand='HIGH_CARD'
	print statistic.signature_sequence	
	print statistic.my_nut_hand


def deal_msg(msg,client):
	if 'inquire/ '==msg[0]:
		print 'inquire:'
		statistic.numraise=0
		statistic.numcall=0
		statistic.numfold=0
		statistic.numallin=0
		statistic.current_bet=0
		print statistic.last_action
		if statistic.last_action not in ('fold','all-in'):
			print msg
			end=msg.index('/inquire ')
			statistic.current_pot=int(msg[end-1].split(' ')[2])
			print statistic.current_pot
			inquireinfo=msg[1:end-1]
			for s in inquireinfo:
				s=s.split(' ')
				statistic.players[s[0]].jetton=int(s[1])
				statistic.players[s[0]].money=int(s[2])
				statistic.players[s[0]].bet=int(s[3])
				if not statistic.current_bet:
					statistic.current_bet=int(s[3])
					print statistic.current_bet
				if s[4].startswith('raise'):
					statistic.numraise=statistic.numraise+1
				if s[4].startswith('call'):
					statistic.numcall=statistic.numcall+1
				if s[4].startswith('fold'):
					statistic.numfold=statistic.numfold+1
				if s[4].startswith('check'):
					statistic.numcheck=statistic.numcheck+1
				if s[4].startswith('all_in'):
					statistic.numallin=statistic.numallin+1
			print 'in judge'
			if not statistic.samestage:
				statistic.samestage=1
			myaction=judge.judge()
			
			print myaction
		#while not client.send(myaction):
		#	time.sleep(0.01)
			#time.sleep(0.3)
		#client.send(myaction)
			if myaction:
				#while not client.send(myaction):
				#	print 'send'
				#	time.sleep(0.06)
				client.send(myaction)
				print 'have send'
		else:
			print 'no need '
		#time.sleep(0.5)		
	#try:
	#	client.send(myaction)
	#	#client.send('check')
	#except socket.error,arg:
	#	(errno,err_msg)=arg
	#	print "Connect server failed: %s, errno=%d" % (err_msg,errno)
	elif 'game-over '==msg[0]:
		print('game-over')
		client.close()
		sys.exit()
	elif 'seat/ '==msg[0]:
		end=msg.index('/seat ')
		seatinfo=msg[1:end]
		#print seatinfo
		count=0
		if not statistic.players:
			for s in seatinfo:
				s=s.split(' ')
				play=player(s)
				statistic.players[play.pid]=play
		statistic.current_playerid=[]
		for s in seatinfo[3:]:
			s=s.split(' ')
			statistic.players[player(s).pid].seat=count
			statistic.players[player(s).pid].jetton=int(s[-3])
			statistic.players[player(s).pid].money=int(s[-2])
			statistic.current_playerid.append(player(s).pid)
			count=count+1
		for s in seatinfo[:3]:
			s=s.split(' ')
			statistic.players[player(s).pid].seat=count
			statistic.players[player(s).pid].jetton=int(s[-3])
			statistic.players[player(s).pid].money=int(s[-2])
			statistic.current_playerid.append(player(s).pid)
			count=count+1
			
		statistic.myseat=statistic.players[statistic.myid].seat
		statistic.myjetton=statistic.players[statistic.myid].jetton
		statistic.mymoney=statistic.players[statistic.myid].money
		statistic.num_player=count
		print 'seatinfo'
		for s in statistic.players.keys():
			print(statistic.players[s].pid,statistic.players[s].seat)
		msg=msg[end+1:]
		if msg and msg[0]:
			#print msg
			deal_msg(msg,client)

	elif 'blind/ '==msg[0]:
		print 'blind:'
		end=msg.index('/blind ')
		#print(msg,end)
		blindinfo=msg[1:end]
		for s in blindinfo:
			s=s.split(' ')
			statistic.players[s[0][:-1]].jetton=statistic.players[s[0][:-1]].jetton-int(s[1])
			if not statistic.current_bb:
				statistic.current_bb=2*int(s[1])
		msg=msg[end+1:]
		if msg and msg[0]:
			#print msg
			deal_msg(msg,client)
	elif 'hold/ '==msg[0]:
		print 'hold:'
		statistic.numraise=0
		statistic.numcall=0
		statistic.numfold=0
		statistic.numallin=0
		statistic.current_bet=0
		statistic.bets=0
		statistic.stage='preflop'
		statistic.samestage=0
		end=msg.index('/hold ')
		holdinfo=msg[1:end]
		for s in holdinfo:
			statistic.hold.append(cards(s))
		if statistic.value[statistic.hold[0].value]<statistic.value[statistic.hold[1].value]:
			statistic.hold=statistic.hold[::-1]
		if statistic.hold[0].color==statistic.hold[1].color:
			statistic.color=statistic.hold[0].color
		statistic.myhands=statistic.hold[0].value+statistic.hold[1].value
		if statistic.color:
			statistic.myhands=statistic.myhands+'s'
		msg=msg[end+1:]
		if msg and msg[0]:
			#print msg
			deal_msg(msg,client)
			
	elif 'flop/ '==msg[0]:
		print 'flop:'
		statistic.numraise=0
		statistic.numcall=0
		statistic.numfold=0
		statistic.numallin=0
		statistic.current_bet=0
		statistic.bets=0
		statistic.stage='flop'
		statistic.samestage=0
		if not statistic.seatchange:
			statistic.seatchange=1
			for s in statistic.current_playerid:
				if statistic.num_player>=3:
					statistic.players[s].seat=(statistic.players[s].seat+3)%statistic.num_player
		statistic.myseat=statistic.players[statistic.myid].seat

		print 'seat:'
		for s in statistic.players.keys():
			print(statistic.players[s].pid,statistic.players[s].seat)


		end=msg.index('/flop ')
		flopinfo=msg[1:end]
		for s in flopinfo:
			statistic.community.append(cards(s))
			statistic.communitycolor[cards(s).color]=statistic.communitycolor[cards(s).color]+1
			statistic.commonvalue.append(statistic.value[cards(s).value])
		statistic.communityvalue.sort()
		for i in range(1,len(statistic.commonvalue)):
			statistic.commongaplist.append(statistic.commonvalue[i]-statistic.commonvalue[i-1])
		statistic.common_sequence=''
		for s in statistic.commongaplist:
			statistic.common_sequence=statistic.common_sequence+str(s)
		for s in statistic.hold:
			statistic.community.append(s)
		#deal the signature_sequence
		statistic.communityvalue=[]
		statistic.numcolor=0
		for s in statistic.community:
			statistic.communityvalue.append(statistic.value[s.value])
		#print(statistic.communityvalue)
		statistic.communityvalue.sort()
		for i in range(1,len(statistic.commonvalue)):
			statistic.commongaplist.append(statistic.commonvalue[i]-statistic.commonvalue[i-1])
		statistic.communityvalue.sort()
		statistic.gaplist=[]
		statistic.gaplist.append(statistic.communityvalue[0])
		for s in statistic.community:
			if statistic.color==s.color:
				statistic.numcolor=statistic.numcolor+1
		for i in range(1,len(statistic.communityvalue)):
			statistic.gaplist.append(statistic.communityvalue[i]-statistic.communityvalue[i-1])
		statistic.signature_sequence=''
		for s in statistic.gaplist:
			statistic.signature_sequence=statistic.signature_sequence+str(s)
		statistic.communityvalue=statistic.communityvalue[::-1]
		if re.match(r'^(\d*)1111(\d*)$',statistic.signature_sequence) and statistic.numcolor==5:
			statistic.my_nut_hand='STRAIGHT_FLUSH'
		elif re.match(r'^(\d*)000(\d*)$',statistic.signature_sequence):
			statistic.my_nut_hand='FOUR_OF_A_KIND'
		elif re.match(r'^(\d*)00(\d)0(\d*)$',statistic.signature_sequence) or re.match(r'^(\d*)0(\d)00(\d*)$',statistic.signature_sequence):
			statistic.my_nut_hand='FULL_HOUSE'
		elif statistic.numcolor==5:
			statistic.my_nut_hand='FLUSH'
		elif re.match(r'^(\d*)1111(\d*)$',statistic.signature_sequence):
			statistic.my_nut_hand='STRAIGHT'
		elif re.match(r'^(\d*)00(\d*)$',statistic.signature_sequence):
			statistic.my_nut_hand='THREE_OF_A_KIND'
		elif re.match(r'^(\d*)0(\d*)0(\d*)$',statistic.signature_sequence):
			statistic.my_nut_hand='TWO_PAIR'
		elif re.match(r'^(\d*)0(\d*)$',statistic.signature_sequence):
			statistic.my_nut_hand='ONE_PAIR'
		else:
			statistic.my_nut_hand='HIGH_CARD'
		print statistic.signature_sequence
		print statistic.common_sequence
		print statistic.my_nut_hand
		#deal next message
		msg=msg[end+1:]
		if msg and msg[0]:
			deal_msg(msg,client)
	elif 'turn/ '==msg[0]:
		print 'turn:'
		statistic.numraise=0
		statistic.numcall=0
		statistic.numfold=0
		statistic.numallin=0
		statistic.current_bet=0
		statistic.bets=0
		statistic.stage='turn'
		statistic.samestage=0
		end=msg.index('/turn ')
		turninfo=msg[1:end]
		statistic.turn=turninfo[0]
		statistic.community.append(cards(turninfo[0]))
		statistic.communitycolor[cards(turninfo[0]).color]=statistic.communitycolor[cards(turninfo[0]).color]+1
		statistic.commonvalue.append(statistic.value[cards(turninfo[0]).value]) 
		statistic.commonvalue.sort()
		for i in range(1,len(statistic.commonvalue)):
			statistic.commongaplist.append(statistic.commonvalue[i]-statistic.commonvalue[i-1])
		statistic.common_sequence=''
		for s in statistic.commongaplist:
			statistic.common_sequence=statistic.common_sequence+str(s)
		#for s in statistic.community:
			#print s.value
		cardclass()
		msg=msg[end+1:]
		if msg and msg[0]:
			deal_msg(msg,client)
	elif 'river/ '==msg[0]:
		print 'river:'
		statistic.numraise=0
		statistic.numcall=0
		statistic.numfold=0
		statistic.numallin=0
		statistic.current_bet=0
		statistic.bets=0
		statistic.stage='river'
		statistic.samestage=0
		end=msg.index('/river ')
		riverinfo=msg[1:end]
		statistic.river=riverinfo[0]
		statistic.community.append(cards(riverinfo[0]))
		statistic.communitycolor[cards(riverinfo[0]).color]=statistic.communitycolor[cards(riverinfo[0]).color]+1
		statistic.commonvalue.append(statistic.value[cards(riverinfo[0]).value]) 
		statistic.commonvalue.sort()
		for i in range(1,len(statistic.commonvalue)):
			statistic.commongaplist.append(statistic.commonvalue[i]-statistic.commonvalue[i-1])
		statistic.common_sequence=''
		for s in statistic.commongaplist:
			statistic.common_sequence=statistic.common_sequence+str(s)
		#statistic.communityvalue.sort()
		#for i in range(1,len(statistic.commonvalue)):
		#	statistic.commongaplist.append(statistic.commonvalue[i]-statistic.commonvalue[i-1])
		cardclass()
		msg=msg[end+1:]
		if msg and msg[0]:
			deal_msg(msg,client)
	elif 'showdown/ '==msg[0]:
		print 'showdown:'
		end=msg.index('/showdown ')
		showdowninfo=msg[1:end]

		msg=msg[end+1:]
		if msg and msg[0]:
			deal_msg(msg,client)
		
	elif 'pot-win/ '==msg[0]:
		print 'pot-win:'
		statistic.totalplay=statistic.totalplay+1
		statistic.numhand=statistic.numhand+1
		end=msg.index('/pot-win ')
		potwininfo=msg[1:end]
		for s in potwininfo:
			s=s.split(' ')
			statistic.players[s[0][:-1]].jetton=statistic.players[s[0][:-1]].jetton+int(s[1])
		statistic.last_action=''
		statistic.stage=''
		statistic.community=[]
		statistic.communityvalue=[]
		statistic.commonvalue=[]
		statistic.communitycolor={'SPADES':0,'HEARTS':0,'CLUBS':0,'DIAMONDS':0}
		statistic.communitynumcolor=[statistic.communitycolor['SPADES'],statistic.communitycolor['HEARTS'],statistic.communitycolor['CLUBS'],statistic.communitycolor['DIAMONDS']]
		statistic.turn=''
		statistic.river='' 
		statistic.bet=0
		statistic.big_blind=''
		statistic.small_blind=''
		statistic.button=''
		statistic.hold=[]
		statistic.current_pot=0
		statistic.current_bet=0
		statistic.current_bb=0
		statistic.color=''
		statistic.numcolor=0
		statistic.myhands=''
		statistic.my_nut_hand=''
		statistic.signature_sequence=''
		statistic.common_sequence=''
		statistic.gaplist=[]
		statistic.commongaplist=[]
		statistic.numraise=0
		statistic.numcall=0
		statistic.numfold=0
		statistic.numcheck=0
		statistic.numallin=0
		statistic.seatchange=0
 		print '-------%d------------' % statistic.totalplay
		msg=msg[end+1:]
		#print msg
		if msg and msg[0]:
			deal_msg(msg,client)
	else:
		pass



if __name__=='__main__':
	msg='seat/ \nbutton: pid1 21 33 \nsmall blind: pid2 22 33 \nbig blind: pid3 33 33 \n/seat \nblind/ \npid1: 2 \npid2: 3 \n/blind \n'
	msg=msg.split('\n')
	deal_msg(msg)
	for k in statistic.players.keys():
		print(k,statistic.players[k].seat)
	msg='blind/ \npid1: 2 \npid2: 3 \n/blind \n'
	msg=msg.split('\n')
	deal_msg(msg)
	for k in statistic.players.keys():
		print(statistic.players[k].jetton)
	msg='hold/ \nfang J \nfang J \n/hold \n'
	msg=msg.split('\n')
	deal_msg(msg)
	msg='flop/ \nh J \nf J \nm J \n/flop \n'
	msg=msg.split('\n')
	deal_msg(msg)
	for s in statistic.community:
		print s.value
		print s.color
	msg='turn/ \nb J \n/turn \n'
	msg=msg.split('\n')
	deal_msg(msg)
	for s in statistic.community:
		print s.value
		print s.color
	msg='river/ \nf K \n/river \n'
	msg=msg.split('\n')
	deal_msg(msg)
	for s in statistic.community:
		print s.value
		print s.color
	msg='pot-win/ \npid1: 110 \npid2: 220 \n/pot-win \n'
	msg=msg.split('\n')
	deal_msg(msg)
	for s in statistic.players.keys():
		print statistic.players[s].jetton
	msg='inquire/ \ntotal pot: num \n/inquire \n'
	deal_msg(msg.split('\n'))
	msg='game-over \n'
	deal_msg(msg.split('\n'))