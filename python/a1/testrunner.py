__author__ = 'Steven Summers'
__version__ = ''

import argparse
import difflib
import importlib.util
import inspect
import io
import json
import re
import sys
import textwrap
import threading
import traceback
import time
import unittest

from bdb import Bdb
from collections import OrderedDict
from enum import Enum, unique
from functools import wraps
from types import FunctionType, ModuleType, TracebackType
from typing import Callable, Dict, List, Tuple, Type, Union, Optional


# GLOBALS TO EXCLUDE FILES IN TRACEBACK
__TEST_RUNNER = True
setattr(threading, '__TEST_RUNNER', True)  # Don't like this but otherwise regex

__all__ = ['OrderedTestCase', 'RedirectStdIO', 'TestCase', 'TestMaster',
           'skipIfFailed', 'timeout']

# DEFAULTS
DEFAULT_MAXDIFF = None
DEFAULT_TIMEOUT = 0
# DEFAULT_MIN_PY_VERSION = (3, 6, 0)

# CONSTANTS
DIFF_OMITTED = '\nDiff is {} characters long. Set TestMaster(max_diff=None) to see it.'
DUPLICATE_MSG = 'AS ABOVE'
TAB_SIZE = 4
BLOCK_WIDTH = 80
BLOCK_TEMPLATE = """\
/{0}\\
|{{:^{1}}}|
\\{0}/\
""".format(''.center(BLOCK_WIDTH - 2, '-'), BLOCK_WIDTH - 2)


def skipIfFailed(test_case: Type[unittest.TestCase] = None, test_name: str = None, tag: str = None):  # pylint: disable=C0103
    """
    skipIfFail decorator allows you to skip entire TestCases or specific test cases
    if not all tests pass for a TestCase, or if a specifc test case fails.
    At least one test method of TestCase1 needs to fail to skip
    @skipIfFailed(TestCase1)
    Skip if 'test_method' of TestCase1 failed
    @skipIfFailed(TestCase1, 'test_method')
    Skip if 'test_method' failed
    Can only be applied to method with class class containing a method named 'test_method'
    @skipIfFailed(test_name='test_method')
    """
    if test_case is None and test_name is None:
        raise RuntimeError("test_case and test_name for skipIfFailed can't both be None")

    if test_case is not None and test_name is not None and not hasattr(test_case, test_name):
        raise AttributeError('{0} has no method {1}'.format(
            test_case.__name__, test_name))

    if tag is not None and test_name is None:
        raise RuntimeError("test_name must be specified if tag is provided for skipIfFailed")

    def decorator(obj: Union[Type[TestCase], Callable]):
        if hasattr(obj, '__skip_test__'):
            obj.__skip_test__.append((test_case, test_name, tag))
        else:
            obj.__skip_test__ = [(test_case, test_name, tag)]
        if not isinstance(obj, FunctionType):
            return obj

        @wraps(obj)
        def wrapper(*args, **kwargs):
            return obj(*args, **kwargs)
        return wrapper
    return decorator


def import_module(name: str, path: str) -> \
        Tuple[Optional[ModuleType], Optional[Tuple[Type, Exception, TracebackType]]]:
    """
    Dynamically import the Python file (.py) at 'path' the
    __name__ attribute will be set to 'name'
    """
    spec = importlib.util.spec_from_file_location(name, path)
    if not name:
        raise ValueError("'name' can not be empty")
    if spec is None:
        raise ValueError(f'The path {path} is invalid. It should be a Python (.py) file path.')
    module = importlib.util.module_from_spec(spec)
    with RedirectStdIO(stdin=True, stdout=True) as stdio:
        try:
            spec.loader.exec_module(module)
            setattr(module, '__TEST_RUNNER_CLEAN_IMPORT', stdio.stdout == '')
            return module, None
        except Exception:  # pylint: disable=W0703
            return None, sys.exc_info()


