import {IssueActionTypes} from '../constants'

import {updateIssue, upvote} from '../api';


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
 * Adds an issue to the current app state.
 */
export function addIssue(issue) {
  return {
    type: IssueActionTypes.ADD_ISSUE,
    payload: {
      issue: issue
    }
  }
}

/**
 * Adds an upvote to the given issue.
 */
export function addUpvote(issueID) {
  return {
    type: IssueActionTypes.UPVOTE,
    payload: {
      issueID: issueID,
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
    dispatch(previewIssue(id, data));
    return updateIssue(data, id)
      .then((issue) => {dispatch(updatedIssue(issue))});
  }
}

/**
 * Async action, which creates a new issue.
 */
export function createIssue(data) {
  return function (dispatch) {
    // todo: dispatch waiting for issue posting.
    return updateIssue(data)
      .then((issue) => {
        dispatch(addIssue(issue));
      });
  }
}

/**
 * Async upvote an issue.
 */
export function upvoteIssue(issueID) {
  return function (dispatch) {
    dispatch(addUpvote(issueID));
    return upvote(issueID)
      .then((issue)=> {
        // todo: dispatch update upvote counter.
      });
  }
}