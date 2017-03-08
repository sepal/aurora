import {connect} from 'react-redux'
import {IssueDetail} from '../components/Issue'
import {changeIssue, upvoteIssue} from '../actions/issueActions';

const mapStateToProps = (state, ownProps) => {
  const issue = state.issues.filter(issue => {
    return issue.id == ownProps.params.id
  })[0];

  return {
    isStaff: state.current_user.is_staff,
    isAuthor: issue.author.id == state.current_user.id ,
    ...issue
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    update: (id, type, title, body) => {
      dispatch(changeIssue({type: type, title: title, body: body}, id));
    },
    upvote: (id) => {
      dispatch(upvoteIssue(id));
    }
  };
};

const IssueContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(IssueDetail);

export default IssueContainer;