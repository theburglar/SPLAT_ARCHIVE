from radon.visitors import ComplexityVisitor

from radon.complexity import sorted_results
from radon.complexity import LINES

from radon.raw import analyze

from radon.cli.harvest import CCHarvester
from radon.cli import Config

from radon.metrics import h_visit

import json
from pprint import pprint


def radon_test(f):
    filename = 'a1/a1_solution_' + f + '.py'
    with open(filename) as file:
        source = file.read()
        cv = ComplexityVisitor.from_code(source)
        res = sorted_results(cv.functions + cv.classes, order=LINES)
        output = {}
        for r in res:
            # print(f'Function: {r.name}, CC: {r.complexity}')
            output['CC'] = r.complexity

        res = analyze(source)
        # pprint(res)

        basic = {'loc': res[0],
                 'lloc': res[1],
                 'sloc': res[2],
                 'comments': res[3],
                 'multi': res[4],
                 'blank': res[5],
                 'single_comment': res[6]}
        output['Lines'] = basic

        config = Config(min='A',
                        max='F',
                        exclude=None,
                        ignore=None,
                        no_assert=False,
                        show_closures=False,
                        order=LINES)

        ch = CCHarvester([filename], config)
        res = ch.results
        x = json.loads(ch.as_json())
        # pprint(x)

        res = h_visit(source)

        hals = {'h1': res[0],
                'h2': res[1],
                'N1': res[2],
                'N2': res[3],
                'vocabulary': res[4],
                'length': res[5],
                'calculated_length': res[6],
                'volume': res[7],
                'difficulty': res[8],
                'effort': res[9],
                'time': res[10],
                'bugs': res[11]}

    output['Halstead'] = hals
    pprint({f: output})


if __name__ == '__main__':
    for f in ('encrypt', 'decrypt', 'find_encryption_offsets'):
        radon_test(f)
