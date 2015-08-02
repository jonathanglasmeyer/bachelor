import React, {Component, PropTypes} from 'react';

export default class Audio extends Component {

  static propTypes = {
    src: PropTypes.string,
    position: PropTypes.number,
    foo: PropTypes.any,
    playing: PropTypes.bool
  }

  componentDidMount() {

    const player = React.findDOMNode(this.refs.player);
    // player.addEventListener('canplay', () =>
    //     this.setState({canPlay: true}));
    // player.addEventListener('play', () =>
    //     this.setState({playing: true}));
    // playerElement.addEventListener('timeupdate', this.audioUpdate);
    // playerElement.addEventListener('pause', this.audioPause);
  }

  componentDidUpdate() {
    this._skipToSecond(this.props.position);
    this._handleSetPlayingState();
  }

  render() {
    console.info('[Audio.jsx] ', 'render');

    return <audio
      controls="controls"
      style={{width: '100%'}}
      ref="player"
      preload="auto">
      <source src={'assets/' + this.props.src} type='audio/x-wav' />
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

}
