
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
  }

  // shouldComponentUpdate(nextProps) {
  //   if (nextProps.word) {
  //     return nextProps.word.word !== this.props.word.word;
  //   } else {
  //     return true;
  //   }
  // }

  render() {
    const {word, noSpan} = this.props;
    const {positions, maxima, graph} = word || {};
    const style_ = Object.assign(style, noSpan ? 
        {flexDirection: 'column'} : {});

    return <div style={style}>
    {word &&
      <span style={spanStyle}>
      <b>{word.word}</b> ({positions.length}/{word.freq})
      </span>
    }
      <Timeline maximaLines {...{word}} />
    </div>;
      // <ul>
      //   {(word.positions).map(position => <Position
      //       key={position}
      //       position={position} />)}
      // </ul>
  }

}
