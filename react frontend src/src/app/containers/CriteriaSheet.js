import React, {Component} from 'react';
import {CriteriaRow} from '../components/CriteriaRow';
import {connect} from 'react-redux';

import {setScore, setComment} from '../actions/criteriaActions'

class CriteriaSheet extends Component {
    render() {
        return (
            <div className="criteria-sheet">
                <div>
                    {this.props.criteria.map((c, index) =>
                        <CriteriaRow
                            key={index}
                            name={c.name}
                            description={c.description}
                            max={c.max}
                            score={c.score}
                            comment={c.comment}
                            onScoreChange={(score) => this.props.setScore(score, index)}
                            onCommentChange={(com) => this.props.setComment(com, index)}
                        />
                    )}
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        criteria: state.criteria
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        setScore: (score, index) => {
            dispatch(setScore(score, index))
        },
        setComment: (comment, index) => {
            dispatch(setComment(comment, index))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(CriteriaSheet);