import argparse

from sally.dataset import DataSet

__version__ = '0.1'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ML dataset management tool')
    parser.add_argument('--version', action='version', version=('%%(prog)s %s' % __version__), help='get version')
    parser.add_argument('install', default=False, type=bool, help='install ML dataset')
    args = parser.parse_args()

    if args.install:
        dataset = DataSet()
        dataset.download()
    else:
        parser.print_help()
