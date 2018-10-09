import React, {Component} from 'react';
import {connect} from 'react-redux';

import {TestResults} from './TestResults';
import {StaticAnalysis} from './StaticAnalysis';

import {ScriptEditor} from './ScriptEditor';
import CriteriaSheet from './CriteriaSheet';
import {CriteriaSummaryPane, CriteriaSummaryPanel} from '../components/CriteriaSummaryPanel';

class App extends Component {

    render() {
        return (
            <div style={{display: 'flex'}}>
                <div className="marking-panel" style={{padding: '10px', borderStyle: 'solid', borderWidth: '3px'}}>
                    <h3>Grading Criteria</h3>
                    <div className="criteria-sheet">
                        <CriteriaSheet/>
                    </div>
                    <div className="criteria-summary-panel">
                        <h3>Marking Summary</h3>
                        <CriteriaSummaryPanel criteria={this.props.criteria}/>
                        <button
                            onClick={() => {
                                console.log('SAVE')
                            }}>Save
                        </button>
                    </div>
                </div>

                <div className="script-panel" style={{padding: '10px', borderStyle: 'solid', borderWidth: '3px'}}>
                    <div><button>Script</button><button>Test Results</button></div>
                    {/*<h3>Script</h3>*/}
                    {/*<ScriptEditor/>*/}
                    {/*<h3>Marking Tests</h3>*/}
                    {/*<TestResults/>*/}
                    <h3>Static Analysis</h3>
                    <StaticAnalysis/>
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        criteria: state.criteria,
        script: state.script
    }
};

const mapDispatchToProps = (dispatch) => {
    return {};
}

export default connect(mapStateToProps, mapDispatchToProps)(App);