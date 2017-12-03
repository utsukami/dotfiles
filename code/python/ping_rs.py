from bs4 import BeautifulSoup as bs
from pathlib import Path
from os.path import expanduser as euser
import re, subprocess, httplib2

home = euser('~')
file_save = Path('{}/.osrs_worlds.html'.format(home))
regions = ( 'United States', 'United Kingdom', 'Germany', 'Australia' )
rs = 'runescape.com'
filter_avg = 'grep -o \'[=].\{1,500\}[\/]\' | tr -d \'=\' | sed \'s/.$//\''
filter_one = 'grep -o "time=.\{4,8\}" | grep -o "[0-9].*"'

def ping_cmd(world_num, world_title, world_url, ping_count):
    if ping_count == 1: 
        do_command = subprocess.Popen('ping -c {} {}.{} | {}'.format(
            ping_count, world_url.lower().replace(' ', ''), rs, filter_one),
        stdout=subprocess.PIPE, bufsize=1, shell=True)
    
    else:
        do_command = subprocess.Popen('echo $(ping -q -c {} {}.{} | {}; echo \'{}\')'.format(
            ping_count, world_url.lower().replace(' ', ''), rs, filter_avg, 'ms'),
        stdout=subprocess.PIPE, bufsize=1, shell=True)
    
    for line in iter(do_command.stdout.readline, b''):
        return world_num['id'].replace('slu-world-', ''), ': ', world_title, "\n ", line.decode('ascii') 
    do_command.stdout.close()
    do_command.wait()

def ping_parse_data(reply, region_choice, num_to_ping):
    for info in worlds.find_all('tr'):
        title = info.contents[9].get_text()
        for loc in info.find_all('td', attrs={'class': re.compile('-{2}[A-U].')}):
            number = loc.find_previous('a')
            for url in number:
                if reply == 1:
                    print(''.join(map(str, (ping_cmd(number, title, url, 1)))))
                elif reply == 2:
                    if region_choice in loc.get_text():
                        print(''.join(map(str, (ping_cmd(number, title, url, 1)))))
                elif reply == 3:
                    if num_to_ping in number['id'].replace('slu-worlds-', ''):
                        print('\nChecking ping on world {}, please wait..\n'.format(num_to_ping))
                        print('#: Title\n min / avg / max (ms)\n')
                        print(''.join(map(str, (ping_cmd(number, title, url, 10)))))

def file_get():
    http = httplib2.Http()
    status, response = http.request('http://oldschool.runescape.com/slu?order=WLMPA')
    data = bs(response, 'lxml')

    with open(file_save, 'w') as fp:
        for lines in data.find_all('tr'):
            fp.write(str(lines))

    print('\nFetching new world file..\n')

def selector(selection):
    if selection == 1:
        print('\nChecking ping on every world..\n')
        ping_parse_data(selection, None, None)

    elif selection == 2:
        region_select = int(input('\nSelect:\n Region:\n\n\t1] {}2] {}3] {}4] {}\nEnter: '.format(
            regions[0] + '\n\t', regions[1] + '\n\t', regions[2] + '\n\t', regions[3] + '\n\t')))
        print('\nChecking ping in the {} region..\n'.format(regions[region_select -1]))
        ping_parse_data(selection, regions[region_select - 1], None)

    elif selection == 3:
        gimme_num = input('\nEnter world number: ')
        ping_parse_data(selection, None, gimme_num)

if file_save.is_file():
    get_select = int(input('Select:\n - Ping types:\n\n\t1] {}2] {}3] {} - Options:\n\n\t4] {}'.format(
        'All\n\t', 'Region\n\t', 'Specific\n\n', 'Update world list\n\nEnter: ')))
    with open(file_save) as file_contents:
        worlds = bs(file_contents, 'lxml')

    selector(get_select)

    if get_select == 4:
        file_get()
    
        with open(file_save) as file_contents:
            worlds = bs(file_contents, 'lxml')
    
        gsec = int(input('Select:\n Ping types:\n\n\t1] All \n\t2] Region \n\t3] Specific\n\nEnter: '))
        selector(gsec)

else:
    file_get()
    gsec_none = int(input('Select:\n Ping types:\n\n\t1] All \n\t2] Region \n\t3] Specific\n\nEnter: '))
    
    with open(file_save) as file_contents:
        worlds = bs(file_contents, 'lxml')
    
    selector(gsec_none)
