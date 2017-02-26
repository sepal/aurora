import {connect} from 'react-redux'
import {IssueForm} from '../components/Issue'
import {createIssue} from '../actions/issueActions';


const mapStateToProps = (state, ownProps) => {
  return {}
};

const mapDispatchToProps = (dispatch) => {
  return {
    createIssue: (type, title, body) => {
      dispatch(createIssue({type: type, title: title, body: body}))
    }
  }
};

const IssueFormContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(IssueForm);

export default IssueFormContainer;