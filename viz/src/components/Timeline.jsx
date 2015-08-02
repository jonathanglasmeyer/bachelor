import React, {Component, PropTypes} from 'react';

import shouldPureComponentUpdate from './utils/shouldPureComponentUpdate.js';

import Svg from './Svg.jsx';
import Text from './Text.jsx';
import Circle from './Svg/Circle.jsx';

const styles = {

};

export default class Timeline extends Component {

  static propTypes = {
    word: PropTypes.object.isRequired,
    maximaLines: PropTypes.bool // should vertical optima lines be rendered
  }

  shouldComponentUpdate = shouldPureComponentUpdate;

  render() {
    const {maximaLines} = this.props;
    const {positions, maxima, graph, word} = this.props.word || {};
    const lengthSec = 3186;
    const [width, height] = ["100%", 80];
    // if (graph) console.info('[Timeline.jsx] ', graph);
    if (!this.props.word) {
      return <Svg height={height} width={width}>
          <rect height={height} width={width} x='0' y='0' fill='#eee'/>
          <g transform="scale(1, 1)">
          </g>
        </Svg>;
    }

    let graphScaled, graphDots;

    if (graph) {
      const maxDensity = Math.max(...(graph.map(tuple => tuple[1])));
      graphScaled = graph.map(tuple => [tuple[0], tuple[1]/maxDensity]);
      graphDots = graphScaled.map(([position,density]) => <Circle
          color='#aaa'
          key={position}
          radius={1}
          cx={`${position*100/lengthSec}%`}
          cy={height*(1-density)} />);
    }

    const maximaDots = maxima && maxima.map(([position,count]) => <Circle
        color='red'
        key={position}
        radius={5}
        cx={`${position*100/lengthSec}%`}
        cy={height/2} />);

    // const maximaLineElems = maxima && maximaLines && maxima.map(([position,count]) => <Circle
    //     color='red'
    //     key={position}
    //     radius={5}
    //     cx={`${position*100/lengthSec}%`}
    //     cy={height/2} />);

    // const maximaText = maxima && maxima.map(([position,count]) => <Text
    //     key={position}
    //     fontSize={9+count}
    //     x={`${position*100/lengthSec}%`}
    //     y={height/2-20}>{word}</Text>);

    const positionDots = positions.map(position => <Circle
        key={position}
        radius={2}
        position={position}
        cx={`${position*100/lengthSec}%`}
        cy={height/2} />);

    const positionDotsBig = positions.map(position => <Circle
        hover
        key={position}
        radius={15}
        color='rgba(0,0,0,.03)'
        position={position}
        cx={`${position*100/lengthSec}%`}
        cy={height/2} />);

    return <Svg height={height} width={width} onClick={this._onClick.bind(this)}>
        <rect height={height} width={width} x='0' y='0' fill='#eee'/>
        <g transform="scale(1, 1)">
          {positionDots}
          {maxima && maximaDots}
          {graphScaled && graphDots}
          {positionDotsBig}
        </g>
      </Svg>;
          // {maxima && maximaLines && maximaLineElems}
  }

  _onClick(e) {
    console.info('[Timeline.jsx] ', e);
  }

}
