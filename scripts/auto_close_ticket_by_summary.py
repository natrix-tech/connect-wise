#!/usr/bin/env python3

"""
Company: Natrix Techonologies
Author: Nicolas Provencher

This script is used to automatically close recurring tickets which are
polluting your system. Simply specify the title and ticket type, and the script
will take care of the rest.
"""

import os
import sys
import argparse
import time
import json
import requests
from common import check_envs, get_header, LOGGER, ENVS

def main(args):
    """
    Continuously fetch Connect Wise for new tickets and updates the status
    :param args: passed arguments (ticket summary and ticket type)
    """
    summary = args.summary
    type_id = args.type
    while True:
        LOGGER.info("Checking for new tickets...")
        url_get = "https://api-na.myconnectwise.net/v4_6_release/apis/3.0/service/tickets" \
                "?conditions=summary=\"" + summary + "\"&pageSize=1000"
        result = requests.get(url_get, headers=get_header())
        if result.status_code != 401:
            url_update = "https://api-na.myconnectwise.net/v4_6_release/apis/3.0/service/tickets"
            for ticket in result.json():
                if ticket["status"]["id"] != 17:
                    ticket["status"]["id"] = 17
                    ticket["type"]["id"] = type_id
                    LOGGER.info("Updating: %s", ticket["id"])
                    update = requests.put(url_update + "/" + str(ticket["id"]),
                                          data=json.dumps(ticket), headers=get_header())
                    if update.status_code != 200:
                        LOGGER.error("Unable to update ticket (%s)", ticket["id"])
                        LOGGER.error(update.json())
            LOGGER.info("Sleeping for 20 seconds...")
            time.sleep(20)
        else:
            LOGGER.error("Provided credentials are incorrect")
            for var in ENVS:
                LOGGER.info(var + ": " + os.getenv(var))
            sys.exit(1)

def get_args():
    """
    Lists the program arguments
    :return: ouput filename
    """
    parser = argparse.ArgumentParser(description="This program continously queries Connect Wise "
                                                 "for new tickets matching the provided summary "
                                                 "and automatically closes them")
    parser.add_argument("--summary", "-s", help="Specify the ticket summary to verify",
                        required=True)
    parser.add_argument("--type", "-t", help="Specify the ticket type ID (ie. 417 for Generic)",
                        required=True)
    return parser.parse_args()

if __name__ == "__main__":
    try:
        check_envs()
        main(get_args())
    except KeyboardInterrupt:
        LOGGER.info("Exiting...")
        sys.exit(0)
