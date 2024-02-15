import time
import os

from Scripts.utils import find_target_day

WDAY_LIST = (
    ("monday", "Понедельник"),
    ("tuesday", "Вторник"),
    ("wednesday", "Среда"),
    ("thursday", "Четверг"),
    ("friday", "Пятница"),
    ("saturday", "Суббота"),
    ("sunday", "Воскресенье"),
)

CURR_TIME = time.gmtime(int(os.getenv("LOCAL_GMT_CORRECTION")) + time.time())


def schedule_obj_2_str_week(obj):
    string = f"<b>Рассписание на неделю {obj.start_data.split(' ')[0]}</b>\n"
    for day in WDAY_LIST:
        string += f"\n<b>{day[1]} ({getattr(obj, day[0]).data}):</b>\n"
        k = 1
        classes = getattr(obj, day[0]).classes
        if not classes:
            string += f" Отдыхаем\n"
        for classe in classes:
            string += f"\n{k}. {classe.subject}. {classe.place} <i><b>{classe.start_time} - {classe.end_time}</b></i>\n"
            k += 1
    return string


def schedule_obj_2_str_day(obj):
    target_day, _ = find_target_day(obj)

    if not target_day:
        data = time.strftime("%d.%m.%Y", CURR_TIME)
        return f"<b>Расписание на сегодня {data}</b>\n Отдыхаем"
    else:
        data = target_day.data
    string = f"<b>Расписание на {data}</b>\n"
    if target_day and not (classes := target_day.classes):
        string += " Отдыхаем\n"
        return string
    k = 1
    for classe in classes:
        string += f"\n{k}. {classe.subject}. {classe.place} <i><b>{classe.start_time} - {classe.end_time}</b></i>\n"
        k += 1
    return string


def where_are_we_going_now(obj):
    target_day, is_it_next_day = find_target_day(obj)

    if is_it_next_day:
        first_classe = target_day.classes[0]
        return f"Первая пара завтра <b>{target_day.data}</b>:\n{first_classe.subject}. {first_classe.place} <i><b>{first_classe.start_time} - {first_classe.end_time}</b></i>\n"

    for classe in target_day.classes:
        if (
            CURR_TIME.tm_hour <= classe.end_time_hour
            and CURR_TIME.tm_min < classe.end_time_min
        ):
            return f"\n{classe.subject}. {classe.place} <i><b>{classe.start_time} - {classe.end_time}</b></i>\n"
    return "На сегодня все"

    # решить проблему с подгруппами
