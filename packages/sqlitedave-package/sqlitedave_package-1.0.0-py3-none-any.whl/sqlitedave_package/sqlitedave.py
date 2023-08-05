"""
  Dave Skura
  
  File Description:
"""

import os
import sys
from datetime import *
import time
import sqlite3
from garbledave_package.garbledave import garbledave 

class dbconnection_details: 
	def __init__(self,DB_NAME=''): 
		self.DatabaseType='SQLite' 
		self.updated='Mar 23/2023' 

		self.settings_loaded_from_file = False

		self.DB_NAME=DB_NAME
		if DB_NAME == '':
			self.loadSettingsFromFile()

	def loadSettingsFromFile(self):
		try:
			f = open('.schemawiz_config3','r')
			connectionstrlines = f.read()
			connectionstr = garbledave().ungarbleit(connectionstrlines.splitlines()[0])
			f.close()
			connarr = connectionstr.split(' - ')

			self.DB_NAME			= connarr[0]

			self.settings_loaded_from_file = True

		except:
			#saved connection details not found. using defaults
			self.DB_NAME='' 

	def dbconnectionstr(self):
		return 'Database=' + self.DB_NAME + ';'

	def saveConnectionDefaults(self,DB_NAME=''):

		f = open('.schemawiz_config3','w')
		f.write(garbledave().garbleit(DB_NAME + ' - ' ))
		f.close()

		self.loadSettingsFromFile()

class tfield:
	def __init__(self):
		self.table_name = ''
		self.column_name = ''
		self.data_type = ''
		self.Need_Quotes = ''
		self.ordinal_position = -1
		self.comment = '' # dateformat in csv [%Y/%m/%d]

