"""

TODO:
    * add save to file
    * add uploading to FTP server

"""

from datetime import datetime

SEPARATOR = " | "


class Log:
    """ Static class to handle logging """

    debugging = False

    @staticmethod
    def write_line(tag, msg):
        print(Log.make_decorators(), tag + SEPARATOR + msg)

    @staticmethod
    def trace(tag, msg):
        print(Log.make_decorators(), "  Trace " + SEPARATOR + tag + SEPARATOR + msg)

    @staticmethod
    def debug(tag, msg):
        if Log.debugging:
            print(Log.make_decorators(), "  Debug " + SEPARATOR + tag + SEPARATOR + msg)

    @staticmethod
    def info(tag, msg):
        print(Log.make_decorators(), "  Info  " + SEPARATOR + tag + SEPARATOR + msg)

    @staticmethod
    def warn(tag, msg):
        print(Log.make_decorators(), "Warning!" + SEPARATOR + tag + SEPARATOR + msg)

    @staticmethod
    def error(tag, msg):
        print(Log.make_decorators(), " Error! " + SEPARATOR + tag + SEPARATOR + msg)

    @staticmethod
    def fatal(tag, msg):
        print(Log.make_decorators(), " Fatal! " + SEPARATOR + tag + SEPARATOR + msg)

    @staticmethod
    def make_decorators():
        return Log.get_current_datetime() + SEPARATOR

    @staticmethod
    def get_current_datetime():
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S:%f")
