import sys
#import time


def write_screen(typ: str, name: str, msg: str, encoding: str) -> None:
    """writing to the screen"""
    #timestring = '%s  ' % time.strftime('%H:%M:%S', time.localtime())
    # max length of 'INFO', 'DEBUG', 'WARNING', etc.
    #name = '%-8s' % (typ + ':')
    #filename_n = '%s:%s' % (filename, lineno)
    #msg2 = ' %-28s %s\n' % (filename_n, msg)

    #msg_all = (timestring + name + msg) if typ else timestring + msg
    #sys.stdout.write(msg_all)
    sys.stdout.write((name + msg) if typ else msg)
