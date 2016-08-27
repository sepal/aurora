import {observable, action} from 'mobx';

export default class Lanes {
  @observable id;
  @observable name;
  @observable weight;
  @observable issues = [];
}