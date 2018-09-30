from radon.visitors import ComplexityVisitor

from radon.complexity import sorted_results
from radon.complexity import LINES

from radon.raw import analyze

from radon.cli.harvest import CCHarvester
from radon.cli import Config

import json
from pprint import pprint

def radon_test(filename='a1/a1.py'):

    with open(filename) as file:
        source = file.read()
        cv = ComplexityVisitor.from_code(source)
        res = sorted_results(cv.functions + cv.classes, order=LINES)
        for r in res:
            print(f'Function: {r.name}, CC: {r.complexity}')

        res = analyze(source)
        pprint(res)

        config = Config(min = 'A',
                        max = 'F',
                        exclude=None,
                        ignore=None,
                        no_assert=False,
                        show_closures=False,
                        order=LINES)

        ch = CCHarvester([filename], config)
        res = ch.results
        x = json.loads(ch.as_json())
        pprint(x)


if __name__ == '__main__':
    radon_test()
