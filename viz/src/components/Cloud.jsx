import React, {Component, PropTypes} from 'react';

import Section from './Section.jsx';
import WordTimeline from './WordTimeline.jsx';
import Text from './Text.jsx';
import Svg from './Svg.jsx';
import _ from 'lodash';

const style = {
  flexGrow: 1
}

// Returns a random integer between min (included) and max (excluded)
// Using Math.round() will give you a non-uniform distribution!
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function sortMaxima([[maxPos1, maxCount1], word],[[maxPos2, maxCount2], word2]) {
  return maxPos1 - maxPos2;
}

function sortMaximaByCount([[maxPos1, maxCount1], word],[[maxPos2, maxCount2], word2]) {
  return maxCount2 - maxCount1;
}

let randomWordYOffset = {};
function getRandomWordYOffset(word) {
  if (randomWordYOffset[word]) {
    return randomWordYOffset[word];
  } else {
    randomWordYOffset[word] = getRandomInt(-20, 20);
    return randomWordYOffset[word];
  }
}

Array.prototype.average=function(){
    var sum=0;
    var j=0;
    for(var i=0;i<this.length;i++){
        if(isFinite(this[i])){
          sum=sum+parseFloat(this[i]);
           j++;
        }
    }
    if(j===0){
        return 0;
    }else{
        return sum/j;
    }

}

const flatten = a => Array.isArray(a) ? [].concat(...a.map(flatten)) : a;

export default class Cloud extends Component {

  static propTypes = {
    words: PropTypes.array,
    selectedWord: PropTypes.any,
  }

  render() {
    let {words,selectedWord} = this.props;
    const [width, height] = ["100%", 480];
    const lengthSec = 3186;

    words = words.filter(w => w.maxima && w.maxima.length);

    let maxima = [];
    for (let w of words) {
      for (let maximum of w.maxima) {
        maxima.push([maximum, w]);
      }
    }
    maxima.sort(sortMaxima);
    const maximaChunks = _.chunk(maxima, 4);

    const wordElemBlockChunks = maximaChunks.map((maximaChunk,i) => {
      maximaChunk.sort(sortMaximaByCount);
      const maximaTextElems = maximaChunk.map(([[maxPos, count], word], j) => {
        const yPos = j*80 + getRandomWordYOffset(word.word);
        return <Text
         word={word}
         position={maxPos}
         key={maxPos}
         fontSize={13+count}
         x={`${maxPos*100/lengthSec}%`}
         y={60+yPos}>{word.word}</Text>
      })
      return maximaTextElems;

    });



    return <Section style={style}>
      <Svg height={height} width={width}>
        <rect height={height} width={width} x='0' y='0' fill='#333'/>
        <g transform="scale(1, 1)">
          {flatten(wordElemBlockChunks)}
        </g>
      </Svg>
      {<WordTimeline noSpan word={selectedWord} />}
    </Section>
  }

}
