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

file_save = Path("{}/.osrs_worlds.html".format(expanduser("~")))
main_menu = ("All", "Region", "Specific")
regions = (
    "United States (East)",
    "United States (West)",
    "United Kingdom",
    "Germany",
    "Australia"
)


def file_get(method, statement, action):
    http = Http()
    status, response = http.request(
        "http://oldschool.runescape.com/slu?order=WLMPA"
    )
    data = BeautifulSoup(response, "lxml")

    with open(file_save, method) as f:
        for lines in data.find_all("tr"):
            f.write(str(lines))

    print("\nFile:   {}\nAction: {}\n".format(statement, action))


def menu_construct(menu, whatis, lister, updated):
    full_string = "\nSelect:\n - {}:\n\n\t".format(whatis)

    for entries in range(1, menu + 1):
        if entries + 1 == menu + 1:
            if updated:
                full_string += "{}] {}".format(entries, lister[entries - 1])

            else:
                full_string += "{}] {}\n\n".format(entries, lister[entries - 1])

        else:
            full_string += "{}] {}\n\t".format(entries, lister[entries - 1])

    if not updated:
        full_string += " - Options:\n\n\t4] Update world list"

    full_string += "\n\nEnter: "

    return full_string


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


def start_ping(reply, region_choice, specific_world):
    with open(file_save) as file_contents:
        worlds = BeautifulSoup(file_contents, "lxml")

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

                    if reply == 3:
                        if specific_world in number_filter:
                            print(
                                "\nChecking ping on world {}..\n"
                                .format(number_filter)
                            )

                            start_ping = ping_command(url, 20)

                            print(
                                full_title + "\n",
                                "Min = {} MS\n Max = {} MS\n Avg = {} MS\n"
                                .format(
                                    start_ping[0], start_ping[1], start_ping[2]
                                )
                            )

                    else:
                        start_ping = ping_command(url, 1)

                        if reply == 1:
                            print(number_filter + ": ", str(start_ping[0]) + " MS")

                        if (reply == 2 and
                                region_choice in loc.get_text()):

                            if specific_world:
                                if (specific_world == 1 and
                                        int(start_ping[0]) < 75):

                                    print(number_filter + ": ", str(start_ping[0]) + " MS")

                                elif (specific_world == 2 and
                                        int(start_ping[0]) > 75):

                                    print(number_filter + ": ", str(start_ping[0]) + " MS")

                            else:
                                    print(number_filter + ": ", str(start_ping[0]) + " MS")

    if platform == "win32":
        input("Hit Return to exit.")


def selector(selection):
    try:
        if selection == 1:
            print("\nChecking ping on every world..\n")
            start_ping(selection, None, None)

        elif selection == 2:
            region_select = int(
                input(menu_construct(len(regions), "Region", regions, 1))
            )

            if len(regions) >= region_select >= 1:
                print(
                    "\nChecking ping in the {} region..\n"
                    .format(regions[region_select - 1])
                )

                if (region_select == 1 or
                        region_select == 2):

                    strip_coast = regions[0][:regions[0].index("(") - 1]
                    start_ping(selection, strip_coast, region_select)

                else:
                    start_ping(selection, regions[region_select - 1], None)

        elif selection == 3:
            world_num = input("\nEnter world number: ")
            start_ping(selection, None, world_num)

        elif selection == 4:
            file_get("w+", "[OUTDATED]" ,"[UPDATE]")
            selector(int(input(menu_construct(
                len(main_menu), "Ping types", main_menu, 1)))
            )

    except ValueError:
        pass


try:
    if file_save.is_file():
        last_updated = round(time() - stat(file_save)[ST_MTIME])

        if last_updated > 604800:
            file_get("w+", "[OUTDATED]", "[UPDATE]")
            selector(int(input(menu_construct(
                len(main_menu), "Ping types", main_menu, 1)))
            )

        else:
            selector(int(input(menu_construct(
                len(main_menu), "Ping types", main_menu, 0)))
            )

    else:
        file_get("a+", "[NOT FOUND]", "[CREATE]")
        selector(int(input(menu_construct(
            len(main_menu), "Ping types", main_menu, 1)))
        )

except KeyboardInterrupt:
    pass
