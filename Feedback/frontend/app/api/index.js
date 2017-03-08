import {getCookieSetting} from '../utilities';

export function getInitialData() {
  let jsonString = document.getElementById('data').innerHTML;

  return new Promise((resolve, reject) => {
    try {
      let data = JSON.parse(jsonString);
      resolve(data);
    } catch ($exception) {
      reject($exception);
    }
  });
}

export function getIssue(id) {
  return new Promise((resolve, reject) => {
    try {
      $.ajax({
        url: `/${course_short_title}/feedback/api/issue/${id}`
      }).done((resp) => {
        // Required fields.
        let issue = {
          'id': resp['id'],
          'title': resp['title'],
          'type': resp['type'],
          'lane': resp['lane'],
        };

        if ('course' in resp)
          issue.course = resp['course'];

        if ('post_date' in resp)
          issue.post_date = resp['post_date'];

        if ('author' in resp)
          issue.author = resp['author']['name'];

        if ('body' in resp)
          issue.body = resp['body'];

        resolve(issue);
      }).fail((reason) => {
        reject(reason);
      });
    } catch ($exception) {
      reject($exception);
    }
  });
}

export function updateIssue(data, id = undefined) {
  let url = `/${course_short_title}/feedback/api/issue`;
  let method = 'POST';

  if (id != undefined) {
    url = `/${course_short_title}/feedback/api/issue/${id}`;
    method = 'PUT';
  }

  return new Promise((resolve, reject) => {
    try {
      const json = JSON.stringify(data);

      $.ajax({
        method: method,
        headers: {
          'X-CSRFToken': getCookieSetting('csrftoken'),
          'Content-Type': 'application/json'
        },
        data: json,
        url: url
      }).done((resp) => {
        resolve(resp);
      }).fail((err) => {
        reject(err);
      });
    } catch ($exception) {
      reject($exception);
    }
  });
}

export function getComments(issueID) {
  const url = `/${course_short_title}/feedback/comments/${issueID}`;
  return new Promise((resolve, reject) => {
    $.ajax({
      url: url,
    }).done((resp) => {
      resolve(resp);
    }).fail((err) => {
      reject(err);
    });
  });
}

export function upvote(issueID) {
  const url = `/${course_short_title}/feedback/api/upvote/${issueID}`;
  return new Promise((resolve, reject) => {
    $.ajax({
      method: 'POST',
      url: url,
      headers: {
        'X-CSRFToken': getCookieSetting('csrftoken'),
      }
    }).done((resp) => {
      resolve(resp);
    }).fail((err) => {
      reject(err);
    });
  });
}