def _timeout_wrapper(test_func):
    """
    Runs the test function in a killable thread, the seconds value
    is obtained from the __timeout__ attribute which can be set globally
    using TestMaster(timeout=value) or apply to specific classes or functions
    using the timeout decorator, if seconds <= 0 the test is not threaded.
    """
    @wraps(test_func)
    def thread_wrapper(self):
        secs = getattr(test_func, '__timeout__', 0) or \
            getattr(self.__class__, '__timeout__', 0) or \
            _TimeoutThread.timeout

        if secs <= 0:
            return test_func(self)

        try:
            thread = _TimeoutThread(target=test_func, args=(self,))
            threading.settrace(thread.global_trace)
            thread.start()
            thread.join(secs)
            alive = thread.isAlive()
            thread.kill()
        finally:
            threading.settrace(None)

        if thread.exc_info is not None:
            raise thread.exc_info[1].with_traceback(thread.exc_info[2])

        if alive:
            # raise TimeoutError(f'Function ran longer than {secs} second(s)')
            raise unittest.SkipTest(f'Function ran longer than {secs} second(s)')
        return None
    return thread_wrapper


def timeout(seconds: float = 0):
    """ Decorator to apply __timeout__ atrribute to a test method or TestCase """
    def timeout_decorator(test_obj):
        test_obj.__timeout__ = seconds
        return test_obj
    return timeout_decorator


@unique
class TestOutcome(Enum):
    SUCCESS = '+'
    FAIL = '-'
    SKIP = '?'


class CachedIO(io.StringIO):
    """ Writes all read values and write values to stream """

    def __init__(self, stream):
        super().__init__()
        self._stream = stream

    def set_value(self, string):
        """ Set value to self without writing to stream """
        super().write(string)
        self.seek(0)

    def write(self, s: str):
        res = super().write(s)
        self._stream.write(s)
        return res

    def readline(self, size: int = None):
        res = super().readline(size)
        self._stream.write(res)
        return res


class RedirectStdIO:
    """
    Context manager to send stdin input and capture stdout and stderr
    Usage:
        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            stdio.set_stdin('World!\n')
            inp = input('Hello')
        stdio.stdout == 'Hello'
        inp == 'World'
    """

    def __init__(self, stdin: bool = False, stdout: bool = False,
                 stderr: bool = False, stdinout: bool = False):
        self._sys_stdin = sys.stdin
        self._sys_stdout = sys.stdout
        self._sys_stderr = sys.stderr

        if stdinout:
            self._stdinout_stream = io.StringIO()
            self._stdin_stream = CachedIO(self._stdinout_stream)
            self._stdout_stream = CachedIO(self._stdinout_stream)

        else:
            self._stdin_stream = io.StringIO() if stdin else None
            self._stdout_stream = io.StringIO() if stdout else None
            self._stdinout_stream = None

        self._stderr_stream = io.StringIO() if stderr else None

    def __enter__(self):
        if self._stdin_stream is not None:
            sys.stdin = self._stdin_stream

        if self._stdout_stream is not None:
            sys.stdout = self._stdout_stream

        if self._stderr_stream is not None:
            sys.stderr = self._stderr_stream

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdin = self._sys_stdin
        sys.stdout = self._sys_stdout
        sys.stderr = self._sys_stderr

    @staticmethod
    def _read_stream(stream: io.StringIO) -> str:
        if stream is None:
            raise RuntimeError(
                'Attempt to read from a stream that has not been enabled')
        return stream.getvalue()

    def set_stdin(self, string: str):
        if self._stdin_stream is None:
            raise RuntimeError(
                f'stdin has not been set in {self.__class__.__name__}.__init__')

        if self._stdinout_stream is None:
            self._stdin_stream.write(string)
            self._stdin_stream.seek(0)
        else:
            self._stdin_stream.set_value(string)

    @property
    def stdinout(self):
        return self._read_stream(self._stdinout_stream)

    @property
    def stdout(self) -> str:
        return self._read_stream(self._stdout_stream)

    @property
    def stderr(self) -> str:
        return self._read_stream(self._stderr_stream)


