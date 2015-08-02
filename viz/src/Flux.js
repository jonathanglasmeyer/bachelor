import {Flummox} from 'flummox';
import AudioStore from './AudioStore.js';
import AudioActions from './AudioActions.js';
import WordsStore from './WordsStore.js';
import WordsActions from './WordsActions.js';

import constants from './constants.js';


export default class Flux extends Flummox {
  constructor() {
    super();

    this.createActions(constants.audio, AudioActions);
    this.createStore(constants.audio, AudioStore, this);
    this.createActions(constants.words, WordsActions);
    this.createStore(constants.words, WordsStore, this);
  }
}
