import {connect} from 'react-redux'
import {IssueList} from '../components/Issue'
import {} from '../actions'

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
    onDrop: (issueId, oldLane, newLane) => {
      dispatch();
    }
  }
};

const IssueListContainer = connect(
  mapStateToProps,
)(IssueList);

export default IssueListContainer;