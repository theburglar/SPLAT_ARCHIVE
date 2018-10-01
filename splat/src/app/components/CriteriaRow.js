import React, {Component} from 'react';

export const CriteriaRow = (props) => {
    return (
        <div className="criteria-row">
            <div className="criteria-name">{props.name}</div>
            <div className="criteria-description">{props.description}</div>
            <div className="criteria-max">{props.max}</div>
            <div className="criteria-score">
                <input defaultValue={props.value}/>
            </div>
            <div className="criteria-comment">
                <input defaultValue={props.comment}/>
            </div>
        </div>
    )
}
