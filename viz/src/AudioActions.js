import {Actions} from 'flummox';

export default class AudioActions extends Actions {
  changePosition(position) {
    return position;
  }

  togglePlay() {
    return true;
  }

  changeFile(file) {
    return file;
  }

  setLength(length) {
    return length;
  }

};
