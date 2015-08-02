import React, {Component, PropTypes} from 'react';
import WordsOverviewItem from './WordsOverviewItem.jsx';
import Section from './Section.jsx';

import {dimension, color} from '../style/vars.js';


const listStyle = {
  listStyleType: 'none'
};

const styleSection = {
  borderRight: '2px solid #ddd',
  minWidth: 200
};

export default class WordsOverviewList extends Component {

  static propTypes = {
    words: PropTypes.array.isRequired
  }

  render() {
    const {words} = this.props;

    return <Section minWidth={200} style={styleSection}>
      <ul style={listStyle}>
        {words.map(w => <WordsOverviewItem
          key={w.word}
          word={w} />)}
      </ul>;
    </Section>;

  }

}
