import React, {Component, PropTypes} from 'react';
import constants from '../constants.js';

export default class Audio extends Component {

  static propTypes = {
    src: PropTypes.string,
    position: PropTypes.number,
    playing: PropTypes.bool
  }

  componentDidMount() {
    const player = React.findDOMNode(this.refs.player);
    player.addEventListener('canplay', () =>
        this._setLength(player.duration));
  }

  componentDidUpdate(prevProps) {
    if (this.props.src) {
      this._skipToSecond(this.props.position);
      this._handleSetPlayingState();
    }

    if (prevProps.src !== this.props.src) {
      const player = React.findDOMNode(this.refs.player);
      player.load();
      console.info('[Audio.jsx] ', player.durationuuuuuu);
    }
  }

  render() {
    console.info('[Audio.jsx] ', this.props);

    return <audio
      controls="controls"
      style={{width: '100%', paddingRight: 20}}
      ref="player"
      preload="auto">
        <source src={'data/' + this.props.src} type='audio/x-wav' />
      </audio>;
  }


  _skipToSecond(second) {
    const player = React.findDOMNode(this.refs.player);
    player.currentTime = second > 1 ? second-1 : second;
    if (second) player.play();
  }

  _handleClickPlay() {
    const player = React.findDOMNode(this.refs.player);
    player.play();
  }

  _handleSetPlayingState() {
    const player = React.findDOMNode(this.refs.player);
    if (this.props.playing) {
      player.play();
    } else {
      player.pause();
    }

  }

  _setLength(length) {
    this.props.flux.getActions(constants.audio).setLength(length);
  }

}
