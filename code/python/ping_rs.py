from bs4 import BeautifulSoup
from httplib2 import Http
from os import stat
from os.path import expanduser
from pathlib import Path
from re import compile, search
from stat import ST_MTIME
from subprocess import Popen, PIPE
from sys import platform
from time import time

file_save = Path(f"{expanduser('~')}/.osrs_worlds.html")
rsw_url = "http://oldschool.runescape.com/slu?order=WLMPA"
main_menu = ("All", "Region", "Specific")
regions = (
    "United States (East)", "United States (West)",
    "United Kingdom", "Germany", "Australia"
)


def file_handler(world_file, method, fetch):
    with open(world_file, method) as f:
        if fetch:
            status, response = Http().request(f"{rsw_url}")

            for lines in BeautifulSoup(response, "lxml").find_all("tr"):
                f.write(str(lines))

            selector(menu_construct(main_menu, "Ping types", True))
        else:
            return BeautifulSoup(f, "lxml")


def menu_construct(menu, whatis, updated):
    fin_str = f"\nSelect:\n - {whatis}:\n\n\t"

    for opt in range(1, len(menu) + 1):
        fin_str += f"{opt}] {menu[opt - 1]}"
        fin_str += "\n\n" if opt + 1 == len(menu) + 1 and not updated else "\n\t"

    if not updated:
        fin_str += " - Options:\n\n\t4] Update world list\n"

    fin_str += "\nEnter: "

    return int(input(fin_str))


def ping_command(url, ping_count):
    if (platform == "linux" or
            platform == "darwin"):
        ping_arg = "-c"
        ping_regex = compile(
            r"\w+/\w+/\w+/\w+ = (?P<min>\d*[.,]?\d*)/(?P<avg>\d*[.,]?\d*)/(?P<max>\d*[.,]?\d*)"
        )
    elif platform == "win32":
        ping_arg = "-n"
        ping_regex = compile(
            r"\w+ = (?P<min>\d+)ms, \w+ = (?P<max>\d+)ms, \w+ = (?P<avg>\d+)ms"
        )

    cmd = Popen(
        ["ping", ping_arg, str(ping_count), f"oldschool{url}.runescape.com"], stdout=PIPE
    ).stdout.read()

    form_data = ping_regex.search(str(cmd))

    min_ms = int(round(float(form_data.group("min"))))
    max_ms = int(round(float(form_data.group("max"))))
    avg_ms = int(round(float(form_data.group("avg"))))

    return min_ms, max_ms, avg_ms


def filter_worlds(world_file):
    worlds = file_handler(world_file, "r", False)
    wfilter = {}

    for info in worlds.find_all("tr"):
        title = info.contents[9].get_text()

        for loc in info.find_all("td", attrs={"class": compile("-{2}[A-U].")}):
            wnum = loc.find_previous("a")["id"].replace("slu-world-", "")
            full = wnum + ": " + title

            wfilter[full] = {}
            wfilter[full]["url"] = int(wnum) - 300
            wfilter[full]["zone"] = loc.get_text()

    return wfilter


def pings(specific, regioned):
    for title, info in filter_worlds(file_save).items():
        filter_num = title[0:title.index(":")]

        if not specific:
            if regioned:
                byreg = regions[0][:13] if regioned <= 2 else regions[regioned - 1]

                if (len(regions) >= regioned >= 1
                      and byreg in info["zone"]):
                    start_ping = ping_command(info["url"], 1)

                    if regioned >= 3:
                        print(f"{filter_num}: {start_ping[0]}")
                    elif (int(start_ping[0]) < 75
                            and regioned == 1):
                        print(f"{filter_num}: {start_ping[0]}")
                    elif (int(start_ping[0]) > 75
                            and regioned == 2):
                        print(f"{filter_num}: {start_ping[0]}")
            else:
                print(f"{filter_num}: {ping_command(info['url'], 1)[0]}")

        elif specific and specific in filter_num:
            print(f"\nPinging World {filter_num}..\n")
            start_ping = ping_command(info["url"], 20)

            print(f"{title}\n Min = {start_ping[0]} MS\n "
                  f"Max = {start_ping[1]} MS\n Avg = {start_ping[2]} MS\n")


def selector(selection):
    if selection == 1:
        pings(False, False)
    elif selection == 2:
        pings(False, menu_construct(regions, "Region", True))
    elif selection == 3:
        pings(input("\nEnter world number: "), False)
    elif selection == 4:
        file_handler(file_save, "w+", True)

try:
    if file_save.is_file():
        last_updated = round(time() - stat(file_save)[ST_MTIME])

        if last_updated > 604800:
            file_handler(file_save, "w+", True)
        else:
            selector(menu_construct(main_menu, "Ping types", False))
    else:
        file_handler(file_save, "a+", True)
except (KeyboardInterrupt, ValueError):
    pass
