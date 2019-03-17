import React, {Component} from 'react';
import Editor from 'react-simple-code-editor';
import {highlight, languages} from 'prismjs';

import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-python';

// const code = ("def testy(x, y):\n" +
//     "  print('Hello World')");

const code = "{'encrypt': {'CC': 4,\n" +
    "             'Halstead': {'N1': 8,\n" +
    "                          'N2': 15,\n" +
    "                          'bugs': 0.02995282789966531,\n" +
    "                          'calculated_length': 47.77443751081735,\n" +
    "                          'difficulty': 1.875,\n" +
    "                          'effort': 168.48465693561735,\n" +
    "                          'h1': 3,\n" +
    "                          'h2': 12,\n" +
    "                          'length': 23,\n" +
    "                          'time': 9.360258718645408,\n" +
    "                          'vocabulary': 15,\n" +
    "                          'volume': 89.85848369899593},\n" +
    "             'Lines': {'blank': 2,\n" +
    "                       'comments': 0,\n" +
    "                       'lloc': 14,\n" +
    "                       'loc': 21,\n" +
    "                       'multi': 5,\n" +
    "                       'single_comment': 0,\n" +
    "                       'sloc': 14}}}\n" +
    "{'decrypt': {'CC': 1,\n" +
    "             'Halstead': {'N1': 1,\n" +
    "                          'N2': 1,\n" +
    "                          'bugs': 0.0006666666666666666,\n" +
    "                          'calculated_length': 0.0,\n" +
    "                          'difficulty': 0.5,\n" +
    "                          'effort': 1.0,\n" +
    "                          'h1': 1,\n" +
    "                          'h2': 1,\n" +
    "                          'length': 2,\n" +
    "                          'time': 0.05555555555555555,\n" +
    "                          'vocabulary': 2,\n" +
    "                          'volume': 2.0},\n" +
    "             'Lines': {'blank': 0,\n" +
    "                       'comments': 0,\n" +
    "                       'lloc': 2,\n" +
    "                       'loc': 6,\n" +
    "                       'multi': 4,\n" +
    "                       'single_comment': 0,\n" +
    "                       'sloc': 2}}}\n" +
    "{'find_encryption_offsets': {'CC': 7,\n" +
    "                             'Halstead': {'N1': 3,\n" +
    "                                          'N2': 5,\n" +
    "                                          'bugs': 0.008,\n" +
    "                                          'calculated_length': 16.36452797660028,\n" +
    "                                          'difficulty': 1.5,\n" +
    "                                          'effort': 36.0,\n" +
    "                                          'h1': 3,\n" +
    "                                          'h2': 5,\n" +
    "                                          'length': 8,\n" +
    "                                          'time': 2.0,\n" +
    "                                          'vocabulary': 8,\n" +
    "                                          'volume': 24.0},\n" +
    "                             'Lines': {'blank': 3,\n" +
    "                                       'comments': 2,\n" +
    "                                       'lloc': 22,\n" +
    "                                       'loc': 31,\n" +
    "                                       'multi': 4,\n" +
    "                                       'single_comment': 2,\n" +
    "                                       'sloc': 22}}}";

export class StaticAnalysis extends Component {

    state = {code};
    render() {
        return (
            <Editor
                value={this.state.code}
                onValueChange={code => this.setState({code})}
                highlight={code => highlight(code, languages.python)}
                padding={10}
                style={{
                    fontFamily: '"Fira code", "Fira Mono", monospace',
                    // fontSize: 32,
                }}
            />
        )
    }

}