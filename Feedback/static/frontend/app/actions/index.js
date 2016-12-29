import * as types from '../constants/ActionTypes'

export const addIssue = (title, type, body) => ({
  type: types.ADD_ISSUE,
  payload: {
    title,
    type,
    body,
    lane: 1
  }
});

export const  removeIssue = (issue_id) => ({
  type: types.REMOVE_ISSUE,
  payload: {
    issue: {
      id: issue_id,
    },
  }
});

export const switchLane = (issue_id, new_lane_id) => ({
  types: types.SWITCH_LANE,
  payload: {
    issue: {
      id: issue_id,
    },
    lane: {
      id: new_lane_id,
    },
  }
});