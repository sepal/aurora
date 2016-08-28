import {observable, action, computed} from 'mobx';

export default class Todo {
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
}