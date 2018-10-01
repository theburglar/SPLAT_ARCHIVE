import React, {Component} from 'react';
import {CriteriaRow} from "./CriteriaRow";


export class CriteriaSheet extends Component {

    constructor(props){
        super(props);
        this.state = props.criteria;
    }

    render () {
        return (
            <div>
                {this.props.criteria.map(c =>
                    <CriteriaRow
                        key={c.name}
                        name={c.name}
                        description={c.description}
                        max={c.max}
                        score={c.score}
                        comment={c.comment}
                    />
                )}
            </div>
        )
    }
}