class RecursionDetector(Bdb):
    def do_clear(self, arg):
        pass

    def __init__(self, *args):
        super().__init__(*args)
        self.stack = set()

    def user_call(self, frame, argument_list):
        code = frame.f_code
        if code in self.stack:
            raise RecursionError
        self.stack.add(code)

    def user_return(self, frame, return_value):
        self.stack.remove(frame.f_code)


class TestLoader(unittest.TestLoader):
    """ Custom loader class to specify TestCase case order """

    def getTestCaseNames(self, testCaseClass: Type[unittest.TestCase]):
        """
        Override for unittest.TestLoad.getTestCaseNames
        Return a sorted sequence of method names found within testCaseClass
        """
        if issubclass(testCaseClass, OrderedTestCase):
            return testCaseClass.member_names
        return super().getTestCaseNames(testCaseClass)

    def loadTestCases(self, test_cases) -> unittest.TestSuite:  # pylint: disable=C0103
        """
        Params:
            test_cases List[Union[unittest.TestCase, Type[unittest.TestCase]]]
        """
        suite = unittest.TestSuite()

        for test_case in test_cases:
            if isinstance(test_case, unittest.TestCase):
                suite.addTest(test_case)
            else:
                suite.addTests(self.loadTestsFromTestCase(test_case))
        return suite


class _TestCaseMeta(type):
    """
    MetaClass to decorate all test methods with _timeout_wrapper and
    track test method definition order.
    """
    def __new__(cls, name, bases, classdict):
        member_names = []
        for key, value in classdict.items():
            if key.startswith(TestLoader.testMethodPrefix) and callable(value):
                member_names.append(key)
                classdict[key] = _timeout_wrapper(value)

        result = super().__new__(cls, name, bases, classdict)
        result.member_names = member_names
        return result

    def __getattr__(cls, item):
        if item not in cls._modules:
            raise AttributeError(f"type object '{cls.__name__}'' has no attribute '{item}'")
        return cls._modules[item]


class _TimeoutThread(threading.Thread):
    """
    Killable thread using a global debug tracing function set with threading.settrace
    """
    timeout = DEFAULT_TIMEOUT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.killed = False
        self.exc_info = None

    def run(self):
        """
        Set the trace function and run the thread catching and storing
        any exceptions that occur.
        """
        try:
            super().run()
        except Exception:  # pylint: disable=W0703
            self.exc_info = sys.exc_info()

    def kill(self):
        self.killed = True

    def global_trace(self, _frame, event, _arg):
        """ Global trace function for threading.settrace which retuns a local trace function """
        if event == 'call':
            return self.local_trace
        return None

    def local_trace(self, _frame, event, _arg):
        """
        Local trace function which kills the thread should it still be running and
        and the 'killed' attribute is set to True.
        """
        if self.killed:
            if event == 'line':
                raise SystemExit
        return self.local_trace


