import React, {Component, PropTypes} from 'react';
import Text from './Text.jsx';

export default class CloudLine extends Component {

  static propTypes = {
    word: PropTypes.object.isRequired
  }

  render() {
    const {positions, maxima, graph, word} = this.props.word;
    const [width, height] = ["100%", 80];


    return maximaText;
  }

}
