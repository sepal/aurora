import {observable, action} from 'mobx';

export default class Lane {
  @observable id;
  @observable name;
  @observable weight;
  @observable issues = [];

  constructor(data) {
    if (data != undefined) {
      this.fromJSON(data);
    }
  }

  @action addIssue(issue) {
    issue.lane = this;
    this.issues.push(issue);
  }

  @action removeIssue(issue_id) {
    this.issues.filter((issue, index) => {
      if (issue.id == issue_id) {
        this.issues.splice(index, 1);
      }
    });
  }

  @action fromJSON(object) {
    this.id = object['id'];
    this.name = object['name'];
    this.weight = object['weight'];
  }

  getIssue(issue_id) {
    let issues = this.issues.filter((issue) => {
      return issue.id == issue_id
    });

    return issues[0];
  }
}


