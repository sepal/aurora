import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {DragSource} from 'react-dnd';
import {Link} from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

import IssueLabel from '../IssueLabel';
import IssueIcon from '../IssueIcon';
import {ItemTypes} from '../../../constants';
import {IssueTypes} from '../../../constants'

const issueSource = {
  canDrag(props) {
    return props.canDrag;
  },

  beginDrag(props) {
    return {
      issue: props,
      onDrop: props.onDrop,
    }
  },

  endDrag(props, monitor) {
    const item = monitor.getItem();
    const dropResult = monitor.getDropResult();
  }
};

@DragSource(ItemTypes.ISSUE, issueSource, (connect, monitor) => ({
  connectDragSource: connect.dragSource(),
  isDragging: monitor.isDragging()
}))
export default class IssueTeaser extends Component {
  static propTypes = {
    connectDragSource: PropTypes.func.isRequired,
    isDragging: PropTypes.bool.isRequired,
    onDrop: PropTypes.func.isRequired,
    id: PropTypes.number.isRequired,
    body: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    isAuthor: PropTypes.bool,
    canDrag: PropTypes.bool,
    upvotes: PropTypes.number,
    comments: PropTypes.number,
    preview: PropTypes.bool,
    archived: PropTypes.bool,
    staff: PropTypes.bool
  };

  static defaultProps = {
    isAuthor: false,
    canDrag: false,
    upvotes: 0,
    comments: 0,
    preview: false,
    archived: false
  };

  render() {
    const {isDragging, connectDragSource} = this.props;

    let className = "issue--teaser";

    if (this.props.preview === true) {
      className += ' issue--teaser--preview';
    }

    if (this.props.archived === true) {
      className += ' issue--teaser--archived';
    }

    if (this.props.staff === true) {
      className += ' issue--teaser--staff';
    }

    if (this.props.type == 'security') {
      className += " issue--teaser--security";
    } else if (this.props.isAuthor) {
      className += " issue--teaser--owned";
    }


    return connectDragSource(
      <div>
        <Link
          key={this.props.id}
          to={{
            pathname: `/${course_short_title}/feedback/issue/${this.props.id}`,
            state: {returnTo: `/${course_short_title}/feedback`}
          }}
          className={className}>
          <div className="issue--teaser__header">
            <span className="issue--teaser__icon">
              <IssueIcon type={this.props.type} />
            </span> {this.props.title}
          </div>
          {this.renderBody()}
          {this.renderFooter()}
        </Link>
      </div>
    );
  }

  renderBody() {
    if (!this.props.archived) {
      const body_preview = this.props.body.substring(0, 100);
      return (
        <div className="issue--teaser__body">
          <ReactMarkdown source={body_preview}
                         disallowedTypes={['HtmlInline', 'HtmlBlock']}
                         escapeHtml={true} />
        </div>
      )
    }
  }

  renderFooter() {
    if (!this.props.archived) {
      let upvote_label = this.props.upvotes == 1 ? "upvote" : "upvotes";
      let comment_label = this.props.comments == 1 ? "comment" : "comments";
      return (
        <div className="issue--teaser__footer">
            <span className="issue--teaser__upvotes">
              <i
                className="fa fa-thumbs-up"></i> {this.props.upvotes} {upvote_label}
            </span>
          <span className="issue--teaser__comments">
              <i
                className="fa fa-comments"></i> {this.props.comments} {comment_label}
            </span>
        </div>
      );
    }
  }
}
