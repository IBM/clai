import React from 'react';
import { Prompt } from 'react-router';
import { Redirect } from 'react-router-dom';
import { checkData } from './checkData';
import { checkEmail } from './checkData';
import {
  Loading,
  FormGroup,
  Tile,
  TextInput,
  Button,
  Link,
  Accordion,
  AccordionItem,
  Form,
  OrderedList,
  ListItem,
  Tag,
} from 'carbon-components-react';

import ExampleList from './ExampleList';
import UserInfo from './UserInfo';
import DataTemplate from './data/DataTemplate';

// const dbapi = "http://0.0.0.0:3456"
const dbapi = 'http://nlc2cmd-storage.mybluemix.net';

class ChallengePage extends React.Component {
  constructor() {
    super();

    var newState = JSON.parse(JSON.stringify(DataTemplate));
    this.elem_template = {
      commands: [''],
      descriptions: [''],
    };

    var id = this.__getRandomID();
    var template = this.elem_template;

    [1, 2, 3, 4, 5].forEach(function(item, key) {
      id = id + item;
      console.log(id);
      newState = {
        ...newState,
        data: {
          ...newState.data,
          [id]: JSON.parse(JSON.stringify(template)),
        },
      };
    });

    this.state = {
      ...newState,
      oldData: null,
      data: newState.data,
    };
  }

  componentDidMount = e => {
    fetch('{}/get_numbers'.replace('{}', dbapi))
      .then(result => result.json())
      .then(data => {
        this.setState({
          ...this.state,
          total_numbers: data['number_of_challenges'],
          idx_numbers: data['number_of_challengers'],
          max_numbers: data['number_of_lead'],
        });
      })
      .catch(console.log);
  };

