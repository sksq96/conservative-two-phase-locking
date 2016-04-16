# @Author: shubham
# @Description: Conservative two phase locking
# @Date:   2016-04-15 15:08:36
# @Last Modified by:   shubham
# @Last Modified time: 2016-04-16 06:49:17

from pprint import pprint
from random import randint, choice
from argparse import ArgumentParser

# Global data-structures
system_time = 0
locks = {}
ready, running, done = [], [], []

# argument parsing
parser = ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()
v = args.verbose

if __name__ == '__main__':

	# Input transactions
	tx = int(input())
	transaction_pointer = [0]*tx

	variable_set = set()
	transactions = {}
	timestamp = {}

	for transaction in range(tx):
		
		nint, ntime = list(map(int, input().split()))
		
		try: 
			timestamp[ntime].append(transaction)
		except:
			timestamp[ntime] = [transaction]

		transactions[transaction] = {'timestamp': ntime, 'operations': []}

		for instruction in range(nint):
			op, var = input().split()
			var = int(var)
			variable_set.add(var)
			
			transactions[transaction]['operations'].append((op, var))

	# print transactions
	for transaction, ops in transactions.items():
		print('Transaction:', transaction, '\nTimestamp:', ops['timestamp'])
		for op in ops['operations']:
			print('  '.join(map(str,op)))
	print()

	# Find write/read set of transactions
	read_write_set = {i:{} for i in range(tx)}
	for ntx, ops_time in transactions.items():

		ops = ops_time['operations']
		
		write, read = set(), set()
		for op in ops:
			if op[0] == 'W':
				write.add(int(op[1]))
			elif op[0] == 'R':
				read.add(int(op[1]))
			else:
				print('Some very miserable thing is gonna happen !')

		read = read - (read & write)
		read_write_set[ntx]['R'] = read
		read_write_set[ntx]['W'] = write

	# pprint(read_write_set)

	locks = {variable:{'R':[], 'W':None} for variable in variable_set}

	# start of schedule-generation
	print('Start of schedule generation:\n')
	while True:
		
		if v: print('\nSystem time:', system_time)

		# new transactions enter system
		try:
			newtx = timestamp[system_time]
			# print('Transactions entering system:', newtx)
		except:
			newtx = []
			# print('No transaction at time:', system_time)
			# continue

		# put new transactions in ready-queue
		ready.extend(newtx)
		
		# try to aquire locks for all ready transactions
		for ntx in ready[:]:
			try:
				write = read_write_set[ntx]['W']
				read = read_write_set[ntx]['R']
				# print(write, read)

				# chack if required write locks available
				for variable in write:
					if locks[variable]['W'] is not None:
						# print(ntx, 'Write lock busy', sep=': ')
						0/0

				# aquire all-write locks
				for variable in write:
					if locks[variable]['W'] == None:
						locks[variable]['W'] = ntx
					else:
						print('Something ver-very miserable happened !!')

				# aquire all-read locks
				for variable in read:
					if not locks[variable]['R']:
						locks[variable]['R'] = [ntx]
					else:
						locks[variable]['R'].append(ntx)
				
				# remove from ready and put in running 
				ready.remove(ntx)
				running.append(ntx)
				if v: print(ntx, 'All locks aquired', sep=': ')

			except:
				pass


		if running == []:
			system_time += 1
			continue

		# choose a random transaction from running to run
		this_will_run = choice(running)
		print(this_will_run, end=': ')

		current_operation = transaction_pointer[this_will_run]
		print('  '.join(map(str, transactions[this_will_run]['operations'][current_operation])))
		
		transaction_pointer[this_will_run] += 1
		
		# all operations successfully completed, restore locks
		if transaction_pointer[this_will_run] > len(transactions[this_will_run]['operations']) - 1:
			for variable, rwlock in locks.items():
				
				if rwlock['W'] == this_will_run:
					rwlock['W'] = None

				if this_will_run in rwlock['R']:
					rwlock['R'].remove(this_will_run)
			
			running.remove(this_will_run)
			done.append(this_will_run)
			if v: print(this_will_run, 'All locks released', sep=': ')


		# if all transactions are done, exit
		if len(done) == tx:
			break
		
		# last-line-dont-disturb
		system_time += 1

	# pprint(locks)
