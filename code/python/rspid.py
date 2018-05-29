import sys, os, subprocess
home = os.path.expanduser("~")

try:
    arg_num = int(sys.argv[1]) + 1

except IndexError:
    arg_num = 4

for x in range(1,arg_num):
    f = open("{}/code/xdotool/acc{}".format(home, x), "r+")
    d = f.readlines()
    f.seek(0)
    for line in d:
        if line == "PID":
            f.truncate()
    pid = subprocess.Popen("{} | {} | {};".format(
        "xprop", "grep PID", "grep -o '[0-9]*'"), 
        stdout=subprocess.PIPE, bufsize=1, shell=True)

    for line in iter(pid.stdout.readline, b''):
        f.write("PID={}\n".format(line.decode("ascii")))
    f.close()
