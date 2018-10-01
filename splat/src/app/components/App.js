import React, {Component} from 'react';

import {ScriptEditor} from './ScriptEditor';
import {CriteriaSheet} from "./CriteriaSheet";

const criteria = [
    {
        name: 'name',
        description: 'description',
        max: 10,
        score: 0,
        comment: '-'
    },
    {
        name: 'name',
        description: 'description',
        max: 10,
        score: 0,
        comment: '-'
    }
]

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {criteria: criteria};
    }

    onCriteriaUpdate(criteria) {
        this.setState({
            criteria: criteria
        })
    }

    updateScore(id, row, score) {
        var newState = {...this.state};
        newState[id] =
        this.setState({

        })
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <CriteriaSheet
                        criteria={this.state.criteria}
                        onUpdate={(criteria) => this.onCriteriaUpdate(criteria)}
                    />
                </div>
            </div>
        );
    }
}

export default App;

import {createStore} from "redux";

const reducer = (state, action) => {
    switch(action.type) {
        case "ADD":
            state = state + action.payload;
            break;
        case "SUBTRACT":
            break;
    }
    return state;
};
const store = createStore(reducer, 1);

store.dispatch({
    type: "ADD",
    payload: 10
});