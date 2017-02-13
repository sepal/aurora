import {connect} from 'react-redux'
import {IssueList} from '../components/Issue'
import {switchLane} from '../actions/issueActions'

const mapStateToProps = (state, ownProps) => {
  const issues = state.issues.filter(issue => {
    return issue.lane.id == ownProps.laneId;
  });

  return {
    issues: issues
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onDrop: (issueId, newLane) => {
      dispatch(switchLane(issueId, newLane));
    }
  }
};

const IssueListContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(IssueList);

export default IssueListContainer;