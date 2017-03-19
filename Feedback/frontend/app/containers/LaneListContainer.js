import {connect } from 'react-redux'
import {LaneList} from '../components/Lanes'

const mapStateToProps = (state) => {
  return {
    lanes: state.lanes,
    isStaff: state.current_user.isStaff
  }
};

const LaneListContainer = connect(
  mapStateToProps,
)(LaneList);

export default LaneListContainer