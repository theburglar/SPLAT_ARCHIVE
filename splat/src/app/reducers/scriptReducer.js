const initialState = {
    code: "print('Hello World')",
    dynamicResults: "",
    staticResults: [ // to be configured later
        {
            measure: 'LOC',
            score: 1
        },
    ]
};

const scriptReducer = (state = initialState, action) => {
    return state;
};

export default scriptReducer;