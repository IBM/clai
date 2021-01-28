import React from 'react';
import { OccupationOptions, MultiSelectItems } from './SelectItems';
import {
  Button,
  Tile,
  FormGroup,
  TextInput,
  Select,
  SelectItem,
  MultiSelect,
} from 'carbon-components-react';

class UserInfo extends React.Component {
  constructor(props) {
    super();

    var tempState = props.state;
    tempState['selectedItems'] = [];
    tempState['selectedKey'] = 0;

    this.state = props.state;
  }

  componentWillReceiveProps(props) {
    var tempState = props.state;
    var tempSelections = [];

    MultiSelectItems.forEach(function(item) {
      if (tempState.info.stuff.indexOf(item.text) > -1) {
        tempSelections.push(item);
      }
    });

    tempState['selectedItems'] = tempSelections;
    tempState['selectedKey'] = this.state.selectedKey + 1;

    this.setState(tempState);
  }

  logInput = e => {
    this.props.logInput(e.target.id, e.target.value);
  };

  logSelection = e => {
    this.props.logSelection(e.target.id, e.target.selectedOptions[0].text);
  };

  logMultiSelection = e => {
    const selectedItems = Object.entries(e).map(
      (element, id) => element[1].text
    );
    this.props.logMultiSelection(selectedItems);
  };

  loadData = e => {
    this.props.loadData(e);
  };

  render() {
    return (
      <FormGroup legendText="">
        <Tile light className="tile-props">
          <TextInput
            id="name"
            labelText="Who am I (required)"
            placeholder="Please enter your name"
            value={this.state.info.name}
            onChange={this.logInput.bind(this)}
            ref={input => {
              this.textInput = input;
            }}
            invalidText={this.state.checks.errorDetails.errorMessage}
            invalid={
              this.state.checks.errorDetails.errorStatus &&
              this.state.checks.errorDetails.errorItem &&
              this.state.checks.errorDetails.errorItem === 'name'
            }
          />

          <br />

          <TextInput
            helperText="If you have submitted data before, you can use the same email to load your previous data below."
            id="email"
            labelText="Contact Email (required)"
            placeholder="Please enter your email"
            value={this.state.info.email}
            onChange={this.logInput.bind(this)}
            ref={input => {
              this.textInput = input;
            }}
            invalidText={this.state.checks.errorDetails.errorMessage}
            invalid={
              this.state.checks.errorDetails.errorStatus &&
              this.state.checks.errorDetails.errorItem &&
              this.state.checks.errorDetails.errorItem === 'email'
            }
          />

          <br />

          {this.state.load_status && (
            <p className="disclaimer gap-below" style={{ color: 'red' }}>
              {this.state.load_status}
            </p>
          )}

          <div className="bx--col-lg-16">
            <div className="bx--row">
              <Button
                style={{ marginRight: '10px' }}
                size="small"
                kind="secondary"
                type="button"
                onClick={this.loadData.bind(this)}>
                Load Previous Data
              </Button>

              <TextInput
                labelText=""
                id="email-key-input"
                className="email-key-input"
                ref={input => {
                  this.textInput = input;
                }}
                placeholder="Enter key to load old data"
              />
            </div>
          </div>

          <p className="disclaimer gap-above">
            This will overwrite unsubmitted examples (if any) below.
          </p>

          <br />
          <br />

          <TextInput
            id="affiliation"
            labelText="Affiliation"
            placeholder="Please enter your affiliation"
            value={this.state.info.affiliation}
            onChange={this.logInput.bind(this)}
            ref={input => {
              this.textInput = input;
            }}
            invalidText={this.state.checks.errorDetails.errorMessage}
            invalid={
              this.state.checks.errorDetails.errorStatus &&
              this.state.checks.errorDetails.errorItem &&
              this.state.checks.errorDetails.errorItem === 'affiliation'
            }
          />

          <br />

          <Select
            id="occupation"
            labelText="Choose an occupation that best describes you (required)"
            value={OccupationOptions[this.state.info.occupation]}
            onChange={this.logSelection}>
            {Object.keys(OccupationOptions).map((item, key) => {
              return (
                <SelectItem
                  text={item}
                  value={OccupationOptions[item]}
                  key={key}
                />
              );
            })}
          </Select>

          <br />

          <MultiSelect
            className="gap-below"
            ariaLabel="MultiSelect"
            id="stuff"
            key={this.state.selectedKey}
            initialSelectedItems={this.state.selectedItems}
            items={MultiSelectItems}
            itemToString={item => (item ? item.text : '')}
            label="Select one or more options"
            titleText="Which of these softwares, products, or services do you use a lot?"
            onChange={value => {
              this.logMultiSelection(value.selectedItems);
            }}
          />

          <p className="disclaimer">
            Data on occupation, affiliation, and usage will be used to compute
            differentiated distribution of data across different demographics.
            The aggregate data will be published after the compeitition is over.
          </p>
        </Tile>
      </FormGroup>
    );
  }
}

export default UserInfo;
