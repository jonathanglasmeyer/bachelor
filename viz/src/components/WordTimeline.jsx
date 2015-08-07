
import React, {Component, PropTypes} from 'react';

import Timeline from './Timeline.jsx';

const style = {
  display: 'flex',
  height: 100
};

const spanStyle = {
  minWidth: 200
};

export default class Word extends Component {

  static propTypes = {
    word: PropTypes.object.isRequired,
    noSpan: PropTypes.bool,
    length: PropTypes.number
  }

  render() {
    const {word, noSpan, length} = this.props;
    const {positions, maxima, graph} = word || {};
    const style_ = Object.assign(style, noSpan ? 
        {flexDirection: 'column'} : {});

    return <div style={style}>
      {word &&
        <span style={spanStyle}>
        <b>{word.word}</b> ({positions.length}/{word.freq})
        </span>
      }

      <Timeline maximaLines {...{word, length}} />
    </div>;
      // <ul>
      //   {(word.positions).map(position => <Position
      //       key={position}
      //       position={position} />)}
      // </ul>
  }

}
