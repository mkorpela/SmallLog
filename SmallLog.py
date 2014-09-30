
class SmallLog(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, log_name='output.db'):
        self._log_name = log_name

    def start_suite(self, name, attributes):
        pass

    def end_suite(self, name, attributes):
        pass

    def start_test(self, name, attributes):
        pass

    def end_test(self, name, attributes):
        pass

    def start_keyword(self, name, attributes):
        pass

    def end_keyword(self, name, attributes):
        pass

    def log_message(self, message):
        pass

    def close(self):
        pass