class sqlite_db:
	def __init__(self,DB_NAME=''):
		self.enable_logging = False
		self.max_loglines = 500
		self.db_conn_dets = dbconnection_details(DB_NAME)
		self.dbconn = None
		self.cur = None

	def getbetween(self,srch_str,chr_strt,chr_end,srch_position=0):
		foundit = 0
		string_of_interest = ''
		for i in range(srch_position,len(srch_str)):
			if (srch_str[i] == chr_strt ):
				foundit += 1

			if (srch_str[i] == chr_end ):
				foundit -= 1
			if (len(string_of_interest) > 0 and (foundit == 0)):
				break
			if (foundit > 0):
				string_of_interest += srch_str[i]
			
		return string_of_interest[1:]

	def getfielddefs(self,tablename):
		tablefields = []
		sql = """
SELECT 
  p.name AS column_name, p.type AS data_type

	,CASE 
        WHEN lower(p.type) in ('text','blob') THEN 'QUOTE'
        WHEN lower(p.type) in ('real','integer','null') THEN 'NO QUOTE'
    END as Need_Quotes    
    ,p.cid as ordinal_position

FROM sqlite_master AS m
  INNER JOIN pragma_table_info(m.name) AS p
WHERE m.name NOT IN ('sqlite_sequence')
	and m.name = '""" + tablename + """'
ORDER BY m.name, p.cid
		"""

		data = self.query(sql)
		for row in data:
			fld = tfield()
			fld.table_name = tablename
			fld.column_name = row[0]
			fld.data_type = row[1]
			fld.Need_Quotes = row[2]
			fld.ordinal_position = row[3]

			tablefields.append(fld)

		return tablefields

	def dbstr(self):
		return 'Database=' + self.db_conn_dets.DB_NAME + '; version ' + self.dbversion()

	def dbversion(self):
		return self.queryone('select sqlite_version();')

	def clean_column_name(self,col_name):

		new_column_name = col_name
		chardict = self.count_chars(col_name)
		alphacount = self.count_alpha(chardict)
		nbrcount = self.count_nbr(chardict)
		if ((len(col_name)-2) == (alphacount + nbrcount)) and '1234567890'.find(col_name[:1]) == -1:
			new_column_name = self.clean_text(col_name) # .replace('"','').strip()

		return new_column_name

	def clean_text(self,ptext): # remove optional double quotes
		text = ptext.strip()
		if (text[:1] == '"' and text[-1:] == '"'):
			return text[1:-1]
		else:
			return text

	def count_chars(self,data,exceptchars=''):
		chars_in_hdr = {}
		for i in range(0,len(data)):
			if data[i] != '\n' and exceptchars.find(data[i]) == -1:
				if data[i] in chars_in_hdr:
					chars_in_hdr[data[i]] += 1
				else:
					chars_in_hdr[data[i]] = 1
		return chars_in_hdr

	def count_alpha(self,alphadict):
		count = 0
		for ch in alphadict:
			if 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def count_nbr(self,alphadict):
		count = 0
		for ch in alphadict:
			if '0123456789'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def logquery(self,logline,duration=0.0):
		if self.enable_logging:
			startat = (datetime.now())
			startdy = str(startat.year) + '-' + ('0' + str(startat.month))[-2:] + '-' + str(startat.day)
			starttm = str(startat.hour) + ':' + ('0' + str(startat.minute))[-2:] + ':' + ('0' + str(startat.second))[-2:]
			start_dtm = startdy + ' ' + starttm
			preline = start_dtm + '\nduration=' + str(duration) + '\n'

			log_contents=''
			try:
				f = open('.querylog','r')
				log_contents = f.read()
				f.close()
			except:
				pass

			logs = log_contents.splitlines()
			
			logs.insert(0,preline + logline + '\n ------------ ')
			f = open('.querylog','w+')
			numlines = 0
			for line in logs:
				numlines += 1
				f.write(line + '\n')
				if numlines > self.max_loglines:
					break

			f.close()


	def saveConnectionDefaults(self,DB_NAME):
		self.db_conn_dets.saveConnectionDefaults(DB_NAME)

	def useConnectionDetails(self,DB_NAME):

		self.db_conn_dets.DB_NAME = DB_NAME					
		self.connect()

	def is_an_int(self,prm):
			try:
				if int(prm) == int(prm):
					return True
				else:
					return False
			except:
					return False

	def export_query_to_str(self,qry,szdelimiter=','):
		self.execute(qry)
		f = ''
		sz = ''
		for k in [i[0] for i in self.cur.description]:
			sz += k + szdelimiter
		f += sz[:-1] + '\n'

		for row in self.cur:
			sz = ''
			for i in range(0,len(self.cur.description)):
				sz += str(row[i])+ szdelimiter

			f += sz[:-1] + '\n'

		return f

	def export_query_to_csv(self,qry,csv_filename,szdelimiter=','):
		data = self.query(qry)
		#print(data.description)
		#sys.exit(0)
		f = open(csv_filename,'w')
		sz = ''
		for k in [i[0] for i in data.description]:
			sz += k + szdelimiter
		f.write(sz[:-1] + '\n')

		for row in data:
			sz = ''
			for i in range(0,len(data.description)):
				sz += str(row[i])+ szdelimiter

			f.write(sz[:-1] + '\n')
				

	def export_table_to_csv(self,csvfile,tblname,szdelimiter=','):
		if not self.does_table_exist(tblname):
			raise Exception('Table does not exist.  Create table first')

		self.export_query_to_csv('SELECT * FROM ' + tblname,csvfile,szdelimiter)

	def load_csv_to_table(self,csvfile,tblname,withtruncate=True,szdelimiter=',',fields='',withextrafields={}):
		table_fields = self.getfielddefs(tblname)

		if not self.does_table_exist(tblname):
			raise Exception('Table does not exist.  Create table first')

		if withtruncate:
			self.execute('DELETE FROM ' + tblname)

		f = open(csvfile,'r')
		hdrs = f.read(1000).split('\n')[0].strip().split(szdelimiter)
		f.close()		

		isqlhdr = 'INSERT INTO ' + tblname + '('

		if fields != '':
			isqlhdr += fields	+ ') VALUES '	
		else:
			for i in range(0,len(hdrs)):
				isqlhdr += self.clean_column_name(hdrs[i]) + ','
			isqlhdr = isqlhdr[:-1] + ') VALUES '

		skiprow1 = 0
		batchcount = 0
		ilines = ''

		with open(csvfile) as myfile:
			for line in myfile:
				if line.strip()!='':
					if skiprow1 == 0:
						skiprow1 = 1
					else:
						batchcount += 1
						row = line.rstrip("\n").split(szdelimiter)
						newline = "("
						for var in withextrafields:
							newline += "'" + withextrafields[var]  + "',"

						for j in range(0,len(row)):

							if row[j].lower() == 'none' or row[j].lower() == 'null':
								newline += "NULL,"
							else:
								if table_fields[j].data_type.strip().lower() == 'date':
									dt_fmt = self.getbetween(table_fields[j].comment,'[',']')
									if dt_fmt.strip() != '':
										newline += "str_to_date('" + self.clean_text(row[j]) + "','" + dt_fmt + "'),"
									else:
										newline += "'" + self.clean_text(row[j]) + "',"

								elif table_fields[j].data_type.strip().lower() == 'timestamp':
									dt_fmt = self.getbetween(table_fields[j].comment,'[',']')
									if dt_fmt.strip() != '':
										newline += "str_to_date('" + self.clean_text(row[j]) + "','" + dt_fmt + "'),"
									else:
										newline += "'" + self.clean_text(row[j]) + "',"

								elif table_fields[j].Need_Quotes == 'QUOTE':
									newline += "'" + self.clean_text(row[j]).replace(',','').replace("'",'').replace('"','') + "',"
								else:
									val = self.clean_text(row[j]).replace(',','').replace("'",'').replace('"','')
									if val == '':
										newline += "NULL,"
									else:
										newline += val + ","

							
						ilines += newline[:-1] + '),'
						
						if batchcount > 500:
							qry = isqlhdr + ilines[:-1]
							#print(qry)
							#sys.exit()
							batchcount = 0
							ilines = ''
							self.execute(qry)

		if batchcount > 0:
			qry = isqlhdr + ilines[:-1]
			batchcount = 0
			ilines = ''
			self.execute(qry)

	def does_table_exist(self,tblname):
		self.connect()

		sql = """
		SELECT count(*)
		FROM sqlite_master AS m
		WHERE lower(m.name) = lower('""" + tblname + "')"
		
		if self.queryone(sql) == 0:
			return False
		else:
			return True

	def close(self):
		if self.dbconn:
			self.dbconn.close()

	def ask_for_database_details(self):
		self.db_conn_dets.DB_NAME = input('DB_NAME (local_sqlite_db): ') or 'local_sqlite_db'

	def connect(self):
		connects_entered = False

		if self.db_conn_dets.DB_NAME == '':
			self.ask_for_database_details()
			connects_entered = True

		try:

			if not self.dbconn:
				self.dbconn = sqlite3.connect(self.db_conn_dets.DB_NAME)

				if connects_entered:
					user_response_to_save = input('Save this connection locally? (y/n) :')
					# only if successful connect after user prompted and got Y do we save pwd
					if user_response_to_save.upper()[:1] == 'Y':
						self.saveConnectionDefaults(self.db_conn_dets.DB_NAME)

		except Exception as e:
			if self.db_conn_dets.settings_loaded_from_file:
				os.remove('.schemawiz_config3')

			raise Exception(str(e))

	def query(self,qry):
		if not self.dbconn:
			self.connect()

		all_rows_of_data = self.dbconn.execute(qry)
		return all_rows_of_data

	def commit(self):
		self.dbconn.commit()


	def execute(self,qry):
		try:
			begin_at = time.time() * 1000
			if not self.dbconn:
				self.connect()
			self.dbconn.execute(qry)
			self.commit()
			end_at = time.time() * 1000
			duration = end_at - begin_at
			self.logquery(qry,duration)
		except Exception as e:
			raise Exception("SQL ERROR:\n\n" + str(e))

	def queryone(self,select_one_fld):
		try:
			if not self.dbconn:
				self.connect()
			data = self.dbconn.execute(select_one_fld)
			for row in data:
				return row[0]
		except Exception as e:
			raise Exception("SQL ERROR:\n\n" + str(e))

if __name__ == '__main__':
	mydb = sqlite_db()
	mydb.connect()
	print(mydb.dbstr())

	#csvfilename = 'Station.tsv'
	#tblname = 'Station'
	#mydb.load_csv_to_table(csvfilename,tblname,True,'\t')
	#mydb.export_table_to_csv(csvfilename,tblname)
	mydb.close()

