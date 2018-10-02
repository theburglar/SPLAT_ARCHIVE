const initialState = [
    {
        name: 'Criteria1',
        description: 'description1',
        max: 10,
        score: 0,
        comment: '-'
    },
    {
        name: 'Criteria2',
        description: 'description2',
        max: 10,
        score: 0,
        comment: '-'
    },
    {
        name: 'Criteria3',
        description: 'description3',
        max: 10,
        score: 0,
        comment: '-'
    }
]

const criteriaReducer = (state = initialState, action) => {
    switch (action.type) {
        case "CRITERIA_EDIT_SCORE":
            state = state.map((item, index) => {
                if (index !== action.index) {
                    return item;
                }
                return {
                    ...item,
                    score: action.payload
                }
            });
            break;

        case "CRITERIA_EDIT_COMMENT":
            state = state.map((item, index) => {
                if (index !== action.index) {
                    return item;
                }
                return {
                    ...item,
                    comment: action.payload
                }
            });
            break;
    }
    return state;
};

export default criteriaReducer;