import React, {Component, PropTypes} from 'react';
import constants from '../constants.js';

const style = {
  cursor: 'pointer'
};

export default class WordsOverviewItem extends Component {

  static propTypes = {
    word: PropTypes.any,
  }

  static contextTypes = {
    flux: PropTypes.any
  }

  render() {
    const {word} = this.props;

    return <li style={style} onClick={this._onClick.bind(this)}>
      {word.word} ({word.freq})
    </li>;
  }

  _onClick() {
    this.context.flux.getActions(constants.words).selectWord(this.props.word);
  }

}
