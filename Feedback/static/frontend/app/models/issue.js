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

  constructor() {
  }

  @action loadFromJSON(data) {
    this.id = data['id'];
    this.course = data['course']['name'];
    this.post_date = data['post_date'];
    this.lane = data['lane']['name'];
    this.type = data['type'];
    this.title = data['title'];
    this.body = data['body'];
  }

  @action loadFromAJAX(id) {
    $.ajax({
      url: '/gsi/feedback/api/issue/1'
    }).done((resp) => {
      this.loadFromJSON(resp);
    });
  }
}