import random,os
def get_all_ids(dirname):
	level_2_done = os.listdir('level_2_followers')
	level2={}
	for i in level_2_done:
		level2[i]=1
	level_1_list = os.listdir(dirname)
	user_list = {}
	for id_file in level_1_list:
		f=open(dirname + "\\" + id_file , 'r')
		for line in f : 
			try:
				if(int(line) in level2):
					pass
				else:
					user_list[int(line)]=1
			except ValueError:
				continue
	user_list=user_list.keys()
	user_list.sort()
	print len(user_list)
	return user_list

def read_ids():
	user_list = get_all_ids('data_collection')
	fm = open('mayank_ids.txt','w')
	fi = open('ishan_ids.txt','w')
	for i in user_list:
		if(random.random() < 0.50):
			fm.write(str(i)+'\n')
		else :
			fi.write(str(i)+'\n')

read_ids()			
		