  submitForm = e => {
    if (this.state.loaded) {
      this.setState(
        {
          ...this.state,
          load_status: null,
          checks: {
            ...this.state.checks,
            waitForSubmit: true,
          },
        },
        this.finishSubmission
      );
    } else {
      fetch('{}/get_past_data'.replace('{}', dbapi), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: this.state.info.email, flag: true }),
      })
        .then(result => result.json())
        .then(data => {
          if (data['success'] && !this.state.loaded) {
            this.setState(
              {
                ...this.state,
                load_status: null,
                oldData: data['info']['data']['data'],
                checks: {
                  ...this.state.checks,
                  waitForSubmit: true,
                },
              },
              this.finishSubmission
            );
          } else {
            this.setState(
              {
                ...this.state,
                load_status: null,
                checks: {
                  ...this.state.checks,
                  waitForSubmit: true,
                },
              },
              this.finishSubmission
            );
          }
        })
        .catch(console.log);
    }
  };

  finishSubmission = e => {
    const status = checkData(this.state);
    // console.log(status);

    var date_object = new Date();
    var current_time = date_object.getTime();

    this.setState(
      {
        ...this.state,
        time: current_time,
        checks: {
          ...this.state.checks,
          waitForSubmit: false,
          errorDetails: {
            ...this.state.checks.errorDetails,
            errorMessage: status.info,
            errorStatus: !status.success,
            errorItem: status.item,
          },
        },
      },
      this.gotoDone
    );
  };

  gotoDone = e => {
    // console.log('logging current data', this.state);

    if (!this.state.checks.errorDetails.errorStatus) {
      fetch('{}/new_submission'.replace('{}', dbapi), {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data: this.state,
        }),
      })
        .then(result => result.json())
        .then(data => {
          if (data['success'])
            this.setState({
              ...this.state,
              checks: {
                ...this.state.checks,
                checked: true,
              },
            });
        })
        .catch(data => {
          this.setState({
            ...this.state,
            checks: {
              ...this.state.checks,
              waitForSubmit: false,
              errorDetails: {
                ...this.state.checks.errorDetails,
                errorMessage: 'Could not submit data :(',
                errorStatus: true,
                errorItem: null,
              },
            },
          });
        });
    }
  };

  loadData = e => {
    const statusCheckEmail = checkEmail(this.state.info.email);
    const enteredKey = document.getElementById('email-key-input').value;

    // console.log(statusCheckEmail);

    if (statusCheckEmail.success && enteredKey) {
      fetch('{}/get_past_data'.replace('{}', dbapi), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.state.info.email,
          key: enteredKey,
          flag: false,
        }),
      })
        .then(result => result.json())
        .then(data => {
          if (data['success']) {
            // console.log('logging loaded data', data['info']['data']);

            this.setState({
              ...this.state,
              load_status: null,
              loaded: true,
              info: data['info']['data']['info'],
              data: data['info']['data']['data'],
            });
          } else {
            this.setState({
              ...this.state,
              load_status: data['info'],
            });
          }
        })
        .catch(console.log);
    } else {
      if (!enteredKey) {
        this.setState({
          ...this.state,
          load_status: 'Please enter your key to load previous data.',
        });
      } else {
        this.setState({
          ...this.state,
          load_status: statusCheckEmail.info,
        });
      }
    }
  };

  // feedback from user info //

  logAgreement = (status, id) => {
    this.setState({
      ...this.state,
      checks: {
        ...this.state.checks,
        agreements: {
          ...this.state.checks.agreements,
          [id]: {
            ...this.state.checks.agreements[id],
            value: status,
          },
        },
      },
    });
  };

  logInput = (id, value) => {
    this.setState({
      ...this.state,
      info: {
        ...this.state.info,
        [id]: value,
      },
    });
  };

  logSelection = (id, value) => {
    this.logInput(id, value);
  };

  logMultiSelection = e => {
    this.setState({
      ...this.state,
      info: {
        ...this.state.info,
        stuff: e,
      },
    });
  };

  // feedback from examples //

  __getRandomID = e => {
    var date_object = new Date();
    var current_time = date_object.getTime();

    return current_time;
  };

  handleAddElement = e => {
    const new_example_id = this.__getRandomID();
    const newState = {
      ...this.state,
      data: {
        ...this.state.data,
        [new_example_id]: JSON.parse(JSON.stringify(this.elem_template)),
      },
    };

    this.setState(newState);
  };

  handleDeleteElement = id => {
    const tempDict = { ...this.state.data };
    delete tempDict[parseInt(id)];

    const newState = {
      ...this.state,
      data: tempDict,
    };

    this.setState(newState);
  };

  handleAddAlternative = id => {
    const newState = {
      ...this.state,
      data: {
        ...this.state.data,
        [id]: {
          ...this.state.data[id],
          commands: this.state.data[id].commands.concat(''),
        },
      },
    };

    this.setState(newState);
  };

  handleAddDescription = id => {
    const newState = {
      ...this.state,
      data: {
        ...this.state.data,
        [id]: {
          ...this.state.data[id],
          descriptions: this.state.data[id].descriptions.concat(''),
        },
      },
    };

    this.setState(newState);
  };

  handleInputChange = (id, value, example_id) => {
    const input = id.split('-');
    const temp = this.state.data[example_id][input[1]];
    temp[parseInt(input[0])] = value;

    const newState = {
      ...this.state,
      data: {
        ...this.state.data,
        [example_id]: {
          ...this.state.data[example_id],
          [input[1]]: temp,
        },
      },
    };

    this.setState(newState);
  };

  deleteExampleItem = (id, example_id) => {
    const input = id.split('-');
    const temp = this.state.data[example_id][input[1]];
    temp.splice(parseInt(input[0]), 1);

    const newState = {
      ...this.state,
      data: {
        ...this.state.data,
        [example_id]: {
          ...this.state.data[example_id],
          [input[1]]: temp,
        },
      },
    };

    this.setState(newState);
  };

  render() {
    return (
      <div className="challenge-page-body">
        {!this.state.checks.errorDetails.errorStatus &&
          this.state.checks.checked && (
            <Redirect
              to={{
                pathname: '/done',
                state: { key: this.state.time },
              }}
            />
          )}
        <Prompt
          when={Object.entries(this.state.data).length > 1}
          message={location =>
            `Are you sure you want to leave the page? Unsaved changes will be lost.`
          }
        />
        <div className="bx--grid bx--grid--full-width landing-page challenge-page">
          <div
            className="bx--row landing-page__banner challenge-page__banner"
            style={{ paddingBottom: '2rem' }}>
            <div className="bx--col-lg-16">
              <h1 className="landing-page__heading challenge-page__heading">
                Challenge the Participants!
              </h1>
              <p className="challenge-page__heading challenge-page__subheading">
                Provide your favorite NLC2CMD examples and find out how well the
                participants can do on them.
              </p>

              <br />

              {this.state.total_numbers && (
                <p
                  className="disclaimer"
                  style={{ color: 'rgb(167, 240, 186)' }}>
                  <Tag type="green" title="Data">
                    {this.state.total_numbers}
                  </Tag>{' '}
                  Total Number of Challenges
                </p>
              )}
              {this.state.max_numbers && (
                <p
                  className="disclaimer"
                  style={{ color: 'rgb(255, 214, 232)' }}>
                  <Tag type="magenta" title="Data">
                    {this.state.max_numbers}
                  </Tag>{' '}
                  Max Challenges from a Challenger
                </p>
              )}
              {this.state.idx_numbers && (
                <p
                  className="disclaimer"
                  style={{ color: 'rgb(232, 218, 255)' }}>
                  <Tag type="purple" title="Data">
                    {this.state.idx_numbers}
                  </Tag>{' '}
                  Total Number of Challengers
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="bx--grid bx--grid--full-width">
          <br />
          <br />
          <Accordion>
            <AccordionItem open title="Rules of the Game">
              <div className="bx--grid bx--grid--full-width">
                <OrderedList>
                  <ListItem>
                    <strong>The NLC2CMD Challenge. </strong>
                    The NLC2CMD Competition revolves around a simple use case:
                    translating English descriptions of command line tasks to
                    their correct Bash syntax. One example has been filled out
                    for you below. In the NLC2CMD Challenge you can challenge
                    the participants with your own examples of English to Bash
                    translations.
                  </ListItem>
                  <ListItem>
                    <strong>What commands are allowed?</strong>
                    <OrderedList nested>
                      <ListItem>
                        You can provide at most 5 examples from the same Bash
                        utility in each try. Examples cannot be more than 240
                        chars in length.
                      </ListItem>
                      <ListItem>
                        Commands must be valid in Unix Bash. The set of allowed
                        commands are available{' '}
                        <Link
                          href="http://manpages.ubuntu.com/manpages/bionic/en/man1/"
                          target="_blank">
                          here
                        </Link>
                        .
                      </ListItem>
                    </OrderedList>
                  </ListItem>
                  <ListItem>
                    <strong>Folder and file naming convention. </strong>
                    Folder names in your examples must be escaped with{' '}
                    <span>`/`</span>. Both folder and file names must be in
                    "double quotes". One example has been filled out for you.
                  </ListItem>
                  <ListItem>
                    <strong>You can submit multiple times. </strong>
                    Your entries will be aggregated under your email id.
                  </ListItem>
                  <ListItem>
                    <strong>The NLC2CMD Challenge raffle. </strong>
                    The raffle for top 10 contributors is closed now but please
                    consider contributing to the dataset and help push the state
                    of the art in English to Bash translation.
                  </ListItem>
                </OrderedList>
              </div>
            </AccordionItem>
          </Accordion>

          <Form className="data-form">
            <UserInfo
              state={this.state}
              logInput={this.logInput.bind(this)}
              logSelection={this.logSelection.bind(this)}
              logMultiSelection={this.logMultiSelection.bind(this)}
              loadData={this.loadData.bind(this)}
            />

            <FormGroup legendText="">
              <Tile
                light
                className="tile-props"
                style={{ marginBottom: '5px' }}>
                Example 0
                <br />
                <br />
                <div className="bx--col-lg-10">
                  <p className="disclaimer">
                    Each example describes a task that can be achieved on the
                    command line. On the left you provide examples of command
                    line invocations that achieve the <strong>same</strong>{' '}
                    task. On the right you say how you can invoke that command
                    in English.
                  </p>
                </div>
                <br />
                <div className="bx--row">
                  {['commands', 'descriptions'].map(item => {
                    return (
                      <div
                        className="bx--col-lg-6"
                        key={'dummy-' + item + '-main'}>
                        {Object.entries(this.state.data[0][item]).map(
                          (example, idx) => {
                            return (
                              <div
                                key={'dummy-' + item + '-' + idx.toString()}
                                className="bx--col-lg-16 gap-above">
                                <div className="bx--row">
                                  <TextInput
                                    labelText=""
                                    id={'dummy-' + item + '-' + idx.toString()}
                                    placeholder={example[1]}
                                    disabled
                                  />
                                </div>
                              </div>
                            );
                          }
                        )}
                      </div>
                    );
                  })}
                  <div className="bx--col-lg-4">
                    <p className="disclaimer">
                      <strong>Instructions. </strong>
                      This is an example. Do not duplicate this in your
                      examples.
                    </p>
                  </div>
                </div>
              </Tile>
            </FormGroup>
            <ExampleList
              state={this.state}
              handleDeleteElement={this.handleDeleteElement.bind(this)}
              handleAddAlternative={this.handleAddAlternative.bind(this)}
              handleAddDescription={this.handleAddDescription.bind(this)}
              deleteExampleItem={this.deleteExampleItem.bind(this)}
              handleInputChange={this.handleInputChange.bind(this)}
              handleAddElement={this.handleAddElement.bind(this)}
            />
          </Form>

          {this.state.checks.errorDetails.errorStatus && (
            <p className="disclaimer gap-below" style={{ color: 'red' }}>
              {this.state.checks.errorDetails.errorMessage}
            </p>
          )}
          <div>
            <Button
              size="field"
              kind="primary"
              type="button"
              onClick={this.submitForm.bind(this)}>
              Submit
            </Button>

            <p className="disclaimer gap-above">
              This will automatically check your submission against any previous
              examples you may have provided. The page will redirect at
              successful submission.
            </p>
          </div>
          {this.state.checks.waitForSubmit && (
            <Loading
              description="Active loading indicator"
              withOverlay={this.state.checks.waitForSubmit}
            />
          )}
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
        </div>
      </div>
    );
  }
}

export default ChallengePage;
