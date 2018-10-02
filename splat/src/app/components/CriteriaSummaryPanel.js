import React from 'react';

const totalMark = (criteria) => {
    return criteria.reduce((total, item) => {
        return total + item.score;
    }, 0);
}

export const CriteriaSummaryPanel = (props) => {
    return (
        <div className="criteria-summary-panel">
            <p>Total Mark: {totalMark(props.criteria)}</p>
        </div>
    )
}