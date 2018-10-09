import React from 'react';

const totalMark = (criteria) => {
    return criteria.reduce((total, item) => {
        return total + item.score;
    }, 0);
}

const totalScore = (criteria) => {
    return criteria.reduce((total, item) => {
        return total + item.max;
    }, 0);
}

export const CriteriaSummaryPanel = (props) => {
    return (
        <div className="criteria-summary-panel">
            <p>Total Mark: {totalMark(props.criteria)} / {totalScore(props.criteria)}</p>
        </div>
    )
}