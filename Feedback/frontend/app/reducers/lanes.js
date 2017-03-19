import {LaneActionTypes} from '../constants'

const initialState = [];

export default function lanes(state = initialState, action) {
  switch (action.type) {
    case LaneActionTypes.ADD_LANE:
      return [...state, action.payload];
    default:
      return state;
  }
}