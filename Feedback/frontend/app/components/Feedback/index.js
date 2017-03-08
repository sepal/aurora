import React from 'react';
import styles from './style.scss';
import Modal from '../Modal';
import Kanban from '../Kanban';

export default class Feedback extends React.Component {
  constructor(props) {
    super(props);
    this.closeModal = this.closeModal.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    // if we changed routes...
    if (nextProps.location.key !== this.props.location.key
      && nextProps.location.state
      && nextProps.location.state.modal
    ) {
      // save the old children (just like animation)
      this.previousChildren = this.props.children
    }
  }

  render() {
    let {location} = this.props;
    const path = new RegExp(`^/${course_short_title}/feedback[/]*$`, 'i');
    let isModal = location.pathname.match(path) == null;
    return (
      <div>
        {isModal ?
          <Kanban /> :
          this.props.children
        }

        {isModal && (
          <Modal isOpen={true} returnTo={`/${course_short_title}/feedback`} router={this.props.router} onClose={this.closeModal}>
            {this.props.children}
          </Modal>
        )}
      </div>
    );
  }


  closeModal() {
    this.props.router.push(`/${course_short_title}/feedback`)
  }
}
