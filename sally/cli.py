import argparse
from pprint import pprint

import inquirer
from inquirer import Text

from sally.dataset import DataSet
from sally.version import VERSION


def main():
    parser = argparse.ArgumentParser(description='ML dataset management tool')
    parser.add_argument('--version', action='version', version=('%%(prog)s %s' % VERSION), help='get version')
    parser.add_argument('install', nargs='*', help='install ML dataset')
    args = parser.parse_args()

    if args.install:
        questions = [
            inquirer.List('repository',
                message='what dataset type do you want?',
                choices=['caltech'],
            ),
        ]
        answers = inquirer.prompt(questions)

        dataset = DataSet(repository=answers['repository'])
        dataset.download()
    else:
        parser.print_help()
