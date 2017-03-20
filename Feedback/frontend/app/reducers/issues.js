import {IssueActionTypes} from '../constants';
const initialState = [];

export default function issues(state = initialState, action) {
  switch (action.type) {
    case IssueActionTypes.PREVIEW_ISSUE:
      const id = action.payload.issueID;
      const data = action.payload.data;
      const newState = state.map((issue) => {
        if (issue.id == id) {
          data['preview'] = true;
          const newIssue = Object.assign(issue, data);
          return newIssue;
        }
        return issue;
      });
      return newState;
    case IssueActionTypes.UPDATED_ISSUE:
      const updatedIssue = action.payload.issue;
      return state.map((issue) => {
        if (issue.id == updatedIssue.id) {
          return updatedIssue;
        }
        return issue;
      });
    case IssueActionTypes.ADD_ISSUE:
      return [...state, action.payload.issue];
    case IssueActionTypes.UPVOTE:
      return state.map((issue) => {
        if (action.payload.issueID == issue.id && !issue.upvoted) {
          issue = Object.assign(issue, {
            upvotes: issue.upvotes + 1,
            upvoted: true
          });
        }
        return issue;
      });

    default:
      return state;
  }
}