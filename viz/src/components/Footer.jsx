import React, {Component, PropTypes} from 'react';
import {dimension, color} from '../style/vars.js';

const styles = {
  position: 'fixed',
  bottom: 0,
  left: 0,
  right: 0,
  width: '100%',

  display: 'flex',
  alignItems: 'center',
  padding: '0 20px',

  zIndex: 9999,
  height: dimension.Navbar.height,
  backgroundColor: color.primary,

  boxShadow: '0 0 8px 2px rgba(0, 0, 0, 0.2)'
};

export default class Navbar extends Component {

  static propTypes = {
    children: PropTypes.element.isRequired
  }

  render() {

    return <footer style={styles}>
      {this.props.children}
    </footer>;

  }

}
