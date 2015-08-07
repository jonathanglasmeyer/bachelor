import React, {Component, PropTypes} from 'react';
import FluxComponent from 'flummox/component';
import constants from '../constants.js';

import Audio from './Audio.jsx';

export default class AudioController extends Component {

  static propTypes = {
    file: PropTypes.string
  }

  static contextTypes = {
    flux: PropTypes.any
  }

  render() {
    console.info('[AudioController.jsx] ', this.props.file);

    return <FluxComponent
      flux={this.context.flux}
      connectToStores={[constants.audio]}>

      <Audio src={this.props.file} />

    </FluxComponent>;
  }

}
