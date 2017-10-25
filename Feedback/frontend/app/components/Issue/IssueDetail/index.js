import Moment from 'moment';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import platform from 'platform';

import IssueLabel from '../IssueLabel'
import IssueIcon from '../IssueIcon';
import IssueBody from '../IssueBody';

import Comments from '../../Comments';

export default class IssueDetail extends Component {
  static propTypes = {
    id: PropTypes.number.isRequired,
    type: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    isAuthor: PropTypes.bool,
    canDrag: PropTypes.bool,
    upvotes: PropTypes.number,
    comments: PropTypes.number,
    preview: PropTypes.bool,
    body: PropTypes.string,
    user_agent: PropTypes.string
  };

  constructor(props) {
    super(props);

    this.onLabelTypeChange = this.onLabelTypeChange.bind(this);
    this.onBodyChange = this.onBodyChange.bind(this);
    this.onUpvote = this.onUpvote.bind(this);
  }

  render() {
    const upvote_label = this.props.upvotes == 1 ? "upvote" : "upvotes";
    const date = Moment(this.props.post_date).calendar();
    const canEdit = this.props.isAuthor || this.props.isStaff;

    let upvote_action = <button onClick={this.onUpvote}><i
      className="fa fa-thumbs-up"></i> upvote</button>;
    if (this.props.upvoted) {
      upvote_action = <span><i className="fa fa-thumbs-up"></i> upvoted</span>;
    }

    return (
      <div className="issue--detail">
        <div>
          <div className="issue--detail__title">
            <span className="issue--detail__icon">
              <IssueIcon type={this.props.type} />
            </span>
            <IssueLabel
              type={this.props.type}
              title={this.props.title}
              onChange={this.onLabelTypeChange}
              editable={canEdit} />
          </div>
          <div className="issue--detail__subtitle">
            <span>by {this.props.author.name}</span>&nbsp;
            <span>on {date}</span>,&nbsp;
            <span>{this.props.upvotes ? this.props.upvotes : 0} {upvote_label}</span>
          </div>
        </div>
        <div className="issue--detail__content">
          <IssueBody className="issue--detail__body" body={this.props.body}
                     onChange={this.onBodyChange} editable={canEdit} />
          <ul className="issue--detail__actions">
            <li>
              {upvote_action}
            </li>
          </ul>
        </div>
        {this.renderPlatform()}
        <Comments issueID={this.props.id} />
      </div>
    );
  }

  renderImages() {
    if (this.props.images) {
      const images = this.props.images.map(image => {
        return (
          <li>
            <a href={image} target="_blank"><img src={image} /></a>
          </li>
        )
      });

      return (
        <ul className="issue--detail__images">
          {images}
        </ul>
      )
    }
  }

  renderPlatform() {
    if (this.props.user_agent !== undefined) {
      const info = platform.parse(this.props.user_agent);
      let product = null;
      if (info.product !== null) {
        product = (
          <li>
            <span className="label">Device:</span> <span
            className="value">{`${info.product}`}</span>
          </li>
        );
      }

      return (
        <div className="issue--detail__platform">
          <h2>Platform:</h2>
          <ul>
            <li>
              <span className="label">Browser:</span> <span
              className="value">{`${info.name} ${info.version}`}</span>
            </li>
            <li>
              <span className="label">Operating system:</span> <span
              className="value">{`${info.os.family} ${info.os.version}`}</span>
            </li>
            {product}
          </ul>
        </div>
      )
    }
  }

  onLabelTypeChange(type, title) {
    this.props.update(this.props.id, type, title, this.props.body);
  }

  onBodyChange(body) {
    this.props.update(this.props.id, this.props.type, this.props.title, body);
  }

  onUpvote() {
    this.props.upvote(this.props.id);
  }
}
