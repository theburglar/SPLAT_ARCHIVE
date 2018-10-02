import React from 'react';

const rowStyle = {
    display: 'flex',
    padding: '1px'
}

const columnStyle = {
    padding: '5px',
}

export const CriteriaRow = (props) => {
    return (
        <div className="criteria-row" style={rowStyle}>
            <div className="criteria-name" style={columnStyle}>{props.name} </div>
            <div className="criteria-description" style={columnStyle}>{props.description}</div>
            <div className="criteria-max" style={columnStyle}>{props.max}</div>
            <div className="criteria-score" style={columnStyle}>
                <input
                    type="number"
                    step="0.25"
                    defaultValue={props.score}
                    onBlur={(e) => {props.onScoreChange(parseFloat(e.target.value))}}
                />
            </div>
            <div className="criteria-comment" style={columnStyle}>
                <input
                    defaultValue={props.comment}
                    onBlur={(e) => props.onCommentChange(e.target.value)}
                />
            </div>
        </div>
    )
};