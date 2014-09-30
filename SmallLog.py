
class SmallLog(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, log_name='output.db'):
        self._log_name = log_name

    def start_suite(self, name, attributes):
        print name, attributes

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


class SmallLogResult(object):

    def __init__(self, log_name='output.db'):
        self._log_name = log_name

    @property
    def suite(self):
        suite = lambda:0
        suite.name = 'Test'
        return suite


if __name__ == '__main__':
    from robot.api import ExecutionResult
    expected = ExecutionResult('output.xml')
    actual = SmallLogResult('output.db')
    assert expected.suite.name == actual.suite.name
