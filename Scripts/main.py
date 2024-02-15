import os

import dotenv

from Scripts.requester import request_html_schedule, request_empty_schadle
from Scripts.html_handler import handle_target_schedule
from Scripts.convertors import schedule_obj_2_str_week, schedule_obj_2_str_day


dotenv.load_dotenv()
SCHEDULE_SOURCE = os.getenv("SCHEDULE_SOURCE")
MODE = os.getenv("MODE")


def main():
    empty_param_response = request_empty_schadle(SCHEDULE_SOURCE)

    with open("../templates/empty_schadle.html", "w") as f:
        f.write(empty_param_response.text)

    target_schedule_obj, start_week_data = request_html_schedule(
        SCHEDULE_SOURCE, empty_param_response
    )

    with open("../templates/tample_shedule.html", "w") as f:
        f.write(target_schedule_obj.text)

    schedule_list = handle_target_schedule(target_schedule_obj, start_week_data)

    return schedule_list


if __name__ == "__main__":
    main()