class TestCase(unittest.TestCase, metaclass=_TestCaseMeta):
    """
    Extends the unittest.TestCase defining additional assert methods.
    """
    # pylint: disable=C0103
    member_names: List[str]
    _modules: Dict[str, ModuleType] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aggregate_failures = []

    def __getattr__(self, item):
        if item not in self._modules:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
        return self._modules[item]

    @classmethod
    def register_module(cls, name: str, module: ModuleType):
        cls._modules[name] = module

    def assertMultiLineEqual(self, first, second, msg=None, strip=False):  # pylint: disable=W0221
        """
        unittest.TestCase.assertMultiLineEqual with strip keyword arg,
        if True then string is split on newlines with leading and trailing
        whitespace striped and rejoined before
        """
        if strip:
            first = '\n'.join(s.strip() for s in first.splitlines())
            second = '\n'.join(s.strip() for s in second.splitlines())

        super().assertMultiLineEqual(first, second, msg=msg)

    def assertDefined(self, obj: Union[ModuleType, Type], name: str):
        self.assertIs(hasattr(obj, name), True,
                      msg=("'{}' is not defined correctly, "
                           "check spelling and number of parameters".format(name)))

    def assertFunctionDefined(self, obj: Union[ModuleType, Type], function_name: str, params: int):
        self.assertDefined(obj, function_name)
        func = getattr(obj, function_name)
        self.assertIs(inspect.isfunction(func), True,
                      msg=f"{function_name} should be a function")
        sig = inspect.signature(func)
        self.assertEqual(len(sig.parameters), params,
                         msg=("'{}' does not have the correct number of parameters, expected"
                              " {} found {}".format(function_name, params, len(sig.parameters))))

    def guess_function_name(self, obj: Union[ModuleType, Type], function_name: str):
        attrs = dict(inspect.getmembers(obj, predicate=inspect.isfunction))
        if function_name in attrs:
            return function_name

        matches = difflib.get_close_matches(function_name, attrs, n=1)
        if not matches:
            self.fail(msg=f'Found no close match for {function_name}')

        return matches[0]

    def assertClassDefined(self, module: ModuleType, class_name: str):
        self.assertDefined(module, class_name)
        class_ = getattr(module, class_name)
        self.assertIs(inspect.isclass(class_), True,
                      msg=f"{class_name} should be a class")

    def assertIsSubclass(self, sub_class: Type, parent_class: Type):
        self.assertIs(issubclass(sub_class, parent_class), True,
                      msg="'{}' is not a subclass of '{}'".format(sub_class, parent_class))

    def assertDocString(self, obj: Union[Type, Callable], name: str = None):
        if name is not None:
            self.assertDefined(obj, name)
            obj = getattr(obj, name)

        doc = inspect.getdoc(obj)
        msg = "Documentation string is required for '{}'".format(
            obj.__qualname__)
        self.assertIsNotNone(doc, msg=msg)
        self.assertNotEqual(doc, '', msg=msg)

    def assertIsNotRecursive(self, func):
        detector = RecursionDetector()
        detector.set_trace()
        not_recursive = True
        try:
            func()
        except RecursionError:
            not_recursive = False
        finally:
            sys.settrace(None)

        self.assertIs(not_recursive, True, msg="function is recursive")

    def aggregate(self, test_func, *args, tag: str = None, **kwargs):
        try:
            test_func(*args, **kwargs)
        except self.failureException as failure:
            self.aggregate_failures.append((failure, tag))

    def aggregate_tests(self):
        """
        Must be called when done with the AggregateTestCase to propogate
        the failures. This is not in __exit__ due to hiding relevant traceback
        levels the exception message ends up pointing to the last line.
        """
        msg = ''
        for error, _, in self.aggregate_failures:
            msg += '\n' + textwrap.indent(str(error), ' ' * TAB_SIZE)

        if msg:
            self.fail(msg=msg)

    def _truncateMessage(self, message, diff):
        """ override unittest.TestCase._truncateMessage to use our DIFF_OMITTED message """
        max_diff = self.maxDiff
        if max_diff is None or len(diff) <= max_diff:
            return message + diff
        return message + DIFF_OMITTED.format(len(diff))

    @property
    def name(self) -> str:
        return self._testMethodName

    @property
    def description(self) -> str:
        short_desc = self.shortDescription()
        return short_desc if short_desc else self.name


class OrderedTestCase(TestCase):
    """ TestCase with the description property reflecting the test number """
    @property
    def description(self):
        return '{}. {}'.format(self.member_names.index(self.name) + 1,
                               super().description)


