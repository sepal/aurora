import {observable, action, computed} from 'mobx';
import Lane from './lane';
import Issue from './issue';


class KanbanStore {
  @observable course;
  @observable lanes = [];

  loadFromJSONString(data) {
    try {
      data = JSON.parse(data);
    } catch ($exception) {
      console.error(`Cound not parse intial data due to ${$exception}`);
      return;
    }

    this.course = data.course;
    data.lanes.forEach((lane_data) => {
      this.lanes.push(new Lane(lane_data));
    });

    data.issues.forEach((issue_data) => {
      let lane = this.getLane(issue_data['lane']['id']);
      lane.addIssue(new Issue(issue_data));
    });
  }

  getLane(lane_id) {
    let lanes = this.lanes.filter((lane) => {
      return lane.id == lane_id
    });
    return lanes[0];
  }
}

export default new KanbanStore();