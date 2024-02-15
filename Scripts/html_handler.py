import bs4
from collections import namedtuple
import re
import os
import dotenv

import time

from Scripts.utils import UniversityClass, ru_wday_to_int, DailySchedule, WeeklySchedule


dotenv.load_dotenv()
DDLFAC = os.getenv("ddlFac")
DDLCOURSE = os.getenv("ddlCourse")
DDLGROUP = os.getenv("ddlGroup")
DDLDEP = os.getenv("ddlDep")


def handle_target_schedule(response, start_week_data):
    # with open('../templates/tample_shedule.html', 'r') as f:
    #     a = f.read()

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    separator = soup.find(attrs={"class": "row row-separator"})
    # curr_time = time.gmtime(int(os.getenv('LOCAL_GMT_CORRECTION')) + time.time() + 288000)

    weekly_schedule = list()
    target_stibligs = list()
    daily_schedule = list()
    # print(response.text)
    # print(separator)
    for stibling in separator.find_next_siblings(attrs={"class": "row"}):

        if stibling != separator:
            if stibling.find_next(attrs={"class": "cell-header"}):
                continue

            target_stibligs.append(stibling)

        else:
            if not target_stibligs:
                continue

            data = target_stibligs[0].find_next(attrs={"class": "date"}).text
            wday = target_stibligs[0].find_next(attrs={"class": "day"}).text
            is_it_today = (
                True
                if target_stibligs[0].find_next(attrs={"class": "cell-data today-date"})
                else False
            )

            for target_stigling in target_stibligs:
                if duration_interval := target_stigling.find_next(
                    attrs={"class": "cell-time"}
                ):
                    duration_interval = duration_interval.text.split("-")
                    daily_schedule.append(
                        UniversityClass(
                            class_start_time=duration_interval[0],
                            class_end_time=duration_interval[1],
                            subject=target_stigling.find_next(
                                attrs={"class": "cell-discipline"}
                            ).text,
                            place=target_stigling.find_next(
                                attrs={"class": "cell-auditory"}
                            ).text,
                        )
                    )

            weekly_schedule.append(
                DailySchedule(
                    data, wday, tuple(daily_schedule), is_it_today=is_it_today
                )
            )
            target_stibligs.clear()
            daily_schedule.clear()

    return WeeklySchedule(start_data=start_week_data, weekly_schedule=weekly_schedule)


def asp_variables_parser(response) -> namedtuple:
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    Asp_vars = namedtuple(
        "asp_vars", ["VIEWSTATE", "VIEWSTATEGENERATOR", "EVENTVALIDATION"]
    )
    return Asp_vars(
        soup.find(id="__VIEWSTATE")["value"],
        soup.find(id="__VIEWSTATEGENERATOR")["value"],
        soup.find(id="__EVENTVALIDATION")["value"],
    )


def selected_param_parser(
    response,
    ddlFac=DDLFAC,
    ddlCourse=DDLCOURSE,
    ddlGroup=DDLGROUP,
    ddlDep=DDLDEP,
    default_selections=False,
):
    # mode для группы, тк для получения списка групп не дефолтного факультета(например) необходимо изменить факультет
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    form_vars = namedtuple("form_vars", ["ddlFac", "ddlCourse", "ddlDep", "ddlGroup"])
    res_namedtuple = namedtuple("res_namedtuple", ["target_param", "default_param"])
    default_param = None
    if not soup.find(id="ddlGroup").find(selected="selected")["value"]:
        without_group_mode = True
    else:
        without_group_mode = False

    if default_selections:
        default_param = form_vars(
            soup.find(id="ddlFac").find(selected="selected")["value"],
            soup.find(id="ddlCourse").find(selected="selected")["value"],
            soup.find(id="ddlDep").find(selected="selected")["value"],
            soup.find(id="ddlGroup").find(selected="selected")["value"],
        )

    if without_group_mode:
        target_param = form_vars(
            soup.find(string=re.compile(f" *{ddlFac} *")).find_parent("option")[
                "value"
            ],
            soup.find(string=re.compile(f" *{ddlCourse} *")).find_parent("option")[
                "value"
            ],
            soup.find(string=re.compile(f" *{ddlDep} *")).find_parent("option")[
                "value"
            ],
            None,
        )
    else:
        target_param = form_vars(
            soup.find(string=re.compile(f" *{ddlFac} *")).find_parent("option")[
                "value"
            ],
            soup.find(string=re.compile(f" *{ddlCourse} *")).find_parent("option")[
                "value"
            ],
            soup.find(string=re.compile(f" *{ddlDep} *")).find_parent("option")[
                "value"
            ],
            soup.find(string=re.compile(f" *{ddlGroup} *")).find_parent("option")[
                "value"
            ],
        )

    print(target_param, default_param)

    return res_namedtuple(target_param, default_param)
