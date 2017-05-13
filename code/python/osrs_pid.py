import os

home = os.path.expanduser('~')
code = "for x in $(xdotool search --pid $PID); do xdotool mousemove --window $x 375 250; done"

for x in range(1,4):
	f = open('%s/code/bash/xdo/acc%s' % (home, x), 'w')
	f.seek(0)
	pid = input('Enter PID #%s: ' % (x))
	f.write('PID=%s\n\n%s' % (pid, code))
	f.close()
