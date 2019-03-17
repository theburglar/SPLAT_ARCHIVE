const initialState = [
    {
        name: 'Criteria1',
        description: 'Description1',
        max: 10,
        score: 10,
        comment: 'Comment on criteria1'
    },
    {
        name: 'Criteria2',
        description: 'Description2',
        max: 10,
        score: 7,
        comment: 'Comment on criteria2'
    },
    {
        name: 'Criteria3',
        description: 'Description3',
        max: 10,
        score: 5,
        comment: 'Comment on criteria3'
    },
    {
        name: 'Criteria4',
        description: 'Description4',
        max: 10,
        score: 8,
        comment: 'Comment on criteria4'
    },
    {
        name: 'Criteria5',
        description: 'Description5',
        max: 10,
        score: 5,
        comment: 'Comment on criteria5'
    },
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