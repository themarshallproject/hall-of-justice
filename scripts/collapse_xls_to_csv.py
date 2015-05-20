#!/usr/bin/env python3

import os
import logging
import csv
import argparse
import xlrd

logger = logging.getLogger()


def main(args):
    infile_path = os.path.abspath(args.infile)

    if infile_path.endswith('.xls') or infile_path.endswith('.xlsx'):
        book = xlrd.open_workbook(infile_path)
        sheet_names = book.sheet_names()
        logger.info(", ".format(sheet_names))
    else:
        logger.error("Input file should be an Excel file ending with .xls or .xlsx")

    writer = csv.writer(args.outfile, quoting=csv.QUOTE_ALL) if args.outfile else None
    headers_written = False

    for name in sheet_names:
        sheet = book.sheet_by_name(name)
        if not headers_written:
            headerrow = sheet.row(0)
            headers = [h.value for h in headerrow]
            if writer:
                writer.writerow(headers)
            else:
                logger.info("Headers: {}".format("|".join(headers)))
            headers_written = True
        print("Processing: '{}'".format(name))
        for rowx in range(1, sheet.nrows):
            row = sheet.row(rowx)
            row_vals = [r.value for r in row]
            if writer:
                writer.writerow(row_vals)
            else:
                logger.info("|{}|".format("|".join(row_vals)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert an Excel file of sheets with uniform columns to a single CSV file')
    parser.add_argument('infile', type=str, help='Path to the Excel file to convert')
    parser.add_argument('outfile', type=argparse.FileType('w'))
    args = parser.parse_args()
    main(args)
