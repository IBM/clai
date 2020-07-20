# [NLC2CMD Challenge](http://nlc2cmd.us-east.mybluemix.net/) @ [NeurIPS 2020](https://neurips.cc/Conferences/2020/CompetitionTrack)

This folder contains the starter code for the NLC2CMD challenge that participants should use to wrap their methods into and submit for evaluation.


### Contents

- [Submission instructions](#submission-instructions)
- [Evaluation setup](#evaluation-setup)
- [Citing CLAI](#citing-clai)
- [Contact us](#contact-us)


-----------------------------------------------------------------------------


## Submission instructions

#### A) Install prerequisites on your development system
- Install [Python 3](https://www.python.org/downloads/). 
    - Note: We use `Python3` throughout the competition and the corresponding utilities such as `pip`. We've tested the code on `Python 3.7` specifically.
- Install [Docker](https://docs.docker.com/engine/install/)
- Create your team and register to participate on the [EvalAI Challenge page](https://evalai.cloudcv.org/web/challenges/challenge-page/{{CNUM}}/overview)
- Install [EvalAI CLI](https://evalai-cli.cloudcv.org/) using `pip install evalai`
- Retrieve your EvalAI token from the EvalAI website and set it using `evalai set_token <token>`

---

#### B) Integrate your source code to the submission

- Participants source code resides independently of the challenge code in the [`src/submission_code/`](src/submission_code/) folder.
The `submission_code` folder contains two files: 1) [`main.py`](src/submission_code/main.py), and 2) [`requirements.txt`](src/submission_code/requirements.txt).

- The `main.py` file implements a `predict` function that serves as an interface to the evaluation script. The `predict` function
accepts a list (batch) of natural language invocations `invocations` and the number of predictions expected for each invocation, 
and returns an array of predicted commands along with a confidence score for each predicted command.

The function definition for the `predict` function is:

```python
def predict(invocations, result_cnt=5):
  """ 
  Function called by the evaluation script to interface the participants model

  Args:
    1. invocations : `list (str)` : list of `n_batch` (default 16) natural language invocations
    2. result_cnt : `int` : number of predicted commands to return for each invocation

  Returns:
    1. commands : `list [ list (str) ]` : a list of list of predicted commands of shape (n_batch, result_cnt)
    2. confidences: `list[ list (float) ]` : confidences corresponding to the predicted commands
                      confidence values should be between 0.0 and 1.0. 
                      Shape: (n_batch, result_cnt)
  """
```

Participants should integrate their methods in the `predict` functions [lines 34 - 37](src/submission_code/main.py#L34). 

- The [`requirements.txt`](src/submission_code/requirements.txt) file in the [`src/submission_code/`](src/submission_code/) folder
is used to install any dependencies for the participants code. Add any dependencies required for your code in this file and they
will be automatically installed in the docker image using `pip`.

---

#### C) Build your docker image

- Once you've integrated your code with the challenge code, build your docker image by executing the [`./BuildDockerImage.sh`](BuildDockerImage.sh) 
script. You can either provide a custom docker image tag, or can use the default tag `nlc2cmd-challenge`

---

#### D) Test your docker image locally

- Once you've successfully built the docker image, you can test it locally before submitting it to EvalAI. The `test_locally.py` file runs the evaluation procedure as it would be run for final evaluation. You can run the script with default parameters as `python test_locally.py`, or you can specify any of the following parameters explicity. 

```
optional arguments:
  --img IMG                                               Submission docker image name
  --annotation_filepath ANNOTATION_FILEPATH               Annotation filepath
  --params_filepath PARAMS_FILEPATH                       Parameters filepath
  --grammar_filepath GRAMMAR_FILEPATH                     Grammar filepath
  --log_folder LOG_FOLDER                                 Output log folder path
```

---

#### E) Submit the docker image to EvalAI

- Get the submission command from the EvalAI competitions `Submit` page.
  - The submission command would be of the form `evalai push <image>:<tag> --phase <phase_name>`
  - The default value of `<image>:<tag>` should be `nlc2cmd-challenge:latest`. You can verify this by executing `docker images` on your system.
  - The `phase_name` will be available from the EvalAI page.


## Evaluation setup
  - All submissions will be evaluated on a standard machine with the following configuration:
    ```
    8 core Intel(R) Xeon(R) CPU E5-2683 v4 @ 2.10GHz processors
    16Gb RAM
    ```
    
  - Please note that GPUs will **NOT** be available for evaluation. Thus, ensure that your code runs on CPU.
  - The submitted docker images will be evaluated with **NO** access to network. Thus, please ensure that your code does not require the internet or calls any REST API for inference.
  - All submissions (across participants) will be evaluated sequentially. This might cause some delay in your submission being picked for evaluation. We would suggest you create your own test set locally in the form as here [./configs/annotations/local_eval_annotations.json](./configs/annotations/local_eval_annotations.json), and testing it locally (as described above) if you require quick evaluation for development purposes.
  

## Citing CLAI

If you write a paper or a report about your submission to this competition, please cite:
```
@article{agarwal2020clai,
  title={CLAI: A Platform for AI Skills on the Command Line},
  author={Agarwal, Mayank and Barroso, Jorge J and Chakraborti, Tathagata and Dow, Eli M and Fadnis, Kshitij and Godoy, Borja and Talamadupula, Kartik},
  journal={arXiv preprint arXiv:2002.00762},
  year={2020}
}
```

Or refer to the CLAI master repo: [https://github.com/IBM/clai](https://github.com/IBM/clai)


## Contact Us
- Website: [http://nlc2cmd.us-east.mybluemix.net/](http://nlc2cmd.us-east.mybluemix.net/)
- Slack: [http://ibm.biz//clai-slack](http://ibm.biz//clai-slack) 
- Email: [nlc2cmd@gmail.com](mailto:nlc2cmd@gmail.com)
