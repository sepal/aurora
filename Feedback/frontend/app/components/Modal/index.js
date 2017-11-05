import React from 'react';
import {Link, withRouter, Redirect} from 'react-router-dom';

class Modal extends React.Component {
  constructor(props) {
    super(props);

    this.close = this.close.bind(this);

    this.state = {
      closed: false,
    }
  }

  componentWillReceiveProps() {
    this.setState({
      closed: false
    });
  }

  render() {
    if (this.state.closed) {
      return (
        <Redirect to={`${base_path}`}/>
      )
    }

    if (this.onIndex()) {
      return (<div></div>);
    }

    return (
      <div className="modal" onClick={this.close}>
        <div className="modal__window" onClick={this.eventHandler}>
          <div className="modal__header">
            <Link to={this.props.returnTo}>
              <button className="modal__close">
                <i className="fa fa-times-circle"></i>
              </button>
            </Link>
          </div>
          <div>
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }

  close(event) {
    this.setState({
      closed: true
    });
  }

  eventHandler(event) {
    event.stopPropagation();
  }

  onIndex() {
    const pathPattern = new RegExp(`^(${base_path}?)$`, 'gi');
    return this.props.location.pathname.match(pathPattern);
  }
}

export default withRouter(props => <Modal {...props} />);