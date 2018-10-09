from pylint.lint import Run
from pylint.reporters.text import TextReporter

class WritableObject:

    def __init__(self):
        self._content = []

    def write(self, st):
        self._content.append(st)

    def read(self):
        return self._content


def run_pylint(filename='a1/a1_solution.py'):
    ARGS = []
    ARGS = ['--output-format=json']
    pylint_output = WritableObject()
    Run([filename] + ARGS, reporter=TextReporter(pylint_output), do_exit=False)

    # print(pylint_output.read())

    # for x in pylint_output.read():
    #     print(x, end='')

if __name__ == '__main__':
    run_pylint()