class TestResult(unittest.TestResult):
    """
    TestResult stores the result of each test in the order they were executed
    """

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self._start = 0
        self._stop = 0
        # TestCaseClassName  TestCaseName
        # Dict[str, Dict[str, Tuple[TestCase, TestOutcome]]
        self.results = OrderedDict()

    def startTestRun(self):
        self._start = time.time()
        super().startTestRun()

    def stopTestRun(self):
        self._stop = time.time()
        super().stopTestRun()

    @property
    def run_time(self):
        return self._stop - self._start

    def startTest(self, test: TestCase):
        test_cls_name = test.__class__.__name__
        if test_cls_name not in self.results:
            self.results[test_cls_name] = OrderedDict()

        test_method = getattr(test.__class__, test.name)
        self._apply_skip(test, test.__class__)
        self._apply_skip(test, test_method)

        super().startTest(test)

    def _apply_skip(self, test: TestCase, test_item: Union[Type[TestCase], FunctionType]):
        """
        Applies the unittest attributes used for skipping tests if the __skip_test__
        attribute has been applied to either the test class or method using the
        skipIfFailed decorator.
        """
        skip_test = getattr(test_item, '__skip_test__', None)
        if skip_test is None:
            return

        for test_cls, test_name, tag in skip_test:
            if test_cls is None:
                test_cls = test.__class__
                if not hasattr(test_cls, test_name):
                    raise AttributeError('{0} has no method {1}'.format(
                        test_cls.__name__, test_name))

            test_cls_name = test_cls.__name__

            if test_cls_name not in self.results:
                raise RuntimeError("Can't check to skip {}.{} if {} hasn't run".format(
                    test.__class__.__name__, test.name, test_cls_name))

            test_results = self.results[test_cls_name]
            if test_name is not None and test_name not in test_results:
                raise RuntimeError("Can't check to skip {}.{} if {}.{} hasn't run".format(
                    test.__class__.__name__, test.name, test_cls_name, test_name))

            if test_name is not None:
                test_case, outcome = test_results[test_name]
                if outcome != TestOutcome.SUCCESS and \
                    (tag is None
                     or (tag is not None
                         and any(tag == t for _, t in test_case.aggregate_failures))):
                    # set attributes unittest looks for if a test is marked to skip
                    test_item.__unittest_skip__ = True
                    tag_msg = f" with tag '{tag}'" if tag is not None else ''
                    test_item.__unittest_skip_why__ = 'Skipped due to failing {}.{}{}'.format(
                        test_cls_name, test_name, tag_msg)
                    break

            elif test_name is None and any(tup[1] != TestOutcome.SUCCESS
                                           for tup in test_results.values()):
                test_item.__unittest_skip__ = True
                test_item.__unittest_skip_why__ = 'Skipped due to failing a test from {}'.format(
                    test_cls_name)
                break
        # delete custom attribute since __unittest_skip__ has been applied
        del test_item.__skip_test__

    def addSubTest(self, test, subtest, err):
        raise NotImplementedError("TODO")

    def add_outcome(self, test: TestCase, outcome: TestOutcome):
        self.results[test.__class__.__name__][test.name] = (test, outcome)

    def addSuccess(self, test: TestCase):
        self.add_outcome(test, TestOutcome.SUCCESS)
        super().addSuccess(test)

    def addFailure(self, test: TestCase, err: Tuple[Type, Exception, TracebackType]):
        self.add_outcome(test, TestOutcome.FAIL)
        super().addFailure(test, err)

    def addError(self, test: TestCase, err: Tuple[Type, Exception, TracebackType]):
        self.add_outcome(test, TestOutcome.FAIL)
        super().addError(test, err)

    def addSkip(self, test: TestCase, reason: str):
        self.add_outcome(test, TestOutcome.SKIP)
        super().addSkip(test, reason)

    def _is_relevant_tb_level(self, tb):
        """
        Override which is used with unittest.TestResult._exc_info_to_string
        to determine what levels of a traceback to skip when formatting the error.
        """
        return '__TEST_RUNNER' in tb.tb_frame.f_globals or \
            super()._is_relevant_tb_level(tb)

    def to_dict(self):
        return {
            test_cls:
                {name: outcome.value for name, (test, outcome) in res.items()}
            for test_cls, res in self.results.items()
        }


