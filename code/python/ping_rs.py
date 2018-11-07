from bs4 import BeautifulSoup
from operator import itemgetter
from pathlib import Path
from os.path import expanduser
import re, subprocess, httplib2

home = expanduser("~")
file_save = Path("{}/.osrs_worlds.html".format(home))
regions = ("United States", "United Kingdom", "Germany", "Australia")
recommend = {}

loc_re = re.compile("-{2}[A-U].")
ping_re = re.compile(
    r"\w+/\w+/\w+/\w+ = (?P<min>\d*[.,]?\d*)/"
    "(?P<avg>\d*[.,]?\d*)/(?P<max>\d*[.,]?\d*)"
)


def ping_cmd(world_url, ping_count):
    do_command = str(
        subprocess.Popen([
            "ping", "-c", str(ping_count),
            "{}.{}".format(
                world_url.lower().replace(" ", ""), "runescape.com")
            ],
            stdout=subprocess.PIPE
        ).stdout.read()
    )

    form_data = ping_re.search(do_command)

    min_ms = int(round(float(form_data.group("min"))))
    max_ms = int(round(float(form_data.group("max"))))
    avg_ms = int(round(float(form_data.group("avg"))))

    return min_ms, max_ms, avg_ms


def ping_parse_data(reply, region_choice, num_to_ping):
    if 3 >= reply > 0:
        for info in worlds.find_all("tr"):
            title = info.contents[9].get_text()

            for loc in info.find_all("td", attrs={"class": re.compile(loc_re)}):
                number = loc.find_previous("a")
                number_filter = number["id"].replace("slu-world-", "")

                for url in number:
                    url = url.replace(" ", "").lower()
                    full_title = number_filter + ": " + title

                    if reply == 3:
                        if num_to_ping in number_filter:
                            print(
                                "\nChecking ping on world {}..\n"
                                "\nWorld #: Title\n Min = _ MS\n"
                                " Max = _ MS\n Avg = _ MS\n"
                                .format(number_filter)
                            )

                            start_ping = ping_cmd(url, 10)

                            print(
                                full_title + "\n"
                                " Min = {} MS\n Max = {} MS\n Avg = {} MS\n"
                                .format(
                                    start_ping[0], start_ping[1], start_ping[2]
                                )
                            )

                    else:
                        if reply == 1:
                            start_ping = ping_cmd(url, 1)

                            print(
                                number_filter + ": ",
                                str(start_ping[0]) + " MS"
                            )
                            recommend[full_title] = int(start_ping[0])

                        elif (reply == 2 and
                                region_choice in loc.get_text()):

                            start_ping = ping_cmd(url, 1)

                            print(
                                number_filter + ": ",
                                str(start_ping[0]) + " MS"
                            )
                            recommend[full_title] = int(start_ping[0])

    if recommend:
        print("\nRecommend worlds:")
        for x in range(1, 4):
            gimme = min(recommend.items(), key=itemgetter(1))
            print("\n  ", gimme[0], "\n    ", gimme[1], " MS")
            recommend.pop(gimme[0])
        print("\r")


def file_get(method):
    http = httplib2.Http()
    status, response = http.request(
        "http://oldschool.runescape.com/slu?order=WLMPA"
    )
    data = BeautifulSoup(response, "lxml")

    with open(file_save, method) as fp:
        for lines in data.find_all("tr"):
            fp.write(str(lines))

    print("\nFetching new world file..\n")


def selector(selection):
    if selection == 1:
        print("\nChecking ping on every world..\n")
        ping_parse_data(selection, None, None)

    elif selection == 2:
        region_select = int(
            input(
                "\nSelect:\n - Region:\n\n\t1] {}2] {}3] {}4] {}\nEnter: "
                .format(
                    regions[0] + "\n\t", regions[1] + "\n\t",
                    regions[2] + "\n\t", regions[3] + "\n\t"
                )
            )
        )

        print("\nChecking ping in the {} region..\n".format(
            regions[region_select -1])
        )
        ping_parse_data(selection, regions[region_select - 1], None)

    elif selection == 3:
        gimme_num = input("\nEnter world number: ")
        ping_parse_data(selection, None, gimme_num)


if file_save.is_file():
    get_select = int(
        input(
            "Select:\n - Ping types:\n\n\t1] {}2] {}3] {} - Options:\n\n\t4] {}"
            .format(
                "All\n\t", "Region\n\t", "Specific\n\n",
                "Update world list\n\nEnter: "
            )
        )
    )
    
    with open(file_save) as file_contents:
        worlds = BeautifulSoup(file_contents, "lxml")

    selector(get_select)

    if get_select == 4:
        file_get("w+")
    
        with open(file_save) as file_contents:
            worlds = BeautifulSoup(file_contents, "lxml")
    
        get_select = int(
            input(
                "Select:\n Ping types:\n\n\t1] All \n\t2] Region"
                "\n\t3] Specific\n\nEnter: "
            )
        )
        selector(get_select)

else:
    file_get("a+")
    get_select = int(
        input(
            "Select:\n Ping types:\n\n\t1] All \n\t2] Region "
            "\n\t3] Specific\n\nEnter: "
        )
    )
    
    with open(file_save) as file_contents:
        worlds = BeautifulSoup(file_contents, "lxml")
    
    selector(get_select)
