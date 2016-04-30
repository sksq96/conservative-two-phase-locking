# @Group-Members: 
# - Ashish Bedi (B13204)
# - Mukkaram Tailor (B13318)
# - Shubham Chandel (B13231)
# @Description: Basic two phase locking - Wait & Die
# @Date:   2016-04-15 15:08:36
# @Last Modified by:   shubham
# @Last Modified time: 2016-04-24 23:04:35

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


def raiseException(): 0/0

def releaseLocks(tx, what=None):
	for variable, rwlock in locks.items():
		
		if rwlock['W'] == tx:
			rwlock['W'] = None

		if tx in rwlock['R']:
			rwlock['R'].remove(tx)

	if what:
		if v: print(tx, 'Aborted.', sep=': ')
	else:
		if v: print(tx, 'All locks released', sep=': ')


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
	print('All transactions:\n')
	for transaction, ops in transactions.items():
		print('Transaction:', transaction, '\nTimestamp:', ops['timestamp'])
		for op in ops['operations']:
			print('  '.join(map(str,op)))
	print()


	locks = {variable:{'R':[], 'W':None} for variable in variable_set}

	# start of schedule-generation
	print('Start of schedule generation:')
	
	# for _ in range(25):
	while True:
		
		if v: print('\nSystem time:', system_time)

		# new transactions enter system
		try:
			newtx = timestamp[system_time]
			if v: print('Transactions entering system:', newtx)
		except:
			newtx = []
			# print('No transaction at time:', system_time)
			# continue

		# put new transactions in ready-queue
		ready.extend(newtx)


		if ready == []:
			system_time += 1
			continue


		while True:

			# choose a random transaction from running to run
			this_will_run = choice(ready)
			# print(this_will_run)
			current_operation = transaction_pointer[this_will_run]

			op, variable = transactions[this_will_run]['operations'][current_operation]
			
			iswrite = locks[variable]['W']
			isread = locks[variable]['R']

			try:
				# W operation
				if op is 'W':

					# W-lock free
					if iswrite is None:
						
						# R-lock free
						if isread == []:
							locks[variable]['W'] = this_will_run
						
						# Only I have aquired R-lock
						elif (this_will_run in isread) and len(isread) == 1:
							locks[variable]['R'].remove(this_will_run)
							locks[variable]['W'] = this_will_run
						
						# Only "Someone else" have aquired R-lock
						elif len(isread) == 1:

							# I am young
							if this_will_run >= isread[0]:
								transaction_pointer[this_will_run] = 0
								releaseLocks(this_will_run)
								raiseException()


							# I am old
							elif this_will_run < isread[0]: raiseException()

							
						# Multiple Tx have aquired R-lock
						else: raiseException()


					elif this_will_run == iswrite:
						pass					

					# W-lock not free
					# I am young
					elif this_will_run > iswrite:
						transaction_pointer[this_will_run] = 0
						releaseLocks(this_will_run)
						raiseException()


					# I am old
					elif this_will_run < iswrite: raiseException()

					else: raiseException()

				
				# R operation
				elif op is 'R':
					
					if this_will_run in isread:
						pass

					elif (iswrite is None):
						locks[variable]['R'].append(this_will_run)
					
					elif this_will_run == iswrite:
						pass

					# I am young
					elif this_will_run >= iswrite:
						transaction_pointer[this_will_run] = 0
						releaseLocks(this_will_run)
						raiseException()
					
					# I am old
					elif this_will_run < iswrite: raiseException()

					else: raiseException()

				# Neither R nor W
				else: print('Something bad happened!')

			except:
				continue


			transaction_pointer[this_will_run] += 1
			# print(this_will_run, transaction_pointer[this_will_run])
			print(str(this_will_run) + ':', '  '.join(map(str, transactions[this_will_run]['operations'][current_operation])))

			# all operations successfully completed, restore locks
			if transaction_pointer[this_will_run] > len(transactions[this_will_run]['operations']) - 1:
				
				releaseLocks(this_will_run, 1)

				# Shift tx from ready --> done
				ready.remove(this_will_run)
				done.append(this_will_run)
				if v: print(this_will_run, 'All locks released', sep=': ')


			break
		
		# pprint(locks)
		# if all transactions are done, exit
		if len(done) == tx:
			break
		
		# last-line-dont-disturb
		system_time += 1

	# pprint(locks)

