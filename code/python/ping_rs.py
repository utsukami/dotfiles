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

home = expanduser("~")
file_save = Path("{}/.osrs_worlds.html".format(home))


def ping_command(world_url, ping_count):
    if (platform == "linux" or
            platform == "darwin"):

        count_arg = "-c"
        compile_ping_re = compile(
            r"\w+/\w+/\w+/\w+ = (?P<min>\d*[.,]?\d*)/"
            "(?P<avg>\d*[.,]?\d*)/(?P<max>\d*[.,]?\d*)"
        )

    elif platform == "win32":
        count_arg = "-n"
        compile_ping_re = compile(
            r"\w+ = (?P<min>\d+)ms, \w+ = (?P<max>\d+)ms, \w+ = (?P<avg>\d+)ms"
        )

    do_command = str(
        Popen([
            "ping", count_arg, str(ping_count),
            "{}.{}"
            .format(
                world_url.lower().replace(" ", ""),
                "runescape.com"
            )
        ],
            stdout=PIPE
        ).stdout.read()
    )

    form_data = compile_ping_re.search(do_command)

    min_ms = int(round(float(form_data.group("min"))))
    max_ms = int(round(float(form_data.group("max"))))
    avg_ms = int(round(float(form_data.group("avg"))))

    return min_ms, max_ms, avg_ms


def parse_html_data(reply, region_choice, specific_world):
    with open(file_save) as file_contents:
        worlds = BeautifulSoup(file_contents, "lxml")

    recommend = {}

    if 3 >= reply > 0:
        for info in worlds.find_all("tr"):
            title = info.contents[9].get_text()

            for loc in info.find_all(
                    "td", attrs={"class": compile("-{2}[A-U].")}):
                number = loc.find_previous("a")
                number_filter = number["id"].replace("slu-world-", "")

                for url in number:
                    url = url.replace(" ", "").lower()
                    full_title = number_filter + ": " + title

                    if reply == 1:
                        start_ping = ping_command(url, 1)

                        print(number_filter + ": ", str(start_ping[0]) + " MS")
                        recommend[full_title] = int(start_ping[0])

                    elif (reply == 2 and
                            region_choice in loc.get_text()):

                        start_ping = ping_command(url, 1)

                        print(number_filter + ": ", str(start_ping[0]) + " MS")
                        recommend[full_title] = int(start_ping[0])

                    elif reply == 3:
                        if specific_world in number_filter:
                            print(
                                "\nChecking ping on world {}..\n"
                                "\nWorld #: Title\n Min = _ MS\n"
                                " Max = _ MS\n Avg = _ MS\n"
                                .format(number_filter)
                            )

                            start_ping = ping_command(url, 10)

                            print(
                                full_title + "\n",
                                "Min = {} MS\n Max = {} MS\n Avg = {} MS\n"
                                .format(
                                    start_ping[0], start_ping[1], start_ping[2]
                                )
                            )

    if recommend:
        print("\nRecommended worlds:")
        for lowest in range(1, 4):
            get_recommend = min(recommend.items(), key=itemgetter(1))
            print("\n  ", get_recommend[0], "\n    ", get_recommend[1], " MS")
            recommend.pop(get_recommend[0])
        print("\r")

    if platform == "win32":
        input("Hit Return to exit.")


def file_get(method, message):
    http = Http()
    status, response = http.request(
        "http://oldschool.runescape.com/slu?order=WLMPA"
    )
    data = BeautifulSoup(response, "lxml")

    with open(file_save, method) as f:
        for lines in data.find_all("tr"):
            f.write(str(lines))

    print("\n{} file..\n".format(message))


def selector(selection):
    regions = ("United States", "United Kingdom", "Germany", "Australia")

    try:
        if selection:
            get_select = int(
                input(
                    "Select:\n - Ping types:\n\n\t1] {}"
                    "2] {}3] {} - Options:\n\n\t4] {}"
                    .format(
                        "All\n\t", "Region\n\t", "Specific\n\n",
                        "Update world list\n\nEnter: "
                    )
                )
            )

        else:
            get_select = int(
                input(
                    "Select:\n Ping types:\n\n\t1] All \n\t2] Region "
                    "\n\t3] Specific\n\nEnter: "
                )
            )

        if get_select == 1:
            print("\nChecking ping on every world..\n")
            parse_html_data(get_select, None, None)

        elif get_select == 2:
            region_select = int(
                input(
                    "\nSelect:\n - Region:\n\n\t1] {}2] {}3] {}4] {}\nEnter: "
                    .format(
                        regions[0] + "\n\t", regions[1] + "\n\t",
                        regions[2] + "\n\t", regions[3] + "\n\t"
                    )
                )
            )

            if len(regions) >= region_select >= 1:
                print(
                    "\nChecking ping in the {} region..\n"
                    .format(regions[region_select - 1])
                )

                parse_html_data(get_select, regions[region_select - 1], None)

        elif get_select == 3:
            world_num = input("\nEnter world number: ")
            parse_html_data(get_select, None, world_num)

        elif get_select == 4:
            file_get("w+", "Fetching new worlds")
            selector(None)

    except ValueError:
        pass


try:
    if file_save.is_file():
        last_updated = round(time() - stat(file_save)[ST_MTIME])

        if last_updated > 604800:
            file_get("w+", "Worlds file outdated, fetching new")
            selector(None)

        else:
            selector(True)

    else:
        file_get("a+", "Worlds file not found, creating")
        selector(None)

except KeyboardInterrupt:
    pass
