import React, {Component, PropTypes} from 'react';
import FluxComponent from 'flummox/component';
import constants from '../constants.js';

import Main from './Main.jsx';

const FILE = 'data/words.json';

export default class MainController extends Component {

  static contextTypes = {
    flux: PropTypes.any,
    cloud: PropTypes.bool
  }

  componentDidMount() {
    const wordActions = this.context.flux.getActions(constants.words)
    wordActions.getWords(FILE);
  }

  render() {

    return <FluxComponent 
      flux={this.context.flux} 
      connectToStores={[constants.words]}>

      <Main cloud={this.props.cloud}/>

    </FluxComponent>;

  }


}
