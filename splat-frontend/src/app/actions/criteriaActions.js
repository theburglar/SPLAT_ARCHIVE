export function setScore(score, index) {
    return {
        type: 'CRITERIA_EDIT_SCORE',
        payload: score,
        index: index
    }
}

export function setComment(comment, index) {
    return {
        type: 'CRITERIA_EDIT_COMMENT',
        payload: comment,
        index: index
    }
}