import {Actions} from 'flummox';

export default class AudioActions extends Actions {
  changePosition(position) {
    return position;
  }

  togglePlay() {
    return true;
  }
};
