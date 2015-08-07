import {Actions} from 'flummox';

export default class WordsActions extends Actions {

  selectWord(word) {
    return word;
  }

  filterOutTopX(x) {
    return x;
  }

  async getWords(path) {
    const response = await fetch(path);
    const words = await response.json();
    console.dir(words);
    return words;
  }

};
