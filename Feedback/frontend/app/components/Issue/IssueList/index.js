import React from 'react';

import IssueTeaser from '../IssueTeaser';

const IssueList = ({issues, isStaff, current_user, onDrop}) => {
  // Build up the issues teasers.
  const issueTeasers = issues.map(issue => {
    let number_comments = 0;
    let upvotes = 0;

    if (issue['comments'] !== undefined) {
      number_comments = issue.comments;
    }

    if (issue['upvotes'] !== undefined) {
      upvotes = issue['upvotes'];
    }


    const preview = issue.preview !== undefined ? issue.preview : false;
    const isAuthor = current_user == issue.author.id;
    const lane = issue.lane.id;

    return (
      <li key={issue.id} className="issue-list__item">
        <IssueTeaser lane={lane} onDrop={onDrop} preview={preview}
                      canDrag={isStaff} isAuthor={isAuthor} {...issue}   />
      </li>
    );
  });

  // Build up the empty message.
  const msg = (
    <li className="issue-list__empty">
      No issues here yet.
    </li>
  );

  return (
    <ul>
      { issues.length > 0 ? issueTeasers : msg }
    </ul>
  );
};

export default IssueList;