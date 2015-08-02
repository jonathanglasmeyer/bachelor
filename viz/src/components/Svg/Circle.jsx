import React, {Component, PropTypes} from 'react';
import {Flux} from 'flummox';
import constants from '../../constants.js';

export default class Circle extends Component {

  static contextTypes = {
    flux: PropTypes.instanceOf(Flux)
  }


  static propTypes = {
    onClick: PropTypes.func,
    color: PropTypes.string,
    radius: PropTypes.number,
    position: PropTypes.number,
    hover: PropTypes.bool
  }

  constructor(props) {
    super(props);
    this.state = {
      color: props.color
    };
  }


  render() {
    const {color, position, radius, onClick, hover} = this.props;


    return <circle
      {...this.props}
      onClick={this._handleClick.bind(this)}
      onMouseEnter={hover ? ()=>this.setState({color: 'rgba(0,0,0,.08)'}) : null}
      onMouseLeave={hover ? ()=>this.setState({color: 'rgba(0,0,0,.03)'}) : null}
      fill={this.state.color || '#333'}
      r={radius} >
    </circle>;
  }

  _handleClick() {
    this.context.flux.getActions(constants.audio).changePosition(this.props.position);
  }

}
