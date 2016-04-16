# @Author: shubham
# @Date:   2016-04-15 15:13:19
# @Last Modified by:   shubham
# @Last Modified time: 2016-04-16 01:54:54

from random import randint, choice
from optparse import OptionParser

# argument parsing
parser = OptionParser()
parser.add_option("-x", dest="ntx", default="1")
parser.add_option("-i", dest="nint", default="1")
parser.add_option("-t", "--ntime", dest="ntime", default="0")
parser.add_option("-v", "--nvar", dest="nvar", default="3")
options, parser = parser.parse_args()

# parameters
ntx = int(options.ntx)
nint = int(options.nint)
ntime = int(options.ntime)
nvar = int(options.nvar)

operations = ['W', 'R']

print(ntx)
for transaction in range(ntx):
	
	num_instructions = randint(1, nint)
	timestamp = randint(0, ntime)
	print(num_instructions, timestamp)

	for instruction in range(num_instructions):
		print(choice(operations), randint(0, nvar))


