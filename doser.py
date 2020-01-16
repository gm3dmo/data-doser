#!/usr/bin/env python3
"""
Template functions to generate test data.
"""

__author__ = "David Morris"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from logzero import logger
import string
import time
import xtemplate
import xs3
import xscarymaths


def do_a_chunk(args, chunk_number, duration, bag_o_random, values):
    logger.debug(f"""doing chunk: {chunk_number}""")
    file_number = 0
    for random_time in bag_o_random:
        if args.mode == 'random_delay':
            logger.debug(f"""Sleeping for {random_time}""")
            time.sleep(random_time)
        file_number += 1
        filename = f"""{args.prefix}-{chunk_number}-{file_number}.txt"""
        t  = xtemplate.get_template_from_file(args.template_file)
        new_record = xtemplate.process_template(t, values)
        logger.debug(new_record)
        xs3.push_to_s3(args.bucket, args.subfolder, new_record, filename)
        sn  = int(values['src_number'])
        sn += 1
        loc =  int(values['loc_11_number'])
        loc += 1
        values['src_number'] = sn
        values['loc_11_number'] = loc
        logger.debug(f"""completed file number: {filename}""")
    logger.debug(f"""completed chunk: {chunk_number}""")
    return values


def main(args):
    """ Main entry point of the app """
    duration = int(args.duration)
    chunks = int(args.chunks)
    number_of_files = int(args.numfiles)
    template_file = args.template_file
    #logger.debug(f"""duration: {duration} in {chunks} chunks """)
    values = xtemplate.get_initial_values()
    for chunk in range(chunks):
        #logger.debug(f"""chunk: {chunk:>4}""")
        c = xscarymaths.random_restricted_composition(duration, number_of_files, 1, duration) 
        bag_o_random = c
        do_a_chunk(args, chunk, duration, bag_o_random, values)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--duration", action="store", dest="duration", default=100)
    parser.add_argument("-c", "--chunks", action="store", dest="chunks", default=5)
    parser.add_argument("-f", "--numfiles", action="store", dest="numfiles", default=10)
    parser.add_argument("-t", "--template", action="store", dest="template_file", default='templates/template1.txt')
    parser.add_argument("-b", "--bucket", action="store", dest="bucket", default='s3monster')
    parser.add_argument("-s", "--subfolder", action="store", dest="subfolder", default='/')
    parser.add_argument("-m", "--mode", action="store", dest="mode", default='random_delay')
    parser.add_argument("-p", "--prefix", action="store", dest="prefix", default='MSG')
    args = parser.parse_args()
    main(args)

