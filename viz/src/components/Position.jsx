import React, {Component, PropTypes} from 'react';
import {secondsToTime} from '../utils/helpers.js';
import {Flux} from 'flummox';
import constants from '../constants.js';


export default class Position extends Component {

  static propTypes = {
    position: PropTypes.number,
  }

  static contextTypes = {
    flux: PropTypes.instanceOf(Flux)
  }

  render() {
    const {position, onPositionClick} = this.props;

    const {h, m, s} = secondsToTime(position/1000);
    const formattedTime = `${h}${m}${s}`;

    return <li>
      <span
        className='position'
        onClick={() => this._onPositionClick(position)}>

        {formattedTime}
      </span>
    </li>;
  }

  /**
   * position: in ms
   */
  _onPositionClick(position) {
    this.context.flux.getActions(constants.position).changePosition(position/1000);
  }

}
