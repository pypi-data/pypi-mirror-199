import argparse
import logging

from cobolio import CopybookParser, CopybookTokenizer, parser
from cobolio.cli import print_banner, add_version


def copybook_to_layout(copybook):

    # convert copybook to dict format
    token = CopybookTokenizer.CopybookTokenizer(copybook)
    copybook_parser = CopybookParser.CopybookParser()
    copybook_parser_output = copybook_parser.copybook_parser(token)
    copybook_parser_dict = {'COPYBOOK': copybook_parser_output}

    return cobdata_to_csv.get_copybook_layout(copybook_parser_dict)


def cob_to_csv(input_copybook, input_datafile, output_datafile):

    # read copybook file
    with open(input_copybook, "r") as copybook_file:
        copybook_data = copybook_file.read()

    lrecl, layout = copybook_to_layout(copybook_data)

    with open(input_datafile, 'rb') as inputFile, open(output_datafile, 'w', newline='') as outputFile:
        cobdata_to_csv.convert_cobol_data_to_csv(inputFile, lrecl, layout, outputFile)


def cli_entry():
    cli_run(**vars(cli_parser().parse_args()))


def cli_run(**kwargs):
    print_banner('cob_to_csv', kwargs)

    if kwargs.get('debug'):
        logging.basicConfig(level=logging.DEBUG)

    if not kwargs.get('out-csv'):
        kwargs['out-csv'] = kwargs['in-data'] + '.csv'

    cob_to_csv(kwargs.get('in-copybook'), kwargs.get('in-data'), kwargs.get('out-csv'))


def cli_parser():
    parser = argparse.ArgumentParser(prog='cob_to_csv', description='COBOL file to csv')
    parser.add_argument('in-copybook')
    parser.add_argument('in-data')
    parser.add_argument('-o', '--out-csv')
    parser.add_argument('--debug', action='store_true')
    add_version(parser)

    return parser


if __name__ == '__main__':
    cli_entry()
