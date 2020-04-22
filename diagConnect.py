#! /usr/bin/env python3
import mysql.connector
import nclib

proface = { 
	'SCR_02_A': 	{'IP' :'10.210.202.60', 'type': 'WD'},
	'SCR_02_B': 	{'IP' :'10.210.202.61', 'type': 'WD'},
	'SCR_03_A': 	{'IP' :'10.210.202.62', 'type': 'LT'},
	'SCR_03_B': 	{'IP' :'10.210.202.63', 'type': 'LT'},
	'SCR_04_CMB': 	{'IP' :'10.210.202.64', 'type': 'WD'},
	'SCR_05_LEAK': 	{'IP' :'10.210.202.65', 'type': 'LT'},
	'LNT_01_02': 	{'IP' :'10.210.202.66', 'type': 'WD1'},
	'LNT_01_03': 	{'IP' :'10.210.202.67', 'type': 'WD1'},
	'LNT_01_04': 	{'IP' :'10.210.202.68', 'type': 'WD1'},
	'LNT_01_05': 	{'IP' :'10.210.202.69', 'type': 'LT'},
	'LNT_01_06': 	{'IP' :'10.210.202.70', 'type': 'WD'},
	'LNT_01_07': 	{'IP' :'10.210.202.71', 'type': 'SP'},
	#'LNT_01_08': 	{'IP' :'10.210.202.72', 'type': 'PR'},
	'LNT_01_09': 	{'IP' :'10.210.202.73', 'type': 'SP'},
	'LNT_01_10': 	{'IP' :'10.210.202.74', 'type': 'SP1'},
	'LNT_01_11': 	{'IP' :'10.210.202.75', 'type': 'BO'},
	'LNT_01_12': 	{'IP' :'10.210.202.76', 'type': 'LT'},
	'QL_CTR': 		{'IP' :'10.210.202.77', 'type': 'WD'},
	'QL_MAIN_02':	{'IP' :'10.210.202.78', 'type': 'WD'},
	'QL_MAIN_03':	{'IP' :'10.210.202.79', 'type': 'WDLT'},
	'KAPPA_WCC':	{'IP' :'10.210.202.80', 'type': 'ST'},
	'LNT_02_02': 	{'IP' :'10.210.202.81', 'type': 'WD1'},
	'LNT_02_03': 	{'IP' :'10.210.202.82', 'type': 'WD1'},
	'LNT_02_04': 	{'IP' :'10.210.202.83', 'type': 'WD1'},
	'LNT_02_05': 	{'IP' :'10.210.202.84', 'type': 'LT'},
	'LNT_02_06': 	{'IP' :'10.210.202.85', 'type': 'WD'},
	'LNT_02_07': 	{'IP' :'10.210.202.86', 'type': 'SP'},
	#'LNT_02_08': 	{'IP' :'10.210.202.87', 'type': 'PR'},
	'LNT_02_09': 	{'IP' :'10.210.202.88', 'type': 'SP'},
	'LNT_02_10': 	{'IP' :'10.210.202.89', 'type': 'SP1'},
	'LNT_02_11': 	{'IP' :'10.210.202.90', 'type': 'BO'},
	'LNT_02_12': 	{'IP' :'10.210.202.91', 'type': 'LT'}	
}

def mp_connect():
	mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
	return mp_database

def get_diag(machine):
	#mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
	#mycursor = mp_database.cursor()
	#print ('HMI stroja je > ',machine)
	mp_database = mp_connect()
	mycursor = mp_database.cursor()
	mycursor.execute("select a.* from tdeqtc_view a,(select @P_IDEQBC:='"+machine+"') as b;")
	myresult = mycursor.fetchall()
	mycursor.execute("select a.* from tdeqtc_view a,(select @P_IDEQBC:='"+machine+"') as b;")
	myresult = mycursor.fetchall()
	#mp_database.close()
	return myresult

def get_diag_ID(table,dopyt):
	for id in table:
		if id[2] == dopyt:
			return id[0]

#print (get_diag_ID(get_diag(),'Teplota'))

def set_diag(HMI,parameter,value):
	
	#mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
	mp_database = mp_connect()
	mycursor = mp_database.cursor()
	#print (HMI,get_diag_ID(get_diag(HMI),parameter))
	sql = "INSERT INTO TIDIAG(FSECRN,IDTCPR,FNDIAG)VALUES(%s,%s,%s)"
	val = (HMI,get_diag_ID(get_diag(HMI),parameter),value)

	mycursor.execute(sql,val)
	mp_database.commit()
	mp_database.close()

def get_proface_value(line):
	
	destination = proface[line]['IP']
	nc = nclib.Netcat((destination, 1024), udp=True, verbose=False)
	nc.echo_hex =False 
	nc.settimeout(0.2)
	nc.send(b'B\x00\x00\x00\x00\x00\x00\x06\x1bR\x01\xf4\x00\x1f')	#MEMLINK 500 first parameter of diagnostic value
	memlink = (nc.recv())
	
	# print (memlink)
	
	status = list()
	status4 = list()
	
	for x in range(10,20):
		status.append(memlink[x])
	
	# print (status)
	for x in range(0,len(status),2):
		status1 = status[x],status[x+1] 	#ff[x] + ff[x+1]
		status2 = bytearray(status1)		# (ff,ff)
		status3 = int.from_bytes(status2, byteorder='big') # = 65 535
		status4.append(status3)

		# print ('STATUS1 = ',status1)
		# print ('STATUS2 = ',status2)
		# print ('STATUS3 = ',status3)
	# print ('STATUS4 FINAL = ',status4)
	
	return status4 #[0]len prvy parameter memlink 500
	
#print (get_diag_ID,(get_diag('SCR_02_B'),'Vyrobené množstvo x100'))
#get_proface_value('SCR_02_B','Vyrobené množstvo x100')
#set_diag('SCR_02_B','Vyrobené množstvo x100',get_proface_value('SCR_02_B')) #OK
#set_diag('SCR_02_B','Vyrobené množstvo x100',get_proface_value('SCR_02_B'))

def test():
	for machines,ip in proface.items():
		print ('stroj - ',machines,'\t IP: ',ip['IP'],'\t D44 (memlink 0500 ) = ',get_proface_value(machines),' \t param: ',get_diag(machines))
		
def fillDiagNonZero():

	try:
		test()
	except:
		exit()
	else:
		#exit() #debug
		for machines,ip in proface.items():
			status = get_proface_value(machines)
			if not status[0] == 0:
				print ('stroj - ',machines,'\t ukladam hodnotu = ',status[0])
				set_diag(machines,'Vyrobené množstvo x100',status[0])

fillDiagNonZero()
#test()
# print (get_proface_value('LNT_01_02'))
#memcpy([w:[#MEMLINK]0500], [w:[PLC1]D00044], 1)
#memcpy([w:[#MEMLINK]0500], [w:[PLC1]D00161], 1) MAIN QL

	#print (machines,ip['IP'])

#select a.* from tdeqtc_view a,(select @P_IDEQBC:='KOM1') as b;
