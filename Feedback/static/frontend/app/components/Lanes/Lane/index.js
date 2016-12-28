import React, {PropTypes, Component} from 'react';
import {observer} from 'mobx-react';
import {DropTarget} from 'react-dnd';

import styles from './style.scss';
import {IssueList} from '../../Issue';
import {ItemTypes} from '../../../constants';
import kanbanStore from '../../../models/kanbanStore';


const laneTarget = {
  drop(props, monitor, component) {
    const issue_ctx = monitor.getItem();
    const oldLane = kanbanStore.getLane(issue_ctx.lane);
    const newLane = kanbanStore.getLane(props.id);

    let issue = oldLane.getIssue(issue_ctx.id);
    oldLane.removeIssue(issue_ctx.id);
    newLane.addIssue(issue);
    issue.update();

    return {
      id: props.id,
    }
  },
};

@observer
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
    issues: PropTypes.array
  };

  renderIssueTeaser() {
    return <IssueList issues={this.props.issues} />
  }

  render() {
    const {canDrop, isOver, connectDropTarget} = this.props;
    let content;

    if (this.props.issues.length == 0) {
      content = <div className={styles.empty}>No issues here yet.</div>
    }
    else {
      content = this.renderIssueTeaser();
    }

    return connectDropTarget(
      <div className={styles.lane}>
        <h2 className={styles.title}>{this.props.name}</h2>
        <div className={styles.content}>
          {content}
        </div>
      </div>
    );
  }
}
