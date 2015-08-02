import React, {Component, PropTypes} from 'react';

import FluxComponent from 'flummox/component';
import Flux from '../Flux.js';

import App from './App.jsx';

const flux = new Flux();

export default class AppController extends Component {

  render() {

    return <FluxComponent
      flux={flux}>

      <App />

    </FluxComponent>;

  }

}
