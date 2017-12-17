import i3ipc, time, re

urg_color = '#d56669'
nor_color = '#ffffff'
foc_color = '#ffffff'
hil_color = '#FFFFFF'
dat_color = '#38C5F3'

i3 = i3ipc.Connection()

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]

    return sorted(l, key = alphanum_key)

def get_wk():
    colors = ''
    foc_wk = ''
    urg_wk = ''
    wk_name = []

    for wk in i3.get_workspaces():
        wk_name.append(wk.name)
        if wk.focused:
            foc_wk = wk.name
        elif wk.urgent:
            urg_wk = wk.name

    for workspace_names in (natural_sort(wk_name)):
        if workspace_names == foc_wk:
            colors += ' %{{+u}}%{{U{}}}%{{F{}}} '.format(foc_color, hil_color) + workspace_names + ' %{F-}%{U-}%{-u}'
        elif workspace_names == urg_wk:
            colors += ' %{{+u}}%{{U{}}}%{{F{}}} '.format(urg_color, hil_color) + workspace_names + ' %{F-}%{U-}%{-u}'
        else:
            colors += ' %{{F{}}} '.format(nor_color) + workspace_names + ' %{F-}'
    return colors 

def get_tida():
    ti = time.strftime('%H:%M')
    da = time.strftime('%m/%d/%Y')

    return ('%{{r}}%{{U{}}}%{{F{}}}'.format(dat_color, hil_color, hil_color) + ti + ' ' + da + ' ' + '%{F-}%{U-}')

#def get_focw():
 #   foc_win = i3.get_tree().find_focused()

  #  return ('%{{c}}%{{U{}}}%{{F{}}}'.format(hil_color, hil_color) + foc_win.name + '%{F-}%{U-}')

def main():
    while True:
        print(format(get_wk() + get_tida()))
        time.sleep(0.2)

main()
