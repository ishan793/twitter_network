import os
from oauth2 import Client
# def get_all_ids(dirname):
	# level_1_list = os.listdir(dirname)
	# user_list = []
	# for id_file in level_1_list:
		# f=open(dirname + "\\" + id_file , 'r')
		# for line in f : 
			# try:
				# user_list.append(int(line))
			# except ValueError:
				# continue
	# user_list.sort()
	# print len(user_list)
# get_all_ids('data_collection')
from config import *
def limitcheck(client):
	status = client.request(STATUS_URL)
	request_remaining = int(status['resources']['friends']['/friends/ids']['remaining'])
	reset_time = int(status['resources']['friends']['/friends/ids']['reset'])
	print request_remaining
	if(request_remaining < 1):
		#current_time = int(round(time.time()))+1
		#print 'Rate Limit exceeded....sleeping now'
		#time.sleep(abs(reset_time-current_time))
		
		print 'exhausted'
	else:
		
		print 'go_on'




client_list = { '0' : [Client(CONSUMER_KEY, CONSUMER_SECRET),0] , '1' : [Client(CONSUMER_KEY1, CONSUMER_SECRET1),0], '2' : [Client(CONSUMER_KEY2, CONSUMER_SECRET2),0], '171' : [Client(CONSUMER_KEY171, CONSUMER_SECRET171),0], '172' : [Client(CONSUMER_KEY172, CONSUMER_SECRET172),0] }
for client in client_list:
	limitcheck(client_list[client][0])

