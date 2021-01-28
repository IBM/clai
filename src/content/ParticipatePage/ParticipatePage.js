import React from 'react';
import MathJax from 'react-mathjax-preview';
import { InfoAreaCompetition, Leaderboard } from '../../components/Info';
import {
  UnorderedList,
  ListItem,
  Link,
  StructuredListWrapper,
  StructuredListHead,
  StructuredListRow,
  StructuredListCell,
  StructuredListBody,
} from 'carbon-components-react';

import FaDownload16 from '@carbon/icons-react/lib/download/16';

const ParticipatePage = () => {
  return (
    <div className="bx--grid bx--grid--full-width landing-page">
      <InfoAreaCompetition />
      <Leaderboard />
      <br />
      <br />
      <StructuredListWrapper>
        <StructuredListBody>
          <StructuredListRow tabIndex={5}>
            <StructuredListCell>
              <span className="font-bold scroll-offset" id="task">
                Task
              </span>
            </StructuredListCell>
            <StructuredListCell>
              <MathJax
                math="The NLC2CMD Competition challenges you to build an algorithm that can translate
            an English description $(nlc)$ of a command line task to its corresponding command line syntax $(c)$.
            The input data looks as follows: $G(nlc) = \{~C~|~\text{Bash command that achieves task described in } nlc~\}$."
              />
              <br />
              <MathJax
                math="In most cases, you will only have one example translation, i.e. $|G(nlc)| = 1$.
            However, in general, there are many ways to achieve the same task."
              />
              <br />
              <MathJax
                math="Your algorithm $A$ models a top-5 translator as follows:"
                style={{ marginBottom: '10px' }}
              />
              <MathJax
                math="$A~:~nlc \mapsto \{~p~|~p = \langle c, \delta \rangle~\}; |A(nlc)| \leq 5$"
                style={{ marginBottom: '10px' }}
              />
              <MathJax
                math="where the ouput of $A$ is a set of atmost five tuples containing a Bash command
            $c$ that achieves the task described in the input $nlc$ with the associated confidence of the translation.
            By default, $\delta = 1$. The normalized score of a single prediction $p = \langle c, \delta \rangle \in A(nlc)$ is as follows:"
                style={{ marginBottom: '10px' }}
              />
              <MathJax
                math="$S(p) =  \max_{C \in G(nlc)} \sum_{i \in [1, T]} \frac{\delta}{T} \times \bigg( \mathbb{I}[ U(c)_i = U(C)_i ] \times \frac{1}{2} \Big(1 + \frac{1}{N} \big( 2 \times |F(U(c)_i) \cap F(U(C)_i)| - |F(U(c)_i) \cup F(U(C)_i)| \big) \Big) - \mathbb{I}[ U(c)_i \not= U(C)_i ] \bigg)$"
                style={{ marginBottom: '10px' }}
              />
              <MathJax
                math="where $U(c)$ is the sequence of Bash utilities in a command $c$ and F(u) is the set of flags for an utility $u$.
                $T = \max \big( |U(c)|, |U(C)| \big)$ and $N = \max \big( |F(U(c)_i)|, |F(U(C)_i)| \big)$.
                $\mathbb{I[\cdot]}$ is the indicator function. The overall score of the prediction is given by:"
                style={{ marginBottom: '10px' }}
              />
              <MathJax
                math="$Score(A(nlc)) =  \max_{p \in A(nlc)} S(p)$ if $\exists_{p \in A(nlc)}$ such that $S(p) > 0$; $Score(A(nlc)) =  \frac{1}{|A(nlc)|}\sum_{p \in A(nlc)} S(p)$ otherwise."
                style={{ marginBottom: '10px' }}
              />
              <span style={{ color: 'silver' }}>
                <em>Revised Oct 5, 2020.</em>
              </span>
              <br />
              <br />
              The scoring mechanism incentivizes precision and recall of the
              correct utitlity and its flags, weighted by the reported
              confidence (the score is attributed to the maximum score of the
              top-5 prediction). A few things to keep in mind:
              <div style={{ margin: '10px' }}>
                <UnorderedList>
                  <ListItem>
                    You get negative points if you translate to the wrong
                    utility.
                  </ListItem>
                  <ListItem>
                    There might be more than one command in the translation, for
                    example, in the case of pipes and exec flags. The are
                    evaluated in order. This means that:
                    <UnorderedList nested>
                      <ListItem>
                        For piped commands, you only get points if the
                        predictions are in the right slots.
                      </ListItem>
                      <ListItem>
                        For exec flags, you only get point if the followup comes
                        second.
                      </ListItem>
                    </UnorderedList>
                  </ListItem>
                  <ListItem>
                    The flags detected are scored as a fraction of total number
                    of flags in the ground truth to account for variations of
                    command complexity. You get penalized for suggesting
                    redundant flags. You get zero points for a rightly predicted
                    utility with all wrong flags.
                  </ListItem>
                  <ListItem>
                    You do not need to populate the parameters for a flag
                    correctly for points.
                  </ListItem>
                  <ListItem>
                    You can find a few detailed examples{' '}
                    <Link
                      href="https://github.com/IBM/clai/blob/nlc2cmd/utils/metric/README.md"
                      target="_blank">
                      here
                    </Link>
                    .
                  </ListItem>
                </UnorderedList>
              </div>
            </StructuredListCell>
          </StructuredListRow>

          <StructuredListRow tabIndex={6}>
            <StructuredListCell>
              <span className="font-bold scroll-offset" id="prizes">
                Prizes
              </span>
            </StructuredListCell>

            <StructuredListWrapper style={{ marginBottom: '0' }}>
              <StructuredListHead>
                <StructuredListRow tabIndex={61}>
                  <StructuredListCell>
                    <span className="scroll-offset" id="prizes-accuracy">
                      <strong>Accuracy</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    The top two teams with the highest scores will win a grand
                    prize of 2500 USD each in the Accuracy Track. The prize pot
                    will be divided among respective teams if more than two
                    teams are tied on score. The team with the highest score
                    will also be invited to replace{' '}
                    <Link
                      href="https://github.com/IBM/clai/tree/master/clai/server/plugins/tellina"
                      target="_blank">
                      tellina in the CLAI skill catalog
                    </Link>{' '}
                    as the new state of the art of the NLC2CMD paradigm.
                  </StructuredListCell>
                </StructuredListRow>

                <StructuredListRow
                  tabIndex={61}
                  className="suppress-border-bottom">
                  <StructuredListCell>
                    <span className="scroll-offset" id="prizes-efficiency">
                      <strong>Efficiency</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    Top-5 scoring teams will also be judged on the efficiency of
                    their solution in terms of the energy consumed. The most
                    efficient team will win a grand prize of 2000 USD in the
                    Efficiency Track. It is possible for the same team to win in
                    both tracks.
                  </StructuredListCell>
                </StructuredListRow>
              </StructuredListHead>
            </StructuredListWrapper>
          </StructuredListRow>

          <StructuredListRow tabIndex={2}>
            <StructuredListCell>
              <span className="font-bold scroll-offset" id="data">
                Data
              </span>
            </StructuredListCell>

            <StructuredListWrapper style={{ marginBottom: '0' }}>
              <StructuredListHead>
                <StructuredListRow tabIndex={21}>
                  <StructuredListCell>
                    <span className="scroll-offset" id="data-stack-overflow">
                      <strong>Stack Overflow</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    A curated list of translations of English commands to their
                    corresponding Bash syntax from{' '}
                    <Link
                      href="https:\/\/github.com\/TellinaTool\/nl2bash"
                      target="_blank">
                      NL2Bash
                    </Link>
                    .
                    <br style={{ marginBottom: '10px' }} />
                    <Link
                      href="https://github.com/IBM/clai/blob/nlc2cmd/docs/nl2bash-data.md"
                      target="_blank">
                      <FaDownload16 className="fill-blue" /> Download
                    </Link>
                  </StructuredListCell>
                </StructuredListRow>

                <StructuredListRow tabIndex={22}>
                  <StructuredListCell>
                    <span className="scroll-offset" id="data-manual-pages">
                      <strong>Documentation</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    The competition will be confined to the Bash user commands
                    listed{' '}
                    <Link
                      href="http://manpages.ubuntu.com/manpages/bionic/en/man1/"
                      target="_blank">
                      here
                    </Link>
                    , available for download as manual pages below. Also
                    included are webpages scraped from{' '}
                    <Link href="https://www.computerhope.com/" target="_blank">
                      computerhope.com
                    </Link>
                    ,{' '}
                    <Link href="https://www.mankier.com/" target="_blank">
                      mankier.com
                    </Link>
                    ,{' '}
                    <Link
                      href="http://dsl.org/cookbook/cookbook_toc.html"
                      target="_blank">
                      {' '}
                      the linux cookbook
                    </Link>
                    , and GNU documentation.
                    <br style={{ marginBottom: '10px' }} />
                    <Link
                      href="https://github.com/IBM/clai/blob/nlc2cmd/docs/manpage-data.md"
                      target="_blank">
                      <FaDownload16 className="fill-blue" /> Manual Pages
                    </Link>{' '}
                    |{' '}
                    <Link
                      href="https://drive.google.com/file/d/1KmijhOXS9PI7TB0XWJ8E1g5eP2hLVlCp/view?usp=sharing"
                      target="_blank">
                      <FaDownload16 className="fill-blue" /> Webpages
                    </Link>
                  </StructuredListCell>
                </StructuredListRow>

                <StructuredListRow tabIndex={24}>
                  <StructuredListCell>
                    <span className="scroll-offset" id="ainix-data">
                      <strong>AInix</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    AInix is a free and open platform for AI-assisted computing.
                    It enables applications like aish, a command-line shell that
                    understands both natural language, and normal shell
                    commands. The project is currently in an early pre-alpha
                    Proof of Concept stage with many aspects still in
                    development.
                    <br style={{ marginBottom: '10px' }} />
                    <Link href="http://ainix.org/" target="_blank">
                      AInix
                    </Link>{' '}
                    |{' '}
                    <Link
                      href="https://github.com/DNGros/ai-nix-kernal-dataset-archie-json"
                      target="_blank">
                      <FaDownload16 className="fill-blue" /> Download
                    </Link>
                  </StructuredListCell>
                </StructuredListRow>

                <StructuredListRow
                  tabIndex={23}
                  className="suppress-border-bottom">
                  <StructuredListCell />
                  <StructuredListCell>
                    If you know of other data that may be useful here, please
                    get in touch and we will add them to this list.
                  </StructuredListCell>
                </StructuredListRow>
              </StructuredListHead>
            </StructuredListWrapper>
          </StructuredListRow>

          <StructuredListRow tabIndex={3}>
            <StructuredListCell>
              <span className="font-bold scroll-offset" id="code">
                Code
              </span>
            </StructuredListCell>

            <StructuredListWrapper style={{ marginBottom: '0' }}>
              <StructuredListHead>
                <StructuredListRow tabIndex={31}>
                  <StructuredListCell>
                    <span className="scroll-offset" id="code-parser">
                      <strong>Command parser</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    This will help you parse a Bash command into its respective
                    utilities, flags, and parameters (extended from the{' '}
                    <Link
                      href="https://github.com/idank/bashlex"
                      target="_blank">
                      bashlint
                    </Link>{' '}
                    parser).
                    <br style={{ marginBottom: '10px' }} />
                    <Link
                      href="https://github.com/IBM/clai/tree/nlc2cmd/utils/bashlint"
                      target="_blank">
                      Command Parser
                    </Link>
                  </StructuredListCell>
                </StructuredListRow>

                <StructuredListRow tabIndex={31}>
                  <StructuredListCell>
                    <span className="scroll-offset" id="code-metric">
                      <strong>Metric computation</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    This will help you compute the score of a prediction.
                    <br style={{ marginBottom: '10px' }} />
                    <Link
                      href="https://github.com/IBM/clai/tree/nlc2cmd/utils/metric"
                      target="_blank">
                      Accuracy
                    </Link>{' '}
                    |{' '}
                    <Link
                      href="https://github.com/IBM/clai/blob/nlc2cmd/docs/efficiency-computation.md"
                      target="_blank">
                      Efficiency
                    </Link>
                  </StructuredListCell>
                </StructuredListRow>

                <StructuredListRow tabIndex={32}>
                  <StructuredListCell>
                    <span className="scroll-offset" id="code-baseline">
                      <strong>Baseline</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    Tellina / NL2Bash is the state of the art for translation of
                    English commands to Bash syntax. It is the baseline for the
                    NLC2CMD competition. You must at least beat the baseline to
                    win.
                    <br style={{ marginBottom: '10px' }} />
                    <Link
                      href="http://kirin.cs.washington.edu:8000/"
                      target="_blank">
                      Tellina Server
                    </Link>{' '}
                    |{' '}
                    <Link
                      href="https://github.com/IBM/clai/tree/nlc2cmd/tellina-baseline"
                      target="_blank">
                      NL2Bash on GitHub
                    </Link>
                  </StructuredListCell>
                </StructuredListRow>

                <StructuredListRow
                  tabIndex={33}
                  className="suppress-border-bottom">
                  <StructuredListCell>
                    <span className="scroll-offset" id="submit">
                      <strong>Submit</strong>
                    </span>
                  </StructuredListCell>
                  <StructuredListCell>
                    Submissions are managed through EvalAI. Follow the
                    instructions in the helper code below to evaluate your
                    submissions online.
                    <br style={{ marginBottom: '10px' }} />
                    <Link
                      href="https://github.com/IBM/clai/tree/nlc2cmd/submission-code"
                      target="_blank">
                      Helper Code
                    </Link>{' '}
                    |{' '}
                    <Link
                      href="https://evalai.cloudcv.org/web/challenges/challenge-page/674/overview"
                      target="_blank">
                      NLC2CMD @ EvalAI{' '}
                    </Link>
                  </StructuredListCell>
                </StructuredListRow>
              </StructuredListHead>
            </StructuredListWrapper>
          </StructuredListRow>

          <StructuredListRow tabIndex={4} className="suppress-border-bottom">
            <StructuredListCell>
              <span className="font-bold scroll-offset" id="contact">
                Contact
              </span>
            </StructuredListCell>
            <StructuredListCell>
              Got questions? Join us on the{' '}
              <Link href="http:\/\/ibm.biz\/clai-slack">CLAI Slack</Link> or
              email us at{' '}
              <Link href="mailto:nlc2cmd@gmail.com">nlc2cmd@gmail.com</Link>.
            </StructuredListCell>
          </StructuredListRow>
        </StructuredListBody>
      </StructuredListWrapper>
    </div>
  );
};

export default ParticipatePage;
