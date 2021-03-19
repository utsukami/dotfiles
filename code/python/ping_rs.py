from bs4 import BeautifulSoup
from httplib2 import Http
from operator import itemgetter
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
regions = ("United States (East)", "United States (West)",
           "United Kingdom", "Germany", "Australia")


def file_get(method, world_file):
    status, response = Http().request(f"{rsw_url}")
    data = BeautifulSoup(response, "lxml")

    with open(world_file, method) as f:
        for lines in data.find_all("tr"):
            f.write(str(lines))

    selector(int(input(menu_construct(main_menu, "Ping types", 1))))


def menu_construct(menu, whatis, updated):
    full_string = f"\nSelect:\n - {whatis}:\n\n\t"

    for entries in range(1, len(menu) + 1):
        full_string += f"{entries}] {menu[entries -1]}"

        if not entries + 1 == len(menu) + 1:
            full_string += "\n\t"
        else:
            if not updated:
                full_string += "\n\n"
    if not updated:
        full_string += " - Options:\n\n\t4] Update world list"

    full_string += "\n\nEnter: "

    return full_string


def ping_command(url, ping_count):
    if (platform == "linux" or
            platform == "darwin"):
        count_arg = "-c"
        ping_reg = compile(r"\w+/\w+/\w+/\w+ = (?P<min>\d*[.,]?\d*)/"
                            "(?P<avg>\d*[.,]?\d*)/(?P<max>\d*[.,]?\d*)")

    elif platform == "win32":
        count_arg = "-n"
        ping_reg = compile(r"\w+ = (?P<min>\d+)ms, \w+ = "
                            "(?P<max>\d+)ms, \w+ = (?P<avg>\d+)ms")

    cmd = Popen(["ping", count_arg, str(ping_count),
                f"{url.replace(' ', '')}.runescape.com"],stdout=PIPE).stdout.read()

    form_data = ping_reg.search(str(cmd))

    min_ms = int(round(float(form_data.group("min"))))
    max_ms = int(round(float(form_data.group("max"))))
    avg_ms = int(round(float(form_data.group("avg"))))

    return min_ms, max_ms, avg_ms


def filter_worlds(world_file):
    filtered_worlds = {}

    with open(world_file) as f:
        worlds = BeautifulSoup(f, "lxml")

    for info in worlds.find_all("tr"):
        title = info.contents[9].get_text()

        for loc in info.find_all("td", attrs={"class": compile("-{2}[A-U].")}):
            number = loc.find_previous("a")
            number_filter = number["id"].replace("slu-world-", "")

            for url in number:
                url = url.replace(" ","").lower()
                full_title = number_filter + ": " + title

                filtered_worlds[full_title] = {}
                filtered_worlds[full_title]["url"] = url
                filtered_worlds[full_title]["region"] = loc.get_text()

    return filtered_worlds


def pings(specific, region_choice):
    for title, info in filter_worlds(file_save).items():
        filter_num = title[0:title.index(":")]

        if not specific:
            start_ping = ping_command(info["url"], 1)

            if region_choice:
                if len(regions) >= region_choice >= 1:
                    ping_region = regions[region_choice - 1]

                    if region_choice <= 2:
                        ping_region = regions[0][:regions[0].index("(") - 1]

                    if ping_region in info["region"]:
                        if region_choice <= 2:
                            if (region_choice == 1
                                    and int(start_ping[0]) < 75):
                                print(f"{filter_num}: {start_ping[0]}")

                            elif (region_choice == 2
                                    and int(start_ping[0]) > 75):
                                print(f"{filter_num}: {start_ping[0]}")
                        else:
                            print(f"{filter_num}: {start_ping[0]}")
            else:
                print(f"{filter_num}: {start_ping[0]}")
        else:
            if specific in filter_num:
                print(f"\nPinging World {filter_num}..\n")
                start_ping = ping_command(info["url"], 20)

                print(f"{title}\n Min = {start_ping[0]} MS\n "
                      f"Max = {start_ping[1]} MS\n Avg = {start_ping[2]} MS\n")


def selector(selection):
    if selection == 1:
        pings(None, None)
    elif selection == 2:
        pings(None, int(input(menu_construct(regions, "Region", 1))))
    elif selection == 3:
        pings(input("\nEnter world number: "), None)
    elif selection == 4:
        file_get("w+", file_save)

try:
    if file_save.is_file():
        last_updated = round(time() - stat(file_save)[ST_MTIME])

        if last_updated > 604800:
            file_get("w+", file_save)
        else:
            selector(int(input(menu_construct(main_menu, "Ping types", 0))))
    else:
        file_get("a+", file_save)

except (KeyboardInterrupt, ValueError):
    pass
