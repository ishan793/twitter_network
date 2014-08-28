import json,os,time,random
from oauth2 import Client,ClientException,NotAuthException,ChangeClientException,NotFoundException
from config import *
import multiprocessing

# client_list = { '0' : [Client(CONSUMER_KEY, CONSUMER_SECRET),0] , '1' : [Client(CONSUMER_KEY1, CONSUMER_SECRET1),0], '2' : [Client(CONSUMER_KEY2, CONSUMER_SECRET2),0], '171' : [Client(CONSUMER_KEY171, CONSUMER_SECRET171),0], '172' : [Client(CONSUMER_KEY172, CONSUMER_SECRET172),0] }
# for client in client_list:
	# print client_list[client]
def get_all_ids(dirname):
	level_1_list = os.listdir(dirname)
	user_list = {}
	for id_file in level_1_list:
		f=open(dirname + "\\" + id_file , 'r')
		for line in f : 
			try:
				user_list[int(line)]=1
			except ValueError:
				continue
	user_list=user_list.keys()
	user_list.sort()
	#print len(user_list)
	return user_list

def distribute_ids():
	f = open('mayank_ids.txt','r')
	user_list1 = []
	user_list2 = []
	user_list3 = []
	for line in f:
		try:
			if(random.random()<10.0/26):
				user_list1.append(int(line))
			elif(random.random()<20.0/26):
				user_list2.append(int(line))
			else:
				user_list3.append(int(line))
		except ValueError:
			continue
	return user_list1,user_list2,user_list3

def get_client_list():
	client_list1 = {}
	client_list2 = {}
	client_list3 = {}
	for key in CONSUMER_KEY_dict:
		if(random.random()<10.0/26):
			client_list1[str(key)] = [Client(CONSUMER_KEY_dict[key], CONSUMER_SECRET_dict[key]),0]
		elif(random.random()<20.0/26):
			client_list2[str(key)] = [Client(CONSUMER_KEY_dict[key], CONSUMER_SECRET_dict[key]),0]
		else:
			client_list3[str(key)] = [Client(CONSUMER_KEY_dict[key], CONSUMER_SECRET_dict[key]),0]
	return client_list1,client_list2,client_list3
	
def limitcheck(client , clientid, client_list):
	#print client,clientid
	status = client.request(STATUS_URL)
	request_remaining = int(status['resources']['friends']['/friends/ids']['remaining'])
	reset_time = int(status['resources']['friends']['/friends/ids']['reset'])
	if(request_remaining < 1):
		current_time = int(round(time.time()))+1
		#print 'Rate Limit exceeded....sleeping now'
		#time.sleep(abs(reset_time-current_time))
		client_list[clientid] = [client, reset_time]
		return 'exhausted'
	else:
		client_list[clientid] = [client, 0]
		return 'go_on'
			

def client_select(client_list):
	flag = 0
	for client in client_list:
		# if ( client_list[client][1] == 0):
			# flag=1
			# return client_list[client][0],client
		if ( limitcheck(client_list[client][0],client,client_list) == 'go_on'):
			flag=1
			return client_list[client][0],client
	sort_resettime=sorted(client_list.items(), key=lambda x: x[1][1])
	current_time = int(round(time.time()))+1
	print 'limit exhausted...sleeping for ',str(sort_resettime[0][1][1] - current_time)
	time.sleep(abs(sort_resettime[0][1][1] - current_time))
	c,i = client_select(client_list)
	return c,i
			
	
def getFollowingIds(user_name,client_list,count,client,i):
	request_url = FOLLOWING_URL_ID+user_name
	friends_list = []
	cursor = '-1'
	
	while(cursor != 0):
		if(count == 15):
			client,i = client_select(client_list)
			#print client,i
			count = 0
		#limitcheck(client)
		url = request_url+'&cursor='+str(cursor)
		#try:
		count += 1
		reply=0
		try:
			reply = client.request(url)
		except NotAuthException:
			return 'notauth',count,client,i
		except NotFoundException:
			return 'notfound',count,client,i
		except ChangeClientException:
			client,i = client_select(client_list)
			#print client,i
			print 'changing ids'
			count = 0
			r,c,cl,il = getFollowingIds(user_name,client_list,count,client,i)
			return r,c,cl,il
		#except:
			# TO DO: find possible exceptions and write appropriate handlers
		#	pass
		friends_list += reply['ids']
		cursor = int(reply['next_cursor_str'])

	result = []
	for i in friends_list:
		result.append(str(i))
            
	return  result,count,client,i

	
count_1 = 15
count_2 = 15
count_3 = 15
client_1 = 0
client_2 = 0
client_3 = 0
i_1 = None
i_2 = None
i_3 = None
def get_followers(target_directory,user_list,client_list,count,client,i):
	
	current_dir = os.getcwd();
	#create a new folder to store the results
	try:
		os.mkdir(target_directory)
	except OSError:
		# in case the folder is already made, we don't do anything
		pass
	
	storing_dir = current_dir+'\\'+target_directory+'\\'
	# find the user for which crawling has been done
	existing_files = os.listdir(storing_dir)
	# get the list of users for which crawling needs to be done
	#user_list = get_all_ids('data_collection')
	for user in user_list:
		user = str(user)
		modified_name = user+'.txt'
		# check if the user has already been crawled
		if modified_name in existing_files:
			#print user,'already done'
			pass
		else:
			try:
				following_list,count,client,i = getFollowingIds(user,client_list,count,client,i)
			except ValueError:
				continue
			if(following_list == 'notauth' or following_list == 'notfound'):
				pass
			
			else:
				print user,'follows',str(len(following_list)),'people'
				with open(storing_dir+user+'.txt','w') as f:
					for i in following_list:
						f.write(i+'\n')
				f.close()

if __name__ == '__main__': 
	[client_list1,client_list2,client_list3] = get_client_list()	
	[user_list1,user_list2,user_list3] = distribute_ids()			
	[client_1,i_1] = client_select(client_list1)
	[client_2,i_2] = client_select(client_list2)
	[client_3,i_3] = client_select(client_list3)
	#print client_1,i_1
	#print client_2,i_2
	#print client_3,i_3
	procs = 3
	jobs = []

	for i in range(0, procs):
		out_list = list()
		if (i == 0):
			process = multiprocessing.Process(target=get_followers, 
											  args=('level_2_followers',user_list1,client_list1,count_1,client_1,i_1))
		elif(i == 1):
			process = multiprocessing.Process(target=get_followers, 
											  args=('level_2_followers',user_list2,client_list2,count_2,client_2,i_2))
		else:
			process = multiprocessing.Process(target=get_followers, 
											  args=('level_2_followers',user_list3,client_list3,count_3,client_3,i_3))
		jobs.append(process)
	for j in jobs:
		j.start()

	# Ensure all of the processes have finished
	for j in jobs:
		j.join()

