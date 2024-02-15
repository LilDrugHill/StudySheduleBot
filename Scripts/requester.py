import os

import requests
import logging

from Scripts.utils import *
from Scripts.html_handler import asp_variables_parser, selected_param_parser

SCHEDULE_SOURCE = os.getenv("SCHEDULE_SOURCE")
MODE = os.getenv("MODE")


def request_html_schedule(source, response):

    asp_variables = asp_variables_parser(response)
    param_dict = selected_param_parser(response, default_selections=True)
    start_week_data, is_sunday = ddlWeek_creator(MODE)

    if is_sunday:
        data = {
            "__EVENTTARGET": "ddlWeek",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": asp_variables.VIEWSTATE,
            "__VIEWSTATEGENERATOR": asp_variables.VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": asp_variables.EVENTVALIDATION,
            "ddlFac": param_dict.default_param.ddlFac,
            "ddlDep": param_dict.default_param.ddlDep,
            "ddlCourse": param_dict.default_param.ddlCourse,
            "ddlGroup": param_dict.default_param.ddlGroup,
            "ddlWeek": start_week_data,
            "iframeheight": 400,
        }

        response = requests.request(
            "POST", source, data=data, cookies=still_cookies(response)
        )

        asp_variables = asp_variables_parser(response)
        param_dict = selected_param_parser(response, default_selections=True)

    if param_dict.target_param.ddlFac != param_dict.default_param.ddlFac:
        data = {
            "__EVENTTARGET": "ddlFac",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": asp_variables.VIEWSTATE,
            "__VIEWSTATEGENERATOR": asp_variables.VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": asp_variables.EVENTVALIDATION,
            "ddlFac": param_dict.target_param.ddlFac,
            "ddlDep": param_dict.default_param.ddlDep,
            "ddlCourse": param_dict.default_param.ddlCourse,
            "ddlGroup": param_dict.default_param.ddlGroup,
            "ddlWeek": start_week_data,
            "iframeheight": 400,
        }

        response = requests.request(
            "POST", source, data=data, cookies=still_cookies(response)
        )

        asp_variables = asp_variables_parser(response)
        param_dict = selected_param_parser(response, default_selections=True)

    if param_dict.target_param.ddlDep != param_dict.default_param.ddlDep:
        data = {
            "__EVENTTARGET": "ddlDep",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": asp_variables.VIEWSTATE,
            "__VIEWSTATEGENERATOR": asp_variables.VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": asp_variables.EVENTVALIDATION,
            "ddlFac": param_dict.default_param.ddlFac,
            "ddlDep": param_dict.target_param.ddlDep,
            "ddlCourse": param_dict.default_param.ddlCourse,
            "ddlGroup": param_dict.default_param.ddlGroup,
            "ddlWeek": start_week_data,
            "iframeheight": 400,
        }

        response = requests.request(
            "POST", source, data=data, cookies=still_cookies(response)
        )

        asp_variables = asp_variables_parser(response)
        param_dict = selected_param_parser(response, default_selections=True)

    if param_dict.target_param.ddlCourse != param_dict.default_param.ddlCourse:
        data = {
            "__EVENTTARGET": "ddlCourse",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": asp_variables.VIEWSTATE,
            "__VIEWSTATEGENERATOR": asp_variables.VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": asp_variables.EVENTVALIDATION,
            "ddlFac": param_dict.default_param.ddlFac,
            "ddlDep": param_dict.default_param.ddlDep,
            "ddlCourse": param_dict.target_param.ddlCourse,
            "ddlGroup": param_dict.default_param.ddlGroup,
            "ddlWeek": start_week_data,
            "iframeheight": 400,
        }

        response = requests.request(
            "POST", source, data=data, cookies=still_cookies(response)
        )

        asp_variables = asp_variables_parser(response)
        param_dict = selected_param_parser(response, default_selections=True)

    if param_dict.target_param.ddlGroup != param_dict.default_param.ddlGroup:
        data = {
            "__EVENTTARGET": "ddlGroup",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": asp_variables.VIEWSTATE,
            "__VIEWSTATEGENERATOR": asp_variables.VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": asp_variables.EVENTVALIDATION,
            "ddlFac": param_dict.default_param.ddlFac,
            "ddlDep": param_dict.default_param.ddlDep,
            "ddlCourse": param_dict.target_param.ddlCourse,
            "ddlGroup": param_dict.default_param.ddlGroup,
            "ddlWeek": start_week_data,
            "iframeheight": 400,
        }

        response = requests.request(
            "POST", source, data=data, cookies=still_cookies(response)
        )

        asp_variables = asp_variables_parser(response)
        param_dict = selected_param_parser(response, default_selections=True)

    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": asp_variables.VIEWSTATE,
        "__VIEWSTATEGENERATOR": asp_variables.VIEWSTATEGENERATOR,
        "__EVENTVALIDATION": asp_variables.EVENTVALIDATION,
        "ddlFac": param_dict.target_param.ddlFac,
        "ddlDep": param_dict.target_param.ddlDep,
        "ddlCourse": param_dict.target_param.ddlCourse,
        "ddlGroup": param_dict.target_param.ddlGroup,
        "ddlWeek": start_week_data,
        "ShowTT": "Показать",
        "iframeheight": 400,
    }

    response = requests.request(
        "POST", source, data=data, cookies=still_cookies(response)
    )
    print("ok")

    return response, start_week_data


def request_empty_schadle(source):
    response = requests.get(source)
    if response.status_code is not requests.codes.ok:
        print("Sworry")
        exit(0)
    else:
        print("Online")

    return response
