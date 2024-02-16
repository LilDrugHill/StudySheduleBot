import os

import dotenv

from Scripts.requester import request_html_schedule, request_empty_schadle
from Scripts.html_handler import handle_target_schedule

dotenv.load_dotenv()
SCHEDULE_SOURCE = os.getenv("SCHEDULE_SOURCE")
MODE = os.getenv("MODE")


def main():
    empty_param_response = request_empty_schadle(SCHEDULE_SOURCE)

    target_schedule_obj, start_week_data = request_html_schedule(
        SCHEDULE_SOURCE, empty_param_response
    )

    schedule_list = handle_target_schedule(target_schedule_obj, start_week_data)

    return schedule_list


if __name__ == "__main__":
    main()
