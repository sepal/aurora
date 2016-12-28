import {observable, action, computed} from 'mobx';
import {getCookieSetting} from '../utilities';

export default class Issue {
  @observable id;
  @observable post_date;
  @observable course;
  @observable author;
  @observable lane;
  @observable type;
  @observable title;
  @observable body;

  constructor(data) {
    if (data != undefined) {
      this.fromJSON(data);
    }
  }

  @action fromJSON(data) {
    // Required data.
    this.id = data['id'];
    this.title = data['title'];
    this.type = data['type'];
    this.lane = data['lane'];
    console.log(data['lane']);

    // Optional data, for detail view only.
    if ('course' in data)
      this.course = data['course'];

    if ('post_date' in data)
      this.post_date = data['post_date'];

    if ('author' in data)
      this.author = data['author']['name'];

    if ('body' in data)
      this.body = data['body'];

  }

  @action loadFromAJAX(id) {
    $.ajax({
      url: `/gsi/feedback/api/issue/${id}`
    }).done((resp) => {
      this.fromJSON(resp);
    });
  }

  @action update() {
    let url = `/gsi/feedback/api/issue`;
    let method = 'POST';

    if (this.id != undefined) {
      url = `/gsi/feedback/api/issue/${this.id}`;
      method = 'PUT';
    }

    return new Promise((resolve, reject) => {
      const data = JSON.stringify({
        lane: this.lane.id,
        type: this.type,
        title: this.title,
        body: this.body,
        course: this.course
      });

      $.ajax({
        method: method,
        headers: {
          'X-CSRFToken': getCookieSetting('csrftoken'),
          'Content-Type': 'application/json'
        },
        data: data,
        url: url
      }).done((resp) => {
        var updatedIssue = new Issue();
        try {
          updatedIssue.fromJSON(resp);
        } catch (exception) {
          reject(exception);
          return;
        }
        resolve(updatedIssue);
      }).fail((err) => {
        reject(err);
      });
    });
  }

  // Should contain the same as Issue model in python.
  options() {
    return {
      bug: 'Bug',
      feature_request: 'Feature Request',
      feedback: 'Feedback',
      security: 'Security'
    };
  };
}
