import React, {Component, PropTypes} from 'react';
import FluxComponent from 'flummox/component';
import constants from '../constants.js';

import Main from './Main.jsx';

const FILE = 'data/words.json';

export default class MainController extends Component {
  static propTypes = {
    cloud: PropTypes.bool,
    file: PropTypes.string.isRequired
  }

  static contextTypes = {
    flux: PropTypes.any
  }

  componentDidMount() {
    const wordActions = this.context.flux.getActions(constants.words);
    if (this.props.file) {
      wordActions.getWords(`data/${this.props.file}`);
    }
  }

  componentDidUpdate() {
    const wordActions = this.context.flux.getActions(constants.words);
    if (this.props.file) {
      wordActions.getWords(`data/${this.props.file}`);
    }
  }

  render() {

    return <FluxComponent
      flux={this.context.flux}
      connectToStores={[constants.words]}>

      <Main cloud={this.props.cloud}/>

    </FluxComponent>;

  }


}
