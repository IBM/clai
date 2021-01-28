const DataTemplate = {
  time: null,
  total_numbers: null,
  idx_numbers: null,
  max_numbers: null,
  load_status: null,
  loaded: false,
  info: {
    name: '',
    email: '',
    affiliation: '',
    occupation: '',
    stuff: [],
  },
  data: {
    0: {
      commands: [
        'grep -r "clai" "./" | grep ".py"',
        'find "./" -type f -name "*.py" -exec grep -r "clai" {} \\;',
      ],
      descriptions: [
        'find all python files in the current directory with "clai" in it',
        'find all ".py" files in "./" with the string "clai"',
        'grep for all ".py" files with the word "clai" in the current directory',
      ],
      disabled: true,
    },
  },
  template: {
    0: {
      commands: [],
      descriptions: [],
      disabled: false,
    },
  },
  checks: {
    checked: false,
    waitForSubmit: false,
    errorDetails: {
      errorMessage: null,
      errorStatus: false,
      errorItem: null,
    },
    agreements: {
      checked_forfeit: {
        value: false,
        text:
          'By providing examples I forfeit the right to participate in the NLC2CMD competition.',
      },
      checked_confidentiality: {
        value: false,
        text: 'I shall not reveal my examples to any participant.',
      },
      checked_terms: {
        value: false,
        text: 'I have read the Terms and Conditions.',
      },
      checked_raffle: {
        value: true,
        text: '(optional) I want to enter the Challenge raffle.',
      },
    },
  },
};

export default DataTemplate;
