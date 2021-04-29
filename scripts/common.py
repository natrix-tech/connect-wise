#!/usr/bin/env python3

"""
Company: Natrix Techonologies
Author: Nicolas Provencher

Common methods used for all scripts
"""

import sys
import os
import base64
import logging
import logging.config
import yaml

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.yaml"), 'r') as f:
    LOG_CFG = yaml.safe_load(f.read())
    f.close()
    logging.config.dictConfig(LOG_CFG)
    LOGGER = logging.getLogger()

ENVS = ["company", "publicKey", "privateKey", "clientId"]

def check_envs():
    """
    Ensures that all required environment variables are present
    """
    LOGGER.info("Checking environmentation variables...")
    for var in ENVS:
        if not os.getenv(var):
            LOGGER.error("Missing env: %s", var)
            sys.exit(1)

def get_header():
    """
    Generates a header object in the format that ConnectWise requires
    :return: header
    """
    return {
        "Authorization": "Basic " + str(base64.b64encode(bytes(os.getenv("company")
                                                               + "+" + os.getenv("publicKey")
                                                               + ":" + os.getenv("privateKey"),
                                                               'utf-8')))[2:-1],
        "clientID": os.getenv("clientId"),
        "Content-Type": "application/json"
    }
