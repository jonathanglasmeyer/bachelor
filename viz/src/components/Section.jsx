import React, {Component, PropTypes} from 'react';

import {dimension, color} from '../style/vars.js';



export default class Section extends Component {

  static propTypes = {
    minWidth: PropTypes.number,
    borderRight: PropTypes.bool
  }


  render() {
    const {minWidth, style} = this.props;

    const style_ = Object.assign(
        {padding: 16},
        style);

    return <section style={style_}>

      {this.props.children}
    </section>;
  }

}
