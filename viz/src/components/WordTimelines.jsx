
import React, {Component, PropTypes} from 'react';

import WordTimeline from './WordTimeline.jsx';
import Section from './Section.jsx';
import m from 'mori';

const style = {
  flexGrow: 1
}

const listStyle = {
    listStylePosition: 'inside'
};

function median(values) {

    values.sort( function(a,b) {return a - b;} );

    var half = Math.floor(values.length/2);

    if(values.length % 2)
        return values[half];
    else
        return (values[half-1] + values[half]) / 2.0;
}

export default class WordTimeslines extends Component {

  static propTypes = {
    words: PropTypes.any,
    length: PropTypes.number
  }


  render() {
    let {words, length} = this.props;
    console.info('[WordTimelines.jsx] ', length);

    return <Section style={style}>
      <ul style={listStyle}>
        {words.map(w => <WordTimeline
          key={w.word}
          length={length}
          word={w} />)}
      </ul>
    </Section>;
  }


}
