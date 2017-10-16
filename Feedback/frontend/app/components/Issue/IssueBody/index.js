import PropTypes from 'prop-types';
import React from 'react';
import ReactMarkdown from 'react-markdown';

class IssueBody extends React.Component {
  static propTypes = {
    body: PropTypes.string,
    className: PropTypes.string,
    editable: PropTypes.bool,
    onChange: PropTypes.func,
  };

  static defaultProps = {
    body: '',
    className: '',
    editable: false,
    onChange: (body) => {
    }
  };

  constructor(props) {
    super(props);

    this.enableEdit = this.enableEdit.bind(this);
    this.disableEdit = this.disableEdit.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
    this.onChange = this.onChange.bind(this);
    this.save = this.save.bind(this);
    this.cancel = this.cancel.bind(this);

    this.state = {
      body: props.body,
      editing: false,
    }
  }

  render() {
    if (this.state.editing == true) {
      const classes = `${this.props.className} issue__body--editing`;
      return (
        <div className={classes}>
          <div >
            <textarea defaultValue={this.state.body}
                      onChange={this.onChange}
                      onKeyDown={this.onKeyDown}>
            </textarea>
          </div>
          <div className="issue__body__button">
            <button onClick={this.save}>
              <i className="fa fa-check"></i> Save
            </button>
            <button onClick={this.disableEdit}>
              <i className="fa fa-times"></i> Cancel
            </button>
          </div>
        </div>
      )
    }

    return (
      <div className={this.props.className}>
        <div className="issue__body__content">
          <ReactMarkdown source={this.props.body}
                         disallowedTypes={['HtmlInline', 'HtmlBlock']}
                         escapeHtml={true} />
        </div>
        {this.renderEditButton()}
      </div>
    );
  }

  renderEditButton() {
    if (!this.props.editable) {
      return;
    }
    return (
      <div className="issue__body__button">
        <button onClick={this.enableEdit}>
          <i className="fa fa-pencil"></i> Edit
        </button>
      </div>
    )
  }

  enableEdit() {
    if (this.props.editable) {
      const newState = Object.assign(this.state, {editing: true});
      this.setState(newState);
    }
  }

  disableEdit() {
    const newState = Object.assign(this.state, {editing: false});
    this.setState(newState);
  }

  save() {
    if (this.props.editable) {
      this.props.onChange(this.state.body);
      this.disableEdit();
    }
  }

  cancel() {
    const newState = Object.assign(this.state, {
      editing: false,
      body: this.props.body,
    });

    this.setState(newState);
  }

  onKeyDown(event) {
    switch (event.key) {
      case 'Escape':
        this.disableEdit();
        break;
    }
  }

  onChange(event) {
    const newState = Object.assign(this.state, {body: event.target.value});
    this.setState(newState);
  }
}

export default IssueBody;