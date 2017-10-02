import PropTypes from 'prop-types';
import React from 'react';
import {getComments} from '../../api';

export default class Comments extends React.Component {
  static propTypes = {
    issueID: PropTypes.number.isRequired
  };

  state = {
    comments: ''
  };

  componentDidMount() {
    getComments(this.props.issueID).then((resp) => {
      const state = Object.assign(this.state, {comments: resp});
      this.setState(state);
      COMMENTS.registerAllTheElements();
      COMMENTS.fixEndlessPaginationLinks();
    });
  }

  render() {
    let body = (
      <div className="comment--body comment--body--loading">
        <i className="fa fa-spinner fa-spin" aria-hidden="true"></i> Loading comments...
      </div>
    );
    if (this.state.comments !== '') {
      body = (
          <div className="comment--body"
               dangerouslySetInnerHTML={this.createCommentsMarkup()}></div>
      );
    }

  return (
      <div className="issue__comments">
        {body}
      </div>
    )
  }

  createCommentsMarkup() {
    return {__html: this.state.comments}
  }
}