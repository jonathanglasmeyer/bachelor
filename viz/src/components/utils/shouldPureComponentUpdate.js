import shallowEqual from 'react/lib/shallowEqual';

export default function shouldPureComponentUpdate(nextProps, nextState) {
  return !shallowEqual(this.props, nextProps) ||
         !shallowEqual(this.state, nextState);
}
