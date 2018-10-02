import React, {Component} from 'react';
import Editor from 'react-simple-code-editor';
import {highlight, languages} from 'prismjs';

import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-python';

const code = ("def testy(x, y):\n" +
    "  print('Hello World')");

export class ScriptEditor extends Component {

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
                    fontSize: 12,
                }}
            />
        )
    }

}