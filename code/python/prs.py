# Used to ping
from subprocess import call

# GLHF
try:
	# Use grep and regex to filter ping output later.
	gag = 'grep -o "time=.\{4,8\}" | grep -o "[0-9].*"'
	
	# Runescape worlds as of 04/20/2017. We don't include F2P worlds.
	# These aren't worlds, or will be in the future.
	notw = ( 71, 72, 79, 80, 87, 88, 89, 90, 91, 92 )
	
	# All US worlds.
	usaw = [ 
		list(range(5, 8)),   list(range(13, 16)), 
		list(range(19, 25)), list(range(29, 33)),
		list(range(37, 41)), list(range(45, 49)), 
		list(range(53, 58)), list(range(61, 63)), 
		list(range(69, 71)), list(range(77, 79))
	]

	# Get world number to ping, or select ping all US worlds.
	get_num = int(input('[1]: Ping all\n[2]: Single world\nEnter: '))
    
	# Option to ping all US worlds.
	if get_num == 1:
		# For each list, we get its length. We use the length to index each list in usaw.
		# We then ping the server and filter it using grep + regex.	
		for lists in usaw:
			for worlds in lists[0:len(lists)]:
				call('printf %s:%s' % (worlds, '%1s'), shell=True)
				call('ping -c1 oldschool%s.runescape.com | %s' % (worlds, gag), shell=True)
	
	# Option to ping single world.
	elif get_num == 2:
		# We get world number.
		get_world = int(input('Enter world number: '))
	
		# We check to make sure it's an actual world. 
		if get_world in notw or get_world > 94:
			print('%s is not a world.' % get_world)

		# Otherwise, it will ping the server with the number from get_world.
		else:
			call('ping -c5 oldschool%s.runescape.com | %s' % (get_world, gag), shell=True)        

# Catches and cleans up text from keyboard interrupts.
except KeyboardInterrupt:
	pass

# Catches when get_num isn't a number.
except ValueError:
	print('That is not a number')
