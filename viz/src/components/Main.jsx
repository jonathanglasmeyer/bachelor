import React, {Component, PropTypes} from 'react';
import FluxComponent from 'flummox/component';

import WordTimeslines from './WordTimelines.jsx';
import Cloud from './Cloud.jsx';
import WordsOverviewList from './WordsOverviewList.jsx';

import {dimension} from '../style/vars.js';
import constants from '../constants.js';

const styles = {
  marginLeft: dimension.grid,
  marginRight: dimension.grid,
  marginTop: dimension.grid*2,
  marginBottom: (dimension.Navbar.height + dimension.grid),

  display: 'flex'

};


export default class Main extends Component {

  static propTypes = {
    words: PropTypes.any,
    selectedWord: PropTypes.any,
    clouds: PropTypes.bool
  }

  render() {
    const {words, selectedWord, cloud} = this.props;

    return words ? 
      <main style={styles}>
        {!cloud ? <Cloud {...{selectedWord,words}} /> : <WordTimeslines words={words} /> }
      </main> : <div>No file loaded.</div>
  }


}
