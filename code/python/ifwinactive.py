from subprocess import Popen
import i3ipc
import time

i3 = i3ipc.Connection()
i = 0

def get_window():
	name = i3.get_tree().find_focused()
	return name.name

while True:
	time.sleep(0.2)
	
	if 'OSBuddy' in get_window() and i != 1:
		Popen('xdotool key alt+0', shell=True)
		i += 1
	elif not 'OSBuddy' in get_window() and i == 1:
		Popen('xdotool key alt+0', shell=True)
		i -= 1
