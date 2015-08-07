import {Store} from 'flummox';
import constants from './constants.js';

export default class AudioStore extends Store {
  constructor(flux) {
    super();

  const audioActions = flux.getActions(constants.audio);
    this.register(audioActions.changePosition, this.handlePositionChange);
    this.register(audioActions.togglePlay, this.handleTogglePlay);
    this.register(audioActions.changeFile, this.handleChangeFile);
    this.register(audioActions.setLength, this.handleSetLength);

    this.state = {
      position: 0,
      src: 'audio.wav',

      playing: false,
      length: undefined
    };
  }

  handlePositionChange(position) {
    console.info('[AudioStore.js] ', 'position change', position);
    this.setState(state => ({position, playing: true}));
  }

  handleTogglePlay() {
    console.info('[AudioStore.js] ', 'toggle');
    this.setState(state => ({playing: !state.playing}));
  }

  handleChangeFile(file) {
    console.info('[AudioStore.js] ', 'change file', file);
    this.setState(state => ({src: file}));
  }

  handleSetLength(length) {
    console.info('[AudioStore.js] ', 'set length', length);
    this.setState(state => ({length}));
  }


}
