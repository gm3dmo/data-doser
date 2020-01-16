#!/usr/bin/env python3
"""
Template functions to generate test data.
"""

import boto3
from logzero import logger

__author__ = "David Morris"
__version__ = "0.1.0"
__license__ = "MIT"


def push_to_s3(bucket, subfolder, thing, thing_name):
    session = boto3.Session(profile_name='default')
    subfolder = '/'
    dev_s3_client = boto3.resource('s3')
    logger.debug(f"""s3 details: {bucket}, {subfolder}, {type(thing)}""")
    object = dev_s3_client.Object(bucket, thing_name)
    object.put(Body=thing)
    pass



if __name__ == "__main__":
    main()






