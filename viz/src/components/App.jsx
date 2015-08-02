
import React, {Component, PropTypes} from 'react';
import constants from '../constants.js';
import AudioController from './AudioController.jsx';
import Footer from './Footer.jsx';
import MainController from './MainController.jsx';

import {dimension} from '../style/vars.js';

const KEY_SPACE = 32;
export default class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      cloud: false
    };
  }

  render() {
    const {position} = this.props;

    return <div>
      <MainController cloud={this.state.cloud} />
      <Footer>
        <AudioController/>
        <input 
          type="checkbox" 
          value="Cloud" 
          checked={this.state.cloud}
          onChange={this._onCheck.bind(this)}/>
      </Footer>
    </div>;
  }

  componentDidMount() {
    const audioActions = this.props.flux.getActions(constants.audio)

    window.onkeydown = function(e) {
       const key = e.keyCode ? e.keyCode : e.which;

       if (key == KEY_SPACE) {
         e.preventDefault();
         audioActions.togglePlay();
       }
    }
  }

  _onCheck() {
    this.setState({cloud: !this.state.cloud});
  }

}

