import React, {Component, PropTypes} from 'react';

export default class Svg extends Component {

  static propTypes = {

  }

  render() {
    return <svg {...this.props}>{this.props.children}</svg>;
  }

}
