import {observable, action} from 'mobx';

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
      this.course = data['course']['name'];

    if ('post_date' in data)
      this.course = data['post_date'];

    if ('author' in data)
      this.course = data['author'];

    if ('body' in data)
      this.course = data['body'];

  }

  @action loadFromAJAX(id) {
    $.ajax({
      url: `/gsi/feedback/api/issue/${id}`
    }).done((resp) => {
      this.fromJSON(resp);
    });
  }
}