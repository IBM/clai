// check data before submitting
import DataTemplate from './data/DataTemplate';
import UserCommands from './data/UserCommands';
import SOData from './data/SOData';

export function checkData(data) {
  var tempData = data.oldData;
  var newData = data.data;

  if (tempData) {
    Object.keys(newData).forEach(function(key) {
      tempData[key] = newData[key];
    });

    data = {
      ...data,
      data: tempData,
    };
  }

  const statusCheckName = checkName(data.info.name);
  if (!statusCheckName.success) return statusCheckName;

  const statusCheckEmail = checkEmail(data.info.email);
  if (!statusCheckEmail.success) return statusCheckEmail;

  const statusForceOccupation = forceOccupation(data.info.occupation);
  if (!statusForceOccupation.success) return statusForceOccupation;

  const statusEmptyExamples = emptyExamples(data.data);
  if (!statusEmptyExamples.success) return statusEmptyExamples;

  const statusAtLeastOneExample = atLeastOneExample(data.data);
  if (!statusAtLeastOneExample.success) return statusAtLeastOneExample;

  const dataList = _computeListOfCommandsAndDescriptions(data.data);
  const commands = dataList[0];
  const descriptions = dataList[1];

  const statusNoDuplicatesInNewExamples = noDuplicatesInNewExamples(
    commands,
    descriptions
  );

  if (!statusNoDuplicatesInNewExamples.success)
    return statusNoDuplicatesInNewExamples;

  const statusNoDuplicatesFromData = noDuplicatesFromData(data.data);
  if (!statusNoDuplicatesFromData.success) return statusNoDuplicatesFromData;

  const statusLegitCommands = legitCommands(data.data);
  if (!statusLegitCommands.success) return statusLegitCommands;

  const statusDiverseCommands = diverseCommands(data.data);
  if (!statusDiverseCommands.success) return statusDiverseCommands;

  const statusCharLimit = charLimit(data.data);
  if (!statusCharLimit.success) return statusCharLimit;

  return { success: true, info: '' };
}

///////////////////////////////////////////
// This function makes sure there is a name
///////////////////////////////////////////

export function checkName(name) {
  if (!name)
    return {
      success: false,
      info: 'Please enter your name.',
      item: 'name',
    };
  else return { success: true, info: '' };
}

//////////////////////////////////////////////////////
// This function does a soft check on the email format
//////////////////////////////////////////////////////

export function checkEmail(email) {
  const re = /\S+@\S+\.\S+/;
  const validate = re.test(email);

  if (!validate)
    return {
      success: false,
      info: 'Please enter a valid email address.',
      item: 'email',
    };
  else return { success: true, info: '' };
}

/////////////////////////////////////////////////////
// This function makes the occupation entry mandatory
/////////////////////////////////////////////////////

function forceOccupation(occupation) {
  if (!occupation || occupation === 'Choose an option')
    return { success: false, info: 'Please enter your occupation.' };
  else return { success: true, info: '' };
}

//////////////////////////////////////////////////////////////////
// This function makes sure that there is at least one new example
//////////////////////////////////////////////////////////////////

function atLeastOneExample(data) {
  if (JSON.stringify(data) === JSON.stringify(DataTemplate.data))
    return { success: false, info: 'Please enter at least one new example.' };
  else return { success: true, info: '' };
}

////////////////////////////////////////////////////////////////////////////
// This function checks for empty examples i.e. no description or no command
////////////////////////////////////////////////////////////////////////////

function emptyExamples(data) {
  const checkEmptyExamples = function(data) {
    var status = true;
    var error_item = {
      example_id: null,
      example_item_type: null,
      example_item_id: null,
    };

    Object.keys(data).forEach(function(key) {
      if (
        data[key].commands.length === 0 ||
        data[key].descriptions.length === 0
      ) {
        status = false;
        return status;
      }

      ['commands', 'descriptions'].forEach(function(array) {
        data[key][array].forEach(function(item, i) {
          if (!item) {
            error_item.example_id = key;
            error_item.example_item_type = array;
            error_item.example_item_id = i;

            status = false;
            return status;
          }
        });

        if (!status) return status;
      });

      if (!status) return status;
    });

    return [status, error_item];
  };

  const check = checkEmptyExamples(data);

  if (!check[0])
    return {
      success: false,
      info:
        'You cannot have empty ' +
        check[1].example_item_type +
        ' in an example.',
      item: check[1],
    };
  else return { success: true, info: '' };
}

