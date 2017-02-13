import {IssueActionTypes} from '../constants';
const initialState = [];

export default function issues(state = initialState, action) {
  switch (action.type) {
    case IssueActionTypes.UPDATED_ISSUE:
      const updatedIssue =  action.payload.issue;
      return state.map((issue) => {
        if (issue.id == updatedIssue.id ) {
          return updatedIssue;
        } else {
          return issue;
        }
      });
      break;
    default:
      return state;
  }
}