import React, {PropTypes, Component} from 'react';
import {DropTarget} from 'react-dnd';

import styles from './style.scss';
import {IssueListContainer} from '../../../containers';
import {ItemTypes} from '../../../constants';


const laneTarget = {
  drop(props, monitor, component) {
    const issue_ctx = monitor.getItem();

    issue_ctx.onDrop(issue_ctx.issue, props.id);
  },
};

@DropTarget(ItemTypes.ISSUE, laneTarget, (connect, monitor) => ({
  connectDropTarget: connect.dropTarget(),
  isOver: monitor.isOver(),
  canDrop: monitor.canDrop()
}))
export default class Lane extends Component {
  static propTypes = {
    connectDropTarget: PropTypes.func.isRequired,
    isOver: PropTypes.bool.isRequired,
    canDrop: PropTypes.bool.isRequired,
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    issues: PropTypes.array
  };

  render() {
    const {canDrop, isOver, connectDropTarget} = this.props;
    let content;

    return connectDropTarget(
      <div className={styles.lane}>
        <h2 className={styles.title}>{this.props.name}</h2>
        <div className={styles.content}>
          <IssueListContainer laneId={this.props.id} />
        </div>
      </div>
    );
  }
}
