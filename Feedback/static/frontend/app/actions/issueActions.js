import {IssueActionTypes} from '../constants'

import {updateIssue} from '../api';


/**
 * This action is dispatched by async actions, after something on a issue was
 * updated.
 */
export function updatedIssue(issue) {
  return {
    type: IssueActionTypes.UPDATED_ISSUE,
    payload: {
      issue: issue
    }
  }
}

export function switchLane(issue, newLane) {
  return function (dispatch) {
    const issueData = {
      lane: newLane,
      type: issue.type,
      title: issue.title,
      body: issue.body,
      course: issue.course
    };
    return updateIssue(issueData, issue.id)
      .then((issue) => {dispatch(updatedIssue(issue))});
  }
}