from enum import Enum
from termcolor import colored, cprint

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    SUCCESS = 2
    WARN = 3
    ERROR = 4

def log(message, level=LogLevel.DEBUG):
    colored_message = make_log(message, level)
    print(colored_message)

def make_log(message, level=LogLevel.DEBUG):
    if level == LogLevel.DEBUG:
        return '%s: %s' % (colored('DEBUG', 'grey'), colored(message, 'white'))

    if level == LogLevel.SUCCESS:
        return '%s: %s' % (colored('SUCCESS', 'green'), colored(message, 'white'))

    if level == LogLevel.INFO:
        return '%s: %s' % (colored('INFO', 'blue'), colored(message, 'white'))

    if level == LogLevel.WARN:
        return '%s: %s' % (colored('WARN', 'magenta'), colored(message, 'white'))

    if level == LogLevel.ERROR:
        return '%s: %s' % (colored('ERROR', 'red'), colored(message, 'white'))
