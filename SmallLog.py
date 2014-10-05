import os
import sqlite3
import sys


class SmallLog(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, log_name='output.db'):
        self.__connection = None
        self._log_name = log_name
        self._parents = []

    @property
    def _connection(self):
        if self.__connection is None:
            if os.path.exists(self._log_name):
                os.remove(self._log_name)
            self.__connection = sqlite3.connect(self._log_name)
            self._create_db_tables(self.__connection)
        return self.__connection

    def _create_db_tables(self, connection):
        connection.execute('CREATE TABLE suites(name)')
        connection.execute('CREATE TABLE tests(name)')
        connection.execute('CREATE TABLE keywords(name, parent)')
        connection.commit()

    def start_suite(self, name, attributes):
        self._connection.execute('INSERT INTO suites (name) VALUES (?)', [name])
        self._connection.commit()

    def end_suite(self, name, attributes):
        pass

    def start_test(self, name, attributes):
        self._connection.execute('INSERT INTO tests (name) VALUES (?)', [name])
        self._connection.commit()
        self._parents.append(name)

    def end_test(self, name, attributes):
        self._parents.pop()

    def start_keyword(self, name, attributes):
        self._connection.execute('INSERT INTO keywords (name, parent) VALUES (?, ?)', [name, self._parents[-1]])
        self._connection.commit()
        self._parents.append(name)

    def end_keyword(self, name, attributes):
        self._parents.pop()

    def log_message(self, message):
        pass

    def close(self):
        self._connection.close()


class SmallLogResult(object):

    def __init__(self, log_name='output.db'):
        self._log_name = log_name

    @property
    def suite(self):
        suite = lambda:0
        with sqlite3.connect(self._log_name) as c:
            suite.name = c.execute('SELECT name FROM suites').fetchone()[0]
            suite.tests = []
            for test in c.execute('SELECT name FROM tests').fetchall():
                t = lambda:0
                t.name = test[0]
                t.keywords = c.execute('SELECT name FROM keywords WHERE parent=?', [t.name]).fetchall()
                suite.tests.append(t)
        return suite


if __name__ == '__main__':
    from robot.api import ExecutionResult
    expected = ExecutionResult('output.xml')
    actual = SmallLogResult('output.db')
    assert expected.suite.name == actual.suite.name
    assert len(expected.suite.tests) == len(actual.suite.tests)
    assert len(expected.suite.tests[0].keywords) == len(actual.suite.tests[0].keywords)