///////////////////////////////////////////////////////////
// This function makes sure there are no duplicate examples
///////////////////////////////////////////////////////////

function noDuplicatesInNewExamples(commands, descriptions) {
  const checkNoDuplicatesInNewExamples = function(list) {
    var status = true;
    var example = null;

    list.forEach(function(item) {
      const check_list = list.filter(i => i === item);

      if (check_list.length > 1) {
        example = item;
        status = false;

        return status;
      }
    });

    return [status, example];
  };

  var response = { success: true, info: '' };

  [commands, descriptions].forEach(function(item) {
    const check = checkNoDuplicatesInNewExamples(item);

    if (!check[0]) {
      response.success = false;
      response.info = 'Duplicate entry: ' + check[1];

      return false;
    }
  });

  return response;
}

/////////////////////////////////////////////////////////////////////////////
// This function makes sure there is no copied examples from the NL2Bash data
// Examples that extend a copy with more examples is fine
/////////////////////////////////////////////////////////

function noDuplicatesFromData(data) {
  const checkNoDuplicatesFromData = function(data) {
    var status = true;
    var example = null;
    var error_item = {
      example_id: null,
      example_item_type: null,
      example_item_id: null,
    };

    Object.keys(data).forEach(function(key) {
      if (
        data[key].commands.length === 1 &&
        data[key].descriptions.length === 1
      ) {
        Object.keys(SOData).forEach(function(id) {
          if (
            SOData[id]['cmd'] === data[key].commands[0] &&
            SOData[id]['invocation'] === data[key].descriptions[0]
          ) {
            status = false;
            example = data[key].commands[0];

            error_item.example_id = key;
            error_item.example_item_type = 'commands';
            error_item.example_item_id = 0;

            return status;
          }
        });

        if (!status) return status;
      }
    });

    return [status, example, error_item];
  };

  const check = checkNoDuplicatesFromData(data);

  if (!check[0])
    return {
      success: false,
      info: 'Duplicate entry from NL2Bash data: ' + check[1],
      item: check[2],
    };
  else return { success: true, info: '' };
}

//////////////////////////////////////////////////////////////////////////////
// This function makes sure all commands are from the stipulated man page list
//////////////////////////////////////////////////////////////////////////////

function legitCommands(data) {
  const checkLegitCommands = function(data) {
    var status = true;
    var example = null;
    var error_item = {
      example_id: null,
      example_item_type: null,
      example_item_id: null,
    };

    Object.keys(data).forEach(function(key) {
      data[key].commands.forEach(function(command, idx) {
        var response = _find_utility(command);

        if (!response[0]) {
          status = false;
          example = command;

          error_item.example_id = key;
          error_item.example_item_type = 'commands';
          error_item.example_item_id = idx;

          return status;
        }
      });

      if (!status) return status;
    });

    return [status, example, error_item];
  };

  const check = checkLegitCommands(data);

  if (!check[0])
    return {
      success: false,
      info:
        check[1] +
        ' is not a valid utility. Refer: http://manpages.ubuntu.com/manpages/bionic/en/man1/',
      item: check[2],
    };
  else return { success: true, info: '' };
}

/////////////////////////////////////////////////////////////////////////////////
// This function enforces than not more than N commands are from the same utility
/////////////////////////////////////////////////////////////////////////////////

