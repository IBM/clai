# [NLC2CMD Challenge](http://ibm.biz/nlc2cmd) @ [NeurIPS 2020](https://neurips.cc/Conferences/2020/CompetitionTrack)


The NLC2CMD Competition brings the power of natural language processing to the command line. You are tasked with building models that can transform descriptions of command line tasks in English to their Bash syntax.

## Getting started

- [`Home`](http://ibm.biz/nlc2cmd) - Link to competition homepage
- [`EvalAI Home`](https://evalai.cloudcv.org/web/challenges/challenge-page/674/overview) - Link to EvalAI homepage
- [`Submission Starter Kit`](./submission-code) - Starter kit for EvalAI submission
- [`Tellina baseline`](./tellina-baseline) - Tellina baseline code
- [`Slack`](http://ibm.biz/clai-slack) - Discussion forum for the challenge


## Updates

- **August  3, 2020** - In the `nl2bash` data provided ([Link](./docs/nl2bash-data.md)), we identified some examples which either had syntactic issues or bash parser incompatibility, resulting in an incorrect metric computation. We've fixed this issue and have updated the dataset. Please update your local copy of the `nl2bash` dataset ([Link](./docs/nl2bash-data.md)) and also update your local copy of `submission-code` folder with the one available in this branch.
