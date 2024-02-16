import time
import os
import dotenv

dotenv.load_dotenv()
MODE = os.getenv("MODE")
CURR_TIME = time.gmtime(int(os.getenv("LOCAL_GMT_CORRECTION")) + time.time())


class WeeklySchedule:
    def __init__(self, start_data, weekly_schedule):
        self.start_data = start_data
        self.monday = ""
        self.tuesday = ""
        self.wednesday = ""
        self.thursday = ""
        self.friday = ""
        self.saturday = ""
        self.sunday = ""
        self.weekly_schedule = weekly_schedule
        self.handle_weekly(weekly_schedule)

    def handle_weekly(self, weekly_schedule):
        for daily in weekly_schedule:
            match daily.wday_name:
                case "Понедельник":
                    self.monday = daily
                case "Вторник":
                    self.tuesday = daily
                case "Среда":
                    self.wednesday = daily
                case "Четверг":
                    self.thursday = daily
                case "Пятница":
                    self.friday = daily
                case "Суббота":
                    self.saturday = daily
                case "Воскресенье":
                    self.sunday = daily


class DailySchedule:
    def __init__(self, data: str, wday_name: str, classes: tuple, is_it_today: bool):
        self.data = data
        self.wday_name = wday_name
        self.classes = classes
        self.is_it_today = is_it_today


class UniversityClass:
    def __init__(self, class_start_time, class_end_time, subject, place):
        self.start_time = class_start_time
        self.end_time = class_end_time
        self.subject = subject
        self.place = place
        self.start_time_hour, self.start_time_min = map(
            int, class_start_time.split(":")
        )
        self.end_time_hour, self.end_time_min = map(int, class_end_time.split(":"))


def ddlWeek_creator(mode):
    if CURR_TIME.tm_wday != 6:
        first_current_week_day = time.strftime(
            "%d.%m.%Y %H:%M:%S",
            (
                CURR_TIME.tm_year,
                CURR_TIME.tm_mon,
                CURR_TIME.tm_mday - CURR_TIME.tm_wday,
                0,
                0,
                0,
                0,
                CURR_TIME.tm_yday - CURR_TIME.tm_wday,
                0,
            ),
        )
        is_sunday = False
    else:
        curr_time = time.gmtime(
            int(os.getenv("LOCAL_GMT_CORRECTION")) + time.time() + 90000
        )
        # прибавка 90000 для перехода на следующую неделю
        first_current_week_day = time.strftime(
            "%d.%m.%Y %H:%M:%S",
            (
                curr_time.tm_year,
                curr_time.tm_mon,
                curr_time.tm_mday - curr_time.tm_wday,
                0,
                0,
                0,
                0,
                curr_time.tm_yday - curr_time.tm_wday,
                0,
            ),
        )
        is_sunday = True

    return (
        (first_current_week_day.replace(" 00", " 0"), is_sunday)
        if mode != "DEV"
        else ("22.01.2024 0:00:00", is_sunday)
    )


def still_cookies(response):
    print(response.cookies)
    return response.cookies


def ru_wday_to_int(ru_wday: str) -> int:
    match ru_wday:
        case "Понедельник":
            return 0
        case "Вторник":
            return 1
        case "Среда":
            return 2
        case "Четверг":
            return 3
        case "Пятница":
            return 4
        case "Суббота":
            return 5
        case "Воскресенье":
            return 6


def find_target_day(obj):
    is_it_next_day = False

    for day in obj.weekly_schedule:
        if is_it_next_day:
            return day, is_it_next_day
        if CURR_TIME.tm_mday == int(day.data.split(".")[0]):
            if (CURR_TIME.tm_hour > int(day.classes[-1].end_time.split(":")[0])) or (
                CURR_TIME.tm_hour == day.classes[-1].end_time.split(":")[0]
                and CURR_TIME.tm_min > day.classes[-1].end_time.split(":")[1]
            ):
                is_it_next_day = True
                continue
            else:
                return day, is_it_next_day


def is_time_between(time, time_interval):
    pass
