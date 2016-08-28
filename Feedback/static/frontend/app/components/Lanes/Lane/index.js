import React from 'react';
import CSSModules from 'react-css-modules';
import {observer} from 'mobx-react';
import styles from './style.scss';

import {IssueList} from '../../Issue';

@observer
class Lane extends React.Component {
  renderIssueTeaser() {
    return <IssueList issues={this.props.issues} />
  }
  render() {
    let content;

    if (this.props.issues.length  == 0) {
      content = <div styleName="empty">No issues here yet.</div>
    }
    else {
      content = this.renderIssueTeaser();
    }

    return (
      <div styleName='lane'>
        <h2 styleName="title">{this.props.name}</h2>
        <div styleName="content">
          {content}
        </div>
      </div>
    );
  }
}

export default CSSModules(Lane, styles)
