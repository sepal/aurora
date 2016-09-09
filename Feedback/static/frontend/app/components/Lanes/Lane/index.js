import React from 'react';
import {observer} from 'mobx-react';
import styles from './style.scss';

import {IssueList} from '../../Issue';

@observer
export default class Lane extends React.Component {
  renderIssueTeaser() {
    return <IssueList issues={this.props.issues} />
  }
  render() {
    let content;

    if (this.props.issues.length  == 0) {
      content = <div className={styles.empty}>No issues here yet.</div>
    }
    else {
      content = this.renderIssueTeaser();
    }

    return (
      <div className={styles.lane}>
        <h2 className={styles.title}>{this.props.name}</h2>
        <div className={styles.content}>
          {content}
        </div>
      </div>
    );
  }
}
