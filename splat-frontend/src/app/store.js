import {createStore, combineReducers, applyMiddleware} from "redux";
import logger from "redux-logger";

//Reducers
import criteria from './reducers/criteriaReducer';
import script from './reducers/scriptReducer';


export default createStore(
    combineReducers({
        criteria,
        script
    }),
    {},
    applyMiddleware(logger)
)