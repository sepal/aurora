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

/**
 * Is dispatched before an async action request is send.
 */
export function previewIssue(issueID, data) {
  return {
    type: IssueActionTypes.PREVIEW_ISSUE,
    payload: {
      issueID: issueID,
      data: data
    }
  }
}

/**
 * Async action that switches the lane for an issue.
 */
export function switchLane(issue, newLane) {
  return function (dispatch) {
    const issueData = {
      lane: newLane,
      type: issue.type,
      title: issue.title,
      body: issue.body,
      course: issue.course
    };
    dispatch(previewIssue(issue.id, {lane: { id: newLane}}));
    return updateIssue(issueData, issue.id)
      .then((issue) => {dispatch(updatedIssue(issue))});
  }
}

/**
 * Updates either the title, type or body of an issue.
 */
export function changeIssue(data, id) {

  return function (dispatch) {
    return updateIssue(data, id)
      .then((issue) => {dispatch(updatedIssue(issue))});
  }
}