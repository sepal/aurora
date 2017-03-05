import {combineReducers} from 'redux'
import issues from './issues'
import lanes from './lanes'
import current_user from './current_user'

export default combineReducers({
  lanes,
  issues,
  current_user
})