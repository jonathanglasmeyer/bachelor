import {Store} from 'flummox';
import constants from './constants.js';

export default class AudioStore extends Store {
  constructor(flux) {
    super();

  const audioActions = flux.getActions(constants.audio);
    this.register(audioActions.changePosition, this.handlePositionChange);
    this.register(audioActions.togglePlay, this.handleTogglePlay);

    this.state = {
      position: 0,
      src: 'psy2.wav',

      playing: false
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

}
