import argparse

from sally.dataset import DataSet
from sally.version import VERSION


def main():
    parser = argparse.ArgumentParser(description='ML dataset management tool')
    parser.add_argument('--version', action='version', version=('%%(prog)s %s' % VERSION), help='get version')
    parser.add_argument('install', nargs='*', help='install ML dataset')
    args = parser.parse_args()

    if args.install:
        dataset = DataSet()
        dataset.download()
    else:
        parser.print_help()
