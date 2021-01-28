import React from 'react';
import { Button, Tile, FormGroup, TextInput } from 'carbon-components-react';
import Delete16 from '@carbon/icons-react/lib/delete/16';

class ExampleList extends React.Component {
  constructor(props) {
    super();
    this.state = props.state;
  }

  componentWillReceiveProps(nextProps) {
    this.setState(nextProps.state);
  }

  handleDeleteElement = id => {
    this.props.handleDeleteElement(id);
  };

  handleAddAlternative = id => {
    this.props.handleAddAlternative(id);
  };

  handleAddDescription = id => {
    this.props.handleAddDescription(id);
  };

  deleteExampleItem = (id, example_id) => {
    this.props.deleteExampleItem(id, example_id);
  };

  handleInputChange = (id, value, example_id) => {
    this.props.handleInputChange(id, value, example_id);
  };

  render() {
    return (
      <div>
        <FormGroup legendText="">
          {Object.entries(this.state.data).map((example, idx) => {
            return (
              !example[1].disabled && (
                <ExampleElement
                  key={idx}
                  id={idx}
                  error={this.state.checks.errorDetails}
                  data={example}
                  handleDeleteElement={this.handleDeleteElement.bind(this)}
                  handleAddAlternative={this.handleAddAlternative.bind(this)}
                  handleAddDescription={this.handleAddDescription.bind(this)}
                  deleteExampleItem={this.deleteExampleItem.bind(this)}
                  handleInputChange={this.handleInputChange.bind(this)}
                />
              )
            );
          })}
        </FormGroup>

        <Button
          kind="ghost"
          size="field"
          onClick={this.props.handleAddElement.bind(this)}>
          + Add another example
        </Button>
        <br />
        <br />
      </div>
    );
  }
}

class ExampleElement extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      header: props.id,
      id: props.data[0],
      data: props.data[1],
      error: props.error,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      header: nextProps.id,
      id: nextProps.data[0],
      data: nextProps.data[1],
      error: nextProps.error,
    });
  }

  handleDeleteElement = id => {
    this.props.handleDeleteElement(id);
  };

  handleAddAlternative = id => {
    this.props.handleAddAlternative(id);
  };

  handleAddDescription = id => {
    this.props.handleAddDescription(id);
  };

  deleteExampleItem = id => {
    this.props.deleteExampleItem(id, this.state.id);
  };

  handleInputChange = (id, value) => {
    this.props.handleInputChange(id, value, this.state.id);
  };

  render() {
    return (
      <Tile light className="tile-props" style={{ marginBottom: '5px' }}>
        Example {this.state.header}
        <br />
        <br />
        <div className="bx--col-lg-10">
          <p className="disclaimer">
            Each example describes a task that can be achieved on the command
            line. On the left you provide examples of command line invocations
            that achieve the <strong>same</strong> task. On the right you say
            how you can invoke that command in English.
          </p>
        </div>
        <br />
        <div className="bx--row">
          <div className="bx--col-lg-6">
            <div>
              {this.state.data.commands.map((command, idx) => {
                return (
                  <InputExample
                    key={idx}
                    id={idx + '-commands'}
                    error={this.state.error}
                    parentID={this.state.id}
                    placeholder="Enter a Unix Bash command"
                    value={command}
                    deleteExampleItem={this.deleteExampleItem.bind(this)}
                    handleInputChange={this.handleInputChange.bind(this)}
                  />
                );
              })}
            </div>

            <Button
              kind="ghost"
              size="field"
              onClick={this.handleAddAlternative.bind(this, this.state.id)}>
              + Add a command
            </Button>
          </div>

          <div className="bx--col-lg-6">
            <div>
              {this.state.data.descriptions.map((description, idx) => {
                return (
                  <InputExample
                    key={idx}
                    id={idx + '-descriptions'}
                    error={this.state.error}
                    parentID={this.state.id}
                    placeholder="Enter an English description of your command"
                    value={description}
                    deleteExampleItem={this.deleteExampleItem.bind(this)}
                    handleInputChange={this.handleInputChange.bind(this)}
                  />
                );
              })}
            </div>

            <Button
              kind="ghost"
              size="field"
              onClick={this.handleAddDescription.bind(this, this.state.id)}>
              + Add a description
            </Button>
          </div>

          <div className="bx--col-lg-4">
            <p className="disclaimer">
              <strong>Instructions. </strong>
              You can add as many examples for your bash command(s) as you want.
              Try paraphrasing your descriptions to help the AI learn. You can
              also enter multiple Bash commands that do the same job you
              describe in English.
            </p>
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <Button
            kind="ghost"
            size="small"
            style={{ color: 'red' }}
            onClick={this.handleDeleteElement.bind(this, this.state.id)}>
            Delete
          </Button>
        </div>
      </Tile>
    );
  }
}

class InputExample extends React.Component {
  constructor(props) {
    super();
    this.state = {
      id: props.id,
      placeholder: props.placeholder,
      value: props.value,
      error: props.error,
      parentID: props.parentID,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      id: nextProps.id,
      placeholder: nextProps.placeholder,
      value: nextProps.value,
      error: nextProps.error,
      parentID: nextProps.parentID,
    });
  }

  handleInputChange = e => {
    this.setState({ value: this.textInput.value });
    this.props.handleInputChange(e, this.textInput.value);
  };

  deleteExampleItem = e => {
    this.props.deleteExampleItem(e);
  };

  render() {
    return (
      <div className="bx--col-lg-16 gap-above">
        <div className="bx--row">
          <TextInput
            labelText=""
            id={this.state.id}
            placeholder={this.state.placeholder}
            value={this.state.value}
            onChange={this.handleInputChange.bind(this, this.state.id)}
            ref={input => {
              this.textInput = input;
            }}
            invalidText={this.state.error.errorMessage}
            invalid={
              this.state.error.errorStatus &&
              this.state.error.errorItem &&
              this.state.error.example_item_id &&
              this.state.error.example_item_type &&
              this.state.error.example_id &&
              this.state.id ===
                this.state.error.errorItem.example_item_id.toString() +
                  '-' +
                  this.state.error.errorItem.example_item_type &&
              this.state.parentID ===
                this.state.error.errorItem.example_id.toString()
            }
          />

          <Button
            hasIconOnly
            iconDescription="Delete"
            kind="ghost"
            size="small"
            tabIndex={0}
            tooltipAlignment="center"
            tooltipPosition="bottom"
            type="button"
            style={{ color: 'grey' }}
            className="delete-item"
            onClick={this.deleteExampleItem.bind(this, this.state.id)}>
            <Delete16 />
          </Button>
        </div>
      </div>
    );
  }
}

export default ExampleList;
