import csv
import numpy as np



def init():	
	unique_items = []
	item_num = 0
	unique_users = []
	user_num = 0

	with open('ua.base', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
	#		print row
			row = row[0]
			row = row.split()
			if row[0] not in unique_users:
				user_num += 1
				unique_users.append(row[0])
			if row[1] not in unique_items:
				item_num += 1
				unique_items.append(row[1])



	#print (unique_users)			
	#print (unique_items)
	m = user_num + 1
	n = item_num + 1
	print m
	print n

	big_R_list = [0] * m

	for i in range(m):
		big_R_list[i] = [0] * n

	big_R = np.array(big_R_list)
	ik = 0


	with open('ua.base', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			ik += 1
			row = row[0]
			row = row.split()
			try:
				big_R[int(row[0])][int(row[1])] = int(row[2])
			except:
			#	print row
				continue


	print big_R[943][1330]


	for i in range(0,m):
		print(str(i) + " : " + str(len(big_R[i])))

		


init()