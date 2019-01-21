import sys, time, re, traceback
import psycopg2 as p

con = p.connect("dbname='' user='' host='' password=''")
cur = con.cursor()

class current_table:
	table = ''


def menu():
	print("\n>\\t(able)  \\d(isplay)  \\a(dd)  \\f(ind)  \\q(uit)")
	user_inp = input('>')
	return user_inp


def table(): 
	# list tables in dir
	cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
	tables_raw = cur.fetchall()
	tables = []
	for i in range(len(tables_raw)):
		tables.append(tables_raw[i][0])

	print()
	for i in tables:
		print('>-'+i)
	table_choice = input('\n>Pick table: ')

	#make sure table_choice exists
	if table_choice in tables:
		current_table.table = table_choice
	else:
		print('\n>Invalid Table Name')
		input()


def display():
	if current_table.table == '':
		print('\n>No Table Selected')
		input()
	else:
		cur.execute(f"select * from {current_table.table}")
		# cur.execute("select * from	site2")
		rows = cur.fetchall()

		# get column names and display them
		cur.execute(f"SELECT * FROM {current_table.table} LIMIT 0")
		colnames = [desc[0] for desc in cur.description]
		print('\n> ', end='')
		for name in colnames:
			print('-'+name+'  ', end='')
		print()

		# return row data
		for i in range(len(rows)):
			print(rows[i])
			time.sleep(.1)


def add():
	# make sure table is selected
	if current_table.table == '':
		print('\n>No Table Selected')
		input()
	else: 
		#access all columns in table
		cur.execute(f"SELECT * FROM {current_table.table} LIMIT 0")
		colnames = [desc[0] for desc in cur.description]

		# ask user for data inputs
		inputs = []
		for i in colnames:
			choice = input(f'>Enter a {i}: ')
			inputs.append(choice)
		
		#turn column list into usable str
		col_string = re.sub("[\[\]']", '', str(colnames))
		#turn user input list into values str
		input_str = re.sub('[\[\]]', '', str(inputs))

		# sql cmd- try to insert user values into new row of current table. If table takes other valuetypes,
		#		   user is prompted with error and offending input in 'except' statement.
		try:
			cur.execute(f"INSERT INTO {current_table.table} ({col_string}) VALUES ({input_str})")
			con.commit()
			print('\n>DATA ADDED')

		except:
			error_message = traceback.format_exc()
			error_re = re.compile(r'DataError:\s\D+"')
			error_output = error_re.search(error_message).group()
			print('\n>--- '+error_output+' ---')
			con.rollback()

		input()


def find(): 
	#make sure table is selected first
	if current_table.table == '':
		print('\n>No Table Selected')
		input()

	else:
		#access all columns in table
		cur.execute(f"SELECT * FROM {current_table.table} LIMIT 0")
		colnames = [desc[0] for desc in cur.description]
	
		# display column names with numbers by them for user to pick
		print('\n>Search by column:')
		print('>', end='')
		for i in range(len(colnames)):
			print('['+str(i)+'] '+colnames[i]+'  ', end='')

		# user picks numb, thus choosing column to search
		try:
			col_pick = input('\n>')
			col_sel = colnames[int(col_pick)]
		except:
			print('\n>Value Invalid- Only Listed Values May Be Selected')
			input()
			main()

		# get input of what to search for in the column, return results
		name = input(f'>Enter {col_sel} to search for in db: ')
		cur.execute(f"SELECT * FROM {current_table.table} WHERE {col_sel} = '{name}';")
		results = cur.fetchall()

		# check if there are any results, then display them or message that  there is none
		if len(results) == 0:
			print('\n>No Results')
			input()
		else:
			print()
			for i in range(len(results)):
				print(results[i])


def quit():
	print('\n>Logging off...\n')
	cur.close()
	con.close()
	sys.exit(0)



def main():
	while True:

		user_inp = menu()

		if user_inp == r'\t':
			table()
		elif user_inp == r'\d':
			display()
		elif user_inp == r'\a':
			add()
		elif user_inp == r'\f':
			find()
		elif user_inp == r'\q':
			quit()
	

main()

cur.close()
con.close()

