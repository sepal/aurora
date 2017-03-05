import React from 'react';

function IssueIcon(props) {
  switch (props.type) {
    case 'feature_request':
      return <i className="fa fa-lightbulb-o"></i>;
    case 'bug':
      return <i className="fa fa-bug"></i>;
    case 'feedback':
      return <i className="fa fa-commenting-o"></i>;
    case 'security':
      return <i className="fa fa-lock"></i>;
  }
  return (
    <i></i>
  )
}

export default IssueIcon;
