import React, {Component, PropTypes} from 'react';
import FluxComponent from 'flummox/component';
import constants from '../constants.js';

import Audio from './Audio.jsx';

export default class AudioController extends Component {

  static contextTypes = {
    flux: PropTypes.any
  }

  render() {

    return <FluxComponent 
      flux={this.context.flux} 
      connectToStores={[constants.audio]}>

      <Audio />

    </FluxComponent>;
  }

}
