
import React, {Component, PropTypes} from 'react';
import constants from '../constants.js';
import AudioController from './AudioController.jsx';
import Footer from './Footer.jsx';
import MainController from './MainController.jsx';
import './app.less';

import {dimension} from '../style/vars.js';

const formStyle = {
  marginTop: 20,
  display: 'flex'
};

const KEY_SPACE = 32;
export default class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      cloud: false,
      jsonFile: 'words.json'
    };
  }

  render() {
    const {position} = this.props;
    const {audioFile, jsonFile, cloud} = this.state;

    return <div>
      <MainController cloud={cloud} file={jsonFile} />
      <Footer>
        <AudioController file={audioFile} />
        <div style={formStyle}>
        <label>
          <input
            type="checkbox"
            value="Cloud"
            checked={!this.state.cloud}
            onChange={this._onCheck.bind(this)}/>
          {'Cloud Mode'}
        </label>
        <label>
        {'JSON: '}
          <input onChange={this._onSubmitFileJson.bind(this)} placeholder='file' type="file" ref='fileJson' />
        </label>
        <label>
        {'Audio: '}
        <input onChange={this._onSubmitFileAudio.bind(this)} placeholder='file' type="file" ref='fileAudio' />
        </label>
        </div>
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

  _onSubmitFileJson(e) {
    e.preventDefault();
    const input = React.findDOMNode(this.refs.fileJson);
    this.setState({jsonFile: e.target.files[0].name});
  }

  _onSubmitFileAudio(e) {
    e.preventDefault();
    const input = React.findDOMNode(this.refs.fileAudio);
    const audioActions = this.props.flux.getActions(constants.audio);
    audioActions.changeFile(e.target.files[0].name);

  }

}

