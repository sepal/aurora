import React from 'react';
import {getComments} from '../../api';

export default class Comments extends React.Component {
  static propTypes = {
    issueID: React.PropTypes.number.isRequired
  };

  constructor(props) {
    super(props);

    this.state = {
      comments: ''
    };
  }

  componentDidMount() {
    getComments(this.props.issueID).then((resp) => {
      const state = Object.assign(this.state, {comments: resp});
      this.setState(state);
      COMMENTS.registerAllTheElements();
      COMMENTS.fixEndlessPaginationLinks();
    });
  }

  render() {
    var my;
    return (
      <div>
        <div
          dangerouslySetInnerHTML={this.createCommentsMarkup()}></div>
      </div>
    )
  }

  createCommentsMarkup() {
    return {__html: this.state.comments}
  }
}