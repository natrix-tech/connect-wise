#!/usr/bin/env python3

"""
Company: Natrix Techonologies
Author: Nicolas Provencher

This script is used to generate a CSV file containing the phone number and company
name of each active company in ConnectWise. The CSV output file is specifically made
to be inputted into a 3CX phone system.
"""

import os
import sys
import argparse
import csv
import requests
from common import check_envs, get_header, LOGGER, ENVS

def main(filename):
    """
    Fetches all active companies and generates csv
    :param filename: output filename
    """
    LOGGER.info("Fetching companies...")
    LOGGER.info(filename)
    url = "https://api-na.myconnectwise.net/v4_6_release/apis/3.0/company/" \
          "companies?conditions=status/id=22&fields=name,phoneNumber&pageSize=1000"
    page = 1
    result = requests.get(url + "&page=" + str(page), headers=get_header())
    if result.status_code != 401:
        companies = []
        while result.json() != []:
            companies += result.json()
            page += 1
            result = requests.get(url + "&page=" + str(page), headers=get_header())
        create_csv(filename, companies)
    else:
        LOGGER.error("Provided credentials are incorrect")
        for var in ENVS:
            LOGGER.info("%s:%s", var, os.getenv(var))
        sys.exit(1)

def create_csv(filename, companies):
    """
    Generates csv file with the company name and phone number
    :param filename: output filename
    :param companies: array of active companies
    """
    LOGGER.info("Generating CSV file...")
    with open(filename, "w", newline='') as file:
        file_write = csv.writer(file, delimiter=",")
        file_write.writerow(["FirstName", "LastName", "Company", "Mobile",
                             "Mobile2", "Home", "Home2", "Business", "Business2",
                             "Email", "Other", "BusinessFax", "HomeFax", "Pager"])
        for item in companies:
            file_write.writerow(["", "", item["name"], "", "", "", "",
                                 item["phoneNumber"].strip('(').strip(')').strip('-'),
                                 "", "", "", "", "", ""])

def get_args():
    """
    Lists the program arguments
    :return: ouput filename
    """
    parser = argparse.ArgumentParser(description="This program queries Connect Wise and" \
                                                 " creates a csv file of all the active companies "
                                                 "in a format that the 3CX system can understand.")
    parser.add_argument("--output", "-o", help="Specify the output filename", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    try:
        check_envs()
        main(get_args())
    except KeyboardInterrupt:
        LOGGER.info("Exiting...")
        sys.exit(0)