class TestMaster:
    """
    Core driving class which creates the TestSuite from the provided TestCases
    """
    separator1 = '=' * BLOCK_WIDTH
    separator2 = '-' * BLOCK_WIDTH
    indent = ' ' * TAB_SIZE
    _remove_path = re.compile(r'File ".*[\\/]([^\\/]+.py)"')
    # _remove_threading = re.compile(
    #     r'(^\s*File \".*threading.py\".+?(?=\s*File \"))', flags=re.DOTALL | re.MULTILINE)
    _remove_importlib = re.compile(
        r'(^\s*File \".*importlib.*\".+?(?=\s{2}File \"))', flags=re.DOTALL | re.MULTILINE)

    # pylint: disable=R0913
    def __init__(self,
                 max_diff: int = DEFAULT_MAXDIFF,
                 suppress_stdout: bool = True,
                 timeout: int = DEFAULT_TIMEOUT,  # pylint: disable=W0621
                 output_json: bool = False,
                 hide_paths: bool = True,
                 scripts: List[Tuple[str, str]] = None,
                 stop_on_import_fail: bool = True):
        """
        Parameters:
            max_diff: This attribute controls the maximum length of diffs output
                by assert methods that report diffs on failure. Set to None for no max
            suppress_stdout: Controls if all output when running tests should be suppressed
            timeout: global timeout value in seconds, if a timeout > 0 is specified then
                the tests are run in killable threads.
            output_json: outputs a text summary if True else json from the result.
            hide_paths: if True file paths in tracebacks for failures are removed to
                only contain the filename.
            scripts: list of tuples, these tuples are a pair of module name and module path
                that gets imported using 'path' with the __name__ attribute of the module set to
                'name'. On successfull import a __TEST_RUNNER_CLEAN_IMPORT attribute is set on the
                module True if nothing was output to stdout otherwise False.
        """

        parser = argparse.ArgumentParser()

        parser.add_argument("-j", "--json",
                            help="Whether or not to display output in JSON format.",
                            action='store_true',
                            default=output_json)
        parser.add_argument("-d", "--diff",
                            help="The maximum number of characters in a diff",
                            action="store",
                            type=int,
                            default=max_diff)
        parser.add_argument('-p', '--paths', nargs="+")
        parser.add_argument('-s', '--scripts', nargs="+")
        parser.add_argument("--tb-hide-paths",
                            help="Hide paths from traceback output.",
                            action="store_true",
                            default=hide_paths)
        parser.add_argument("--tb-no-duplicates",
                            help="Remove duplicates from test output.",
                            action="store_true",
                            default=True)
        parser.add_argument("--stop-on-import-fail",
                            help="Remove duplicates from test output.",
                            action="store_true",
                            default=stop_on_import_fail)

        args = parser.parse_args()

        self.result = None
        self._output_json = args.json
        self._no_dups = args.tb_no_duplicates
        self._hide_paths = args.tb_hide_paths
        self._suppress_stdout = suppress_stdout
        self._stop_on_import_fail = args.stop_on_import_fail

        TestCase.maxDiff = None if not args.diff or args.diff < 0 else args.diff
        _TimeoutThread.timeout = timeout

        if args.scripts or args.paths:
            if len(args.scripts or ()) != len(args.paths or ()):
                parser.error("must have equal number of values for 'imports' and 'paths'")
            scripts = zip(args.scripts, args.paths)

        self._import_errors = []

        for name, path in (scripts or ()):
            name = name.strip()
            module, error = import_module(name, path)
            TestCase.register_module(name, module)
            if error:
                self._import_errors.append(self.format_error(name, error))
                if self._stop_on_import_fail:
                    break

    @staticmethod
    def _add_flavour(flavour: str, test_results: List[Tuple[TestCase, str]]):
        return [(flavour, test, msg) for test, msg in test_results]

    def print_results(self, all_tests: List[TestCase], result: TestResult):
        # Join the lists sorted by the test order
        failed_tests = sorted(
            self._add_flavour('FAIL', result.failures) +
            self._add_flavour('ERROR', result.errors) +
            self._add_flavour('SKIP', result.skipped),
            key=lambda t: all_tests.index(t[1]))

        # print summary
        print(BLOCK_TEMPLATE.format('Summary of Results'))
        for test_cls, test_cases in result.results.items():
            print(test_cls)
            for _test_name, (test, outcome) in test_cases.items():
                print(f'{self.indent}{outcome.value} {test.description}')

        # failed imports
        if self._import_errors:
            print(self.separator2)
            print(BLOCK_TEMPLATE.format('Failed Imports'))
            for name, exc_info in self._import_errors:
                print(self.separator1)
                _, msg, err_msg = self.format_error(name, exc_info)
                print(f'Reason: {msg}')
                print(self.separator2)
                print(textwrap.indent(err_msg, self.indent))

        # print fails
        if failed_tests:
            print(self.separator2)
            print(BLOCK_TEMPLATE.format('Failed Tests'))
            prev = None
            for flavour, test, msg in failed_tests:
                if self._no_dups:
                    self.print_error(flavour, test, DUPLICATE_MSG if msg == prev else msg.strip())
                    prev = msg
                else:
                    self.print_error(flavour, test, msg.strip())

    def print_error(self, flavour: str, test: TestCase, msg: str):
        print(self.separator1)
        print(f'{flavour}: {test.__class__.__name__} {test.description}')
        print(self.separator2)
        if self._hide_paths:
            msg = self._remove_path.sub(r'File "\1"', msg)
        # msg = self._remove_threading.sub('', msg)
        print(textwrap.indent(msg, self.indent))
        print()

    def format_error(self, name: str, exc_info) -> Tuple[str, str]:
        exc_type, exc_value, exc_traceback = exc_info
        if exc_type is ImportError:
            msg = f"Tests not run due to {name} file not found"
            err_type = 'import'
        elif exc_type is SyntaxError:
            msg = "Tests not run due to syntax error"
            err_type = 'syntax'
        elif exc_type is EOFError:
            msg = "Tests not run due to unexpectedly waiting for input"
            err_type = 'eof'
        else:
            msg = "Tests not run due to arbitrary exception"
            err_type = 'exception'

        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        err_msg = self._remove_importlib.sub('', err_msg)
        if self._hide_paths:
            err_msg = self._remove_path.sub(r'File "\1"', err_msg)

        return err_type, msg, err_msg

    def run(self, test_cases: List[Union[TestCase, Type[TestCase]]]) -> TestResult:

        if self._stop_on_import_fail and self._import_errors:
            err_type, msg, err_msg = self._import_errors[0]
            if self._output_json:
                data = dict(error=err_type, error_message=f'{msg}\n{err_msg}')
                json.dump(data, sys.stdout, indent=4)
            else:
                print(BLOCK_TEMPLATE.format(msg))
                print(err_msg)

            sys.stdout.flush()
            return None

        suite = TestLoader().loadTestCases(test_cases)
        all_tests = list(suite)

        # hide unittest output
        with RedirectStdIO(stdout=self._suppress_stdout, stderr=True):
            runner = unittest.TextTestRunner(stream=None,
                                             verbosity=0,
                                             resultclass=TestResult)
            result = runner.run(suite)

        runtime = result.run_time
        total = result.testsRun
        fails, skips = len(result.failures) + len(result.errors), len(result.skipped)
        passed = total - fails - skips

        if self._output_json:
            errors = []
            for name, exc_info in self._import_errors:
                err_type, msg, err_msg = self.format_error(name, exc_info)
                errors.append(dict(error=err_type, error_message=f'{msg}\n{err_msg}'))
            data = dict(total=total, failed=fails, skipped=skips, passed=passed,
                        time=runtime, results=result.to_dict(), errors=errors)
            json.dump(data, sys.stdout, indent=4)
        else:
            self.print_results(all_tests, result)
            print(self.separator2)
            print(f'Ran {total} tests in {runtime:.3f} seconds with '
                  f'{passed} passed/{skips} skipped/{fails} failed.')

        sys.stdout.flush()

        return result