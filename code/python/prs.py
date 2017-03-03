from subprocess import call

try:
    notw = (71, 72, 79, 80, 87, 88, 89, 90, 91, 92)
    get_num = int(input('Enter world number: '))
    
    if get_num in notw or get_num > 94:
        print('%s is not a world.' % get_num)
    else:
        call('ping oldschool%s.runescape.com' % (get_num), shell=True)        

except KeyboardInterrupt:
    pass

except ValueError:
    print('That is not a number')
