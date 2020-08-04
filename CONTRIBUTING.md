# Contributing to Project CLAI

Adding new features, improving documentation, fixing bugs, or writing tutorials are all examples of helpful contributions. 
Furthermore, if you are building a new skill, we strongly encourage you to add it to the 
[CLAI skill catalog](clai/server/plugins/) so that others may
also benefit from it as well as contribute to it and improve it.

Bug fixes can be initiated through GitHub pull requests or PRs. 
When making code contributions to Project CLAI, we ask that you follow the `PEP 8` coding standard 
and that you provide unit tests for the new features.

This project uses [DCO](https://developercertificate.org/). 
Be sure to sign off your commits using the `-s` flag or adding `Signed-off-By: Name<Email>` in the commit message.

### Example commit message
```bash
git commit -s -m 'Informative commit message'
```

### Unit tests

Whether you are contributing a new skill or updating the code elsewhere, you need to ensure that the unit tests pass. 

If you are developing a new skill, you can check in sample inputs and outputs in 
[here](./test_integration/) to make sure your skill runs as intended. 
See [here](./test_integration/test_skill_nlc2cmd.py) for an example test with the [`nlc2cmd`](clai/server/plugins/nlc2cmd) skill. 

Once all the tests have passed, and you are satisfied with your contribution, open a pull request into the `master` branch from **your fork of the repository** to request adding your contributions into the main code base.
