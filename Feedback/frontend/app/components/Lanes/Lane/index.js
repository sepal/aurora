import React, {PropTypes, Component} from 'react';
import {DropTarget} from 'react-dnd';

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
    issues: PropTypes.array,
    inbox: PropTypes.bool,
    archiving: PropTypes.bool
  };

  static defaultProps = {
    issues: [],
    inbox: false,
    archiving: false
  };

  render() {
    const {canDrop, isOver, connectDropTarget} = this.props;
    let content;

    let classes = 'lane';

    if (this.props.inbox) {
      classes += ' lane--inbox';
    } else if(this.props.archiving) {
      classes += ' lane--archive'
    }

    return connectDropTarget(
      <div className={classes} id={`lane--${this.props.id}`}>
        <h2 className="lane__title">{this.props.name}</h2>
        <div className="lane__content">
          <IssueListContainer laneId={this.props.id} />
        </div>
      </div>
    );
  }
}
