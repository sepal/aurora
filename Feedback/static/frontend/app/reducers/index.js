import {combineReducers} from 'redux'
import issues from './issues'
import lanes from './lanes'

export default combineReducers({
  lanes,
  issues
})