function diverseCommands(data) {
  const _max_limit = 5;

  var cacheData = JSON.parse(JSON.stringify(data));
  delete cacheData[0];

  const checkDiverseCommands = function(data) {
    var status = true;
    var example = null;
    var cache = {};

    Object.keys(data).forEach(function(key) {
      var utilities_in_this_example = [];

      data[key].commands.forEach(function(command) {
        var response = _find_utility(command);

        if (
          response[0] &&
          utilities_in_this_example.indexOf(response[1]) === -1
        ) {
          utilities_in_this_example.push.apply(utilities_in_this_example, [
            response[1],
          ]);
        }
      });

      utilities_in_this_example.forEach(function(utility) {
        if (!(utility in cache)) cache[utility] = 1;
        else cache[utility] += 1;

        if (cache[utility] > _max_limit) {
          example = utility;
          status = false;

          return status;
        }
      });

      if (!status) return status;
    });

    return [status, example];
  };

  const check = checkDiverseCommands(cacheData);

  if (!check[0])
    return {
      success: false,
      info:
        'Too many examples with ' +
        check[1] +
        '. You are allowed a maximum of ' +
        _max_limit +
        '.',
    };
  else return { success: true, info: '' };
}

//////////////////////////////////////////////////////////
// This function makes sure all the agreements are checked
//////////////////////////////////////////////////////////

function agreementChecked(agreement) {
  const checkAgreement = function(agreement) {
    var status = true;
    Object.keys(agreement).forEach(function(key) {
      if (!agreement[key].value && key !== 'checked_raffle') {
        status = false;
        return status;
      }
    });

    return status;
  };

  if (!checkAgreement(agreement))
    return {
      success: false,
      info:
        'You have to agree with the rules of the challenge before submitting.',
    };
  else return { success: true, info: '' };
}

//////////////////////////////////////////////////////////////////////////////
// This function limits the number of characters in commmands and descriptions
//////////////////////////////////////////////////////////////////////////////

function charLimit(data) {
  const _char_limit = 280;
  var error_item = {
    example_id: null,
    example_item_type: null,
    example_item_id: null,
  };

  const checkCharLimit = function(data) {
    var status = true;
    Object.keys(data).forEach(function(key) {
      ['commands', 'descriptions'].forEach(function(array) {
        data[key][array].forEach(function(item, idx) {
          if (item.length > _char_limit) {
            status = false;

            error_item.example_id = key;
            error_item.example_item_type = array;
            error_item.example_item_id = idx;

            return status;
          }
        });

        if (!status) return status;
      });

      if (!status) return status;
    });

    return [status, error_item];
  };

  const check = checkCharLimit(data);

  if (!check[0])
    return {
      success: false,
      info:
        _toUpper(check[1].example_item_type) +
        ' cannot be larger than a tweet! (280 chars)',
      item: check[1],
    };
  else return { success: true, info: '' };
}

/////////////////////////////////////////////////////////
//////////////////// HELPER METHODS /////////////////////
/////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////
// Helper method to find which utility a command is about
/////////////////////////////////////////////////////////

function _find_utility(command) {
  var utility_found = false;
  var found_utility = null;

  UserCommands.forEach(function(utility) {
    utility = utility.replace(/-/g, ' ');

    if (command.startsWith(utility + ' ') || command === utility) {
      found_utility = utility;
      utility_found = true;

      return utility_found;
    }
  });

  return [utility_found, found_utility];
}

//////////////////////////////////////////////////////////////////////////
// Helper method to compute list of commands and descriptions from payload
//////////////////////////////////////////////////////////////////////////

function _computeListOfCommandsAndDescriptions(data) {
  var commandList = [];
  var descriptionList = [];

  var cacheData = JSON.parse(JSON.stringify(data));
  delete cacheData[0];

  Object.keys(cacheData).forEach(function(key) {
    data[key].commands.forEach(function(item) {
      if (item) commandList.push(item);
    });

    data[key].descriptions.forEach(function(item) {
      if (item) commandList.push(item);
    });
  });

  return [commandList, descriptionList];
}

/////////////////////////////////////
// Helper method to capitalize a word
/////////////////////////////////////

function _toUpper(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
