import {Store} from 'flummox';
import constants from './constants.js';
import React from 'react';
import top5000 from 'json!./data/top5000.json';

export default class WordsStore extends Store {
  constructor(flux) {
    super();

    const wordsActions = flux.getActions(constants.words);
      this.register(wordsActions.selectWord,
            this.handleSelectWord);

      this.register(wordsActions.getWords, this.handleGetWords);
      this.register(wordsActions.filterOutTopX, this.handleFilterOutTopX);

    this.state = {
      words: [],
      selectedWord: null,
    };

  }

  handleSelectWord(word) {
    this.setState({selectedWord: word});
  }

  async handleGetWords(words) {
    // let words_ = words.filter(word => word.freq > 3).slice(0,20);
    let words_ = words.filter(word => word.freq > 3);
    words_ = words_.map(word => {
      let positionsSec = word.positions.map(p => p/1000);
      let maxima = word.maxima ? word.maxima.map(([pos, count]) => [pos/1000, count]) : null;
      word.positions = positionsSec;
      if (maxima) word.maxima = maxima;
      return word;
    });
    this.setState({words: words_, selectedWords: words_});
  }

  // handleFilterOutTopX(x) {
//   let words = this.state.words.filter(w => top5000.slice(0,x).indexOf(w.word) < 0);
//   console.info('[WordsStore.js] ', words.length);
  //   this.setState({selectedWords: words});
  // }

}
