import React from 'react';
import { MemberCard, OrgInfo } from './OrgInfo';
import {
  InfoAreaCompetition,
  LinkList,
  Leaderboard,
} from '../../components/Info';
import {
  Button,
  Tabs,
  Tab,
  Tag,
  TextInput,
  Link,
  InlineLoading,
  RadioButtonGroup,
  RadioButton,
  StructuredListRow,
  StructuredListCell,
  StructuredListHead,
  StructuredListBody,
  StructuredListWrapper,
} from 'carbon-components-react';

import FaExternalLinkAlt20 from '@carbon/icons-react/lib/link/20';
import { TrophyFilled16 } from '@carbon/icons-react';

const props = {
  tabs: {
    selected: 0,
    triggerHref: '#',
    role: 'navigation',
  },
  tab: {
    href: '#',
    role: 'presentation',
    tabIndex: 0,
  },
};

const known_endpoints = {
  tellina: 'http://nlc2cmd.sl.res.ibm.com:8000/api/translate',
  gpt3: 'http://gpt3server.mybluemix.net/gpt3',
};

class TextInputNew extends React.Component {
  constructor() {
    super();
    this.state = {
      placeholder: 'Try it out! e.g. "extract files from an archive".',
      value: '',
      innerElement: '</>',
      submitButtonType: 'secondary',
      isDisabled: false,
      service: 'tellina',
    };
  }

  Tellina = e => {
    this.setState({
      isDisabled: true,
      innerElement: <InlineLoading className="no-fill" />,
      submitButtonType: 'ghost',
    });

    const user_command = document.getElementById('tellina-embed').value;
    var gpt3_key = null;

    if (document.getElementById('gpt3-key-embed'))
      gpt3_key = document.getElementById('gpt3-key-embed').value;

    const endpoint = known_endpoints[this.state.service];
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        command: user_command,
        text: user_command,
        use_cached_prompt: true,
        gpt3_key: gpt3_key,
      }),
    };

    // console.log(requestOptions)
    // return false;

    fetch(endpoint, requestOptions)
      .then(response => response.json())
      .then(
        function(data) {
          this.setState({
            placeholder: data['response'],
            value: '',
            innerElement: '</>',
            submitButtonType: 'secondary',
            isDisabled: false,
          });
        }.bind(this)
      )
      .catch(console.log);
  };

  handleInputChange = e => {
    this.setState({ value: this.textInput.value });
  };

  logSelection = e => {
    this.setState({
      ...this.state,
      placeholder: 'Try it out! e.g. "extract files from an archive".',
      value: '',
      innerElement: '</>',
      submitButtonType: 'secondary',
      isDisabled: false,
      service: e.target.id.replace('radio-', ''),
    });
  };

  handleKeyPress = e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      this.Tellina();
    }
  };

  render() {
    return (
      <form>
        <div className="bx--col-lg-16 tellina-area">
          <div className="bx--row service-selector">
            <Button
              size="small"
              kind={this.state.submitButtonType}
              id="tellina-submit"
              hasIconOnly={true}
              iconDescription="Bash!"
              onClick={this.Tellina}
              className="bx--offset-lg-1">
              {this.state.innerElement}
            </Button>
            <TextInput
              labelText=""
              id="tellina-embed"
              ref={input => {
                this.textInput = input;
              }}
              value={this.state.value}
              placeholder={this.state.placeholder}
              onChange={this.handleInputChange.bind(this)}
              onKeyPress={this.handleKeyPress.bind(this)}
              disabled={this.state.isDisabled}
            />
          </div>
        </div>
        <div className="bx--col-lg-16">
          {this.state.service === 'gpt3' && (
            <div className="bx--row" style={{ marginTop: '5px' }}>
              <div
                className="bx--col-lg-2"
                style={{ paddingLeft: '0', paddingRight: '0' }}>
                <TextInput
                  light
                  labelText=""
                  id="gpt3-key-embed"
                  placeholder="xxxxxxxxxxxxx"
                />
              </div>
              <div className="bx--col-lg-6">
                <p className="disclaimer">
                  Enter your <Link href="">NLC2CMD Challenge</Link> key to use
                  the GPT-3 API. You get 10x the number of examples you have
                  contributed.{' '}
                  <span style={{ color: 'red' }}>
                    Service will resume on Dec 13.
                  </span>
                </p>
              </div>
            </div>
          )}

          <div className="bx--row" style={{ marginTop: '5px' }}>
            <RadioButtonGroup
              defaultSelected="default-selected"
              legend="Group Legend"
              name="radio-button-group"
              valueSelected="default-selected">
              <RadioButton
                id="radio-tellina"
                name="translator-service"
                labelText={
                  <Link
                    href="http://kirin.cs.washington.edu:8000/"
                    target="_blank"
                    className="black-link">
                    Tellina
                  </Link>
                }
                value="default-selected"
                onClick={this.logSelection.bind(this)}
              />
              <RadioButton
                id="radio-gpt3"
                name="translator-service"
                labelText={
                  <ul style={{ display: 'flex' }}>
                    <li>
                      <Link
                        href="https://openai.com/blog/openai-api/"
                        target="_blank"
                        className="black-link">
                        GPT-3
                      </Link>
                    </li>
                    <li>
                      <span>&nbsp;|&nbsp;</span>
                      <Link
                        href="https://github.com/IBM/clai/tree/master/clai/server/plugins/gpt3"
                        target="_blank"
                        className="black-link">
                        Try it on your command line!
                      </Link>
                    </li>
                  </ul>
                }
                value="standard"
                onClick={this.logSelection.bind(this)}
              />
            </RadioButtonGroup>
          </div>
        </div>
      </form>
    );
  }
}

const LandingPage = () => {
  return (
    <div className="bx--grid bx--grid--full-width landing-page">
      <div className="bx--row landing-page__banner">
        <div className="bx--col-lg-16">
          <LinkList
            primaryUrlName={'NeurIPS 2020'}
            primaryUrl={'https://neurips.cc/Conferences/2020/CompetitionTrack'}
            secondaryUrlName={'Project CLAI'}
            secondaryUrl={'https://github.com/IBM/clai'}
          />
          <h1 className="landing-page__heading">The NLC2CMD Challenge</h1>
          <TextInputNew />
        </div>
      </div>
      <div className="bx--row landing-page__r2">
        <div className="bx--col bx--no-gutter">
          <Tabs {...props.tabs} aria-label="Tab navigation">
            <Tab {...props.tab} label="About">
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                  <div
                    className="bx--col-md-4 bx--col-lg-7"
                    style={{ marginBottom: '50px' }}>
                    <h2 className="landing-page__subheading">About NLC2CMD.</h2>
                    <p className="participation-page__p">
                      The NLC2CMD Competition brings the power of natural
                      language processing to the command line. You are tasked
                      with building models that can transform descriptions of
                      command line tasks in English to their Bash syntax.
                    </p>
                    <p className="participation-page__p">
                      Don't have time to compete? You can still get involved by
                      challenging the participants with your favorite command
                      line tasks.
                    </p>
                    <br />
                    <br />
                    <Link
                      href="/#/participate"
                      rel="noopener noreferrer"
                      style={{ marginRight: '10px' }}>
                      <Button size="field" kind="primary">
                        Compete
                      </Button>
                    </Link>
                    <Link href="/#/challenge" rel="noopener noreferrer">
                      <Button size="field" kind="secondary">
                        Challenge
                      </Button>
                    </Link>
                  </div>
                  <div className="bx--col-md-4 bx--offset-lg-1 bx--col-lg-8">
                    <img
                      className="landing-page__illo"
                      src={`${process.env.PUBLIC_URL}/images/screencast.png`}
                      alt="Carbon illustration"
                    />
                    <p className="disclaimer">
                      &nbsp; <sup>*</sup>Snapshot of Bash with the{' '}
                      <Link
                        className="black-link"
                        href={
                          'https://github.com/IBM/clai/tree/master/clai/server/plugins/nlc2cmd'
                        }>
                        NLC2CMD skill on CLAI
                      </Link>{' '}
                      .
                    </p>
                  </div>
                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Backstory">
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                  <div className="bx--col-md-12 bx--offset-lg-2 bx--col-lg-12">
                    <h2 className="landing-page__subheading">
                      The NLC2CMD Story.
                    </h2>

                    <p className="participation-page__p">
                      The NLC2CMD competition revolves around a simple use case:
                      translating natural language (NL) descriptions of command
                      line tasks to their correct Bash syntax. The image below
                      provides a glimpse of how life on the command line will
                      change with NLC2CMD capabilities. NLC2CMD ensures that the
                      user on the terminal does not have to leave the terminal
                      and go looking for answers on the internet every time they
                      get stuck, while normal life on the terminal continues for
                      regular Bash commands.
                    </p>

                    <br />
                    <div className="bx--col-md-12 bx--col-lg-14">
                      <img
                        className="landing-page__illo"
                        src={`${process.env.PUBLIC_URL}/images/screencast.png`}
                        alt="Carbon illustration"
                      />
                    </div>

                    <p className="participation-page__p">
                      It renders obsolete all the cheat sheets for{' '}
                      <Link
                        href={
                          'https://education.github.com/git-cheat-sheet-education.pdf'
                        }>
                        git commands
                      </Link>{' '}
                      or{' '}
                      <Link
                        href={
                          'https://github.com/ibm-cloud-docs/cli/blob/master/IBM%20Cloud%20CLI%20quick%20reference.pdf}'
                        }>
                        cloud syntax
                      </Link>{' '}
                      that developers <em>still</em> have to memorize! Such
                      interactions, if successful over a large variety of
                      command line tasks, has the potential to transform the way
                      we interact with operating systems, cloud platforms,
                      mainframes, etc. thereby lowering the barrier to entry and
                      increasing the accessibility of compute resources across
                      the planet.
                    </p>

                    <br />

                    <h2 className="landing-page__subheading">AI Softbots.</h2>

                    <p className="participation-page__p">
                      The AI community has always had a soft spot for AI
                      assistants on the command line. In the early to mid 90s,
                      researchers at the University of Washington conducted
                      extensive academic work in this space under the umbrella
                      of "
                      <Link
                        href={
                          'https://www.aaai.org/Papers/ARPI/1996/ARPI96-020.pdf'
                        }>
                        Internet Softbots
                      </Link>
                      ". In the late 90s, Microsoft introduced a slew of
                      assistive agents along with their Office productivity
                      software. Unfortunately, the (in)famous{' '}
                      <Link
                        href={'https://en.wikipedia.org/wiki/Office_Assistant'}>
                        Clippy
                      </Link>{' '}
                      and other commercial AI sofbots fell short of user
                      expectations. Notably, this generation of embodied
                      assistants taught future designers{' '}
                      <Link
                        href={
                          'https://www.goodreads.com/book/show/44098.The_Inmates_Are_Running_the_Asylum'
                        }>
                        valuable lessons
                      </Link>{' '}
                      for the deployment of future agents.
                    </p>

                    <p className="participation-page__p">
                      Recently, a number of rule-based command line assistants
                      such as{' '}
                      <Link href={'https://github.com/Bash-it/bash-it'}>
                        Bash-it
                      </Link>
                      ,{' '}
                      <Link href={'https://github.com/nvbn/thefuck'}>
                        The Fuck
                      </Link>
                      ,{' '}
                      <Link href={'https://github.com/tldr-pages/tldr'}>
                        tldr
                      </Link>
                      , etc. have emerged. These CLI assistants generally deal
                      with correcting misspelled commands and other common
                      errors on the command line, as well as automating
                      commonlyperformed tasks using predefined scripts. While
                      these assistants certainly make the job of working with
                      the command line easier, they have a high maintenance
                      burden due to theconstant up-keep of the rules that form
                      their back-end. In general, such domain specificsolutions
                      do not scale or generalize. Recent advances in machine
                      learning stands to make big contributions in this area.
                    </p>

                    <p className="participation-page__p">
                      In order to construct a more generalized solution to
                      assistive CLI-centric AI, one must be able to learn the
                      rules of the underlying system. The{' '}
                      <Link
                        href={
                          'https://www.cs.rochester.edu/research/cisd/resources/linux-plan/'
                        }>
                        Linux Plan Corpus
                      </Link>{' '}
                      -- a collection of Linux sessions collected at the
                      University of Rochester in 2003 -- provides a great source
                      of data for research in this direction. Similarly, the{' '}
                      <Link
                        href={
                          'https://aaai.org/ocs/index.php/IAAI/IAAI17/paper/view/14206'
                        }>
                        UbuntuWorld
                      </Link>{' '}
                      used a combination of automated planning, reinforcement
                      learning (RL), and information retrieval to drive
                      data-driven exploration and decision making on the CLI
                      through a process of bootstrapping data from the AskUbuntu
                      forum. Researchers have also attempted to use
                      reinforcement learning (RL) for{' '}
                      <Link href={'https://www.aclweb.org/anthology/P09-1010/'}>
                        interpreting instructions in the Windows OS
                      </Link>
                      . With recent advances -- especially on sample complexity
                      -- learning agents are poised for a comeback in the
                      context of operating systems. In this particular
                      competition we look at the specific use case of NLC2CMD
                      and propose to automate the generation of command line
                      plugins that can translate NL instructions to their
                      corresponding Bash syntax.
                    </p>

                    <br />
                    <h2 className="landing-page__subheading">
                      The CLI is back!
                    </h2>

                    <p className="participation-page__p">
                      The command line has always been near and dear to the life
                      of a developer due to its speed, expressiveness, and ease
                      of use (for power users). However, another reason for the
                      popularity of CLIs is that oftentimes, users{' '}
                      <em>have to</em> use them. This is proved by recent trends
                      in software development: GUIs can rarely keep up with the
                      rate of change of features (e.g. consider the time it took
                      to move from Docker to Kubernetes to OpenShift in cloud
                      platforms). This means that CLIs become the default
                      interfacing medium not just for new adopters of a
                      software, but also for experts in one domain (e.g.
                      programming) who are no longer experts in others (e.g.
                      devops). The merging of developer and devops roles is
                      certainly an emerging trend with the proliferation of
                      cloud applications in the development lifecycle. This is
                      highlighted by newly emergent CLIs with smart features,
                      such as{' '}
                      <Link href={'https://devspace.cloud/'}>DevSpace</Link>,{' '}
                      <Link
                        href={
                          'https://developers.redhat.com/products/odo/overview/}'
                        }>
                        odo
                      </Link>
                      , and so on for cloud native applications; and the well
                      documented{' '}
                      <Link
                        href={
                          'https://www.zdnet.com/article/good-news-for-developers-the-cli-is-back/'
                        }>
                        second coming of CLIs
                      </Link>{' '}
                      in the media.
                      <a
                        href="https://apievangelist.com/2019/11/05/what-is-behind-the-cli-making-a-comeback/"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                      <a
                        href="https://www.theverge.com/2019/6/4/18651872/apple-macos-catalina-zsh-bash-shell-replacement-features"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                      <a
                        href="https://avc.com/2015/09/the-return-of-the-command-line-interface/"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                    </p>

                    <p className="participation-page__p">
                      However, even with the CLI's re-emergence, the issue of
                      support on the command line remains a huge problem. The
                      image below on the left [
                      <Link href={'https://danluu.com/cli-complexity/'}>
                        Source
                      </Link>
                      ] shows the increasing complexity of those commands over
                      the years, while that on the right [
                      <Link href={'https://github.com/TellinaTool/nl2bash'}>
                        Source
                      </Link>
                      ] shows Bash utilities users ask for help with the most:{' '}
                      <em>
                        tar now has 139 options while curl has 230 options!
                      </em>
                    </p>

                    <br />
                    <br />
                    <div className="bx--col-lg-12">
                      <div className="bx--row">
                        <div className="bx--col-12 bx--col-lg-4">
                          <img
                            className="landing-page__illo"
                            src={`${
                              process.env.PUBLIC_URL
                            }/images/wtf-options.png`}
                            alt="Carbon illustration"
                            width="100%"
                          />
                        </div>
                        <div className="bx--col-12 bx--col-lg-11">
                          <img
                            className="landing-page__illo"
                            src={`${process.env.PUBLIC_URL}/images/so-data.png`}
                            alt="Carbon illustration"
                            width="100%"
                          />
                        </div>
                      </div>
                    </div>

                    <br />
                    <p className="participation-page__p">
                      The image below shows how community sourced support has
                      failed to keep up with the needs of users. This data from{' '}
                      <Link href={'https://meta.askubuntu.com/a/8575'}>
                        Ask Ubuntu
                      </Link>{' '}
                      illustrates the inability of community-sourced support to
                      scale with the proliferation of "Zombie posts" or
                      questions unanswered for over 72hrs over the last few
                      years. This further motivates the need for on-premise
                      support (such as CLI plugins) with easy accessibility
                      (such as using natural language). There has been an
                      increasing amount of work that builds towards the NLC2CMD
                      use case, in particular to natural language to code.
                      <a
                        href="https://pennstate.pure.elsevier.com/en/publications/smartshell-automated-shell-scripts-synthesis-from-natural-languag"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                      <a
                        href="https://www.aclweb.org/anthology/L18-1491/"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                      <a
                        href="https://homes.cs.washington.edu/~mernst/pubs/nl-command-tr170301-abstract.html"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                      <a
                        href="http://ainix.org/"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                      <a
                        href="https://github.com/pickhardt/betty"
                        target="_blank"
                        rel="noopener noreferrer">
                        <FaExternalLinkAlt20 />
                      </a>
                    </p>

                    <br />
                    <br />
                    <div className="bx--col-12 bx--col-lg-14">
                      <img
                        className="landing-page__illo"
                        src={`${process.env.PUBLIC_URL}/images/zombies.png`}
                        alt="Carbon illustration"
                        width="100%"
                      />
                    </div>

                    <br />
                    <p className="participation-page__p">
                      It's time to flatten the curve.
                    </p>
                  </div>
                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="xkcd!">
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                  <div className="bx--col-md-12 bx--offset-lg-4 bx--col-lg-8">
                    <img
                      className="landing-page__illo"
                      src={`${process.env.PUBLIC_URL}/images/xkcd.png`}
                      alt="Carbon illustration"
                    />

                    <p className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                      <br />
                      "I don't know what's worse--the fact that after 15 years
                      of using tar I still can't keep the flags straight, or
                      that after 15 years of technological advancement I'm still
                      mucking with tar flags that were 15 years old when I
                      started."
                      <br />
                      <br />
                      <a
                        href="https://uni.xkcd.com/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="no-decoration-link">
                        <Button size="field" kind="secondary">
                          xkcd &lt;/&gt;
                        </Button>
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Team">
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                  {OrgInfo.map(Member => (
                    <React.Fragment key={Member.id}>
                      <MemberCard MemberInfo={Member} />
                    </React.Fragment>
                  ))}
                </div>
              </div>
            </Tab>
          </Tabs>
        </div>
      </div>
      <Leaderboard />

      <div
        className="bx--col-lg-14 bx--offset-lg-1"
        style={{ marginTop: '40px' }}>
        <StructuredListWrapper
          ariaLabel="Structured list"
          style={{ marginBottom: '20px' }}>
          <StructuredListHead>
            <StructuredListRow>
              <StructuredListCell head>
                NeurIPS 2020 NLC2CMD Session <br />
                Sat, Dec 12th, 2020
              </StructuredListCell>
            </StructuredListRow>
          </StructuredListHead>
          <StructuredListBody>
            <StructuredListRow>
              <StructuredListCell>14:00 – 14:05 EST</StructuredListCell>
              <StructuredListCell>Mayank Agarwal</StructuredListCell>
              <StructuredListCell>
                NLC2CMD Competition: Introduction, Problem Description, CLAI |{' '}
                <Link href="https://slideslive.com/38942499" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:05 – 14:15 EST</StructuredListCell>
              <StructuredListCell>Victoria Lin</StructuredListCell>
              <StructuredListCell>
                NLC2CMD Keynote: Tellina <Tag type="green">live</Tag>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:15 – 14:20 EST</StructuredListCell>
              <StructuredListCell>Mayank Agarwal</StructuredListCell>
              <StructuredListCell>
                NLC2CMD Competition: Metrics, Data, Tracks |{' '}
                <Link href="https://slideslive.com/38942501" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:20 – 14:22 EST</StructuredListCell>
              <StructuredListCell>David Gros</StructuredListCell>
              <StructuredListCell>
                Participant Team: AINixClaiSimple |{' '}
                <Link href="https://slideslive.com/38942502" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:22 – 14:24 EST</StructuredListCell>
              <StructuredListCell>Juyeon Yoon</StructuredListCell>
              <StructuredListCell>
                Participant Team: coinse-team |{' '}
                <Link href="https://slideslive.com/38942503" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:24 – 14:26 EST</StructuredListCell>
              <StructuredListCell>
                Kangwook Lee{' '}
                <span style={{ fill: '#FFD700' }}>
                  <TrophyFilled16 />
                </span>
              </StructuredListCell>
              <StructuredListCell>
                Participant Team: AICore |{' '}
                <Link href="https://slideslive.com/38942507" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:26 – 14:28 EST</StructuredListCell>
              <StructuredListCell>
                Quchen Fu{' '}
                <span style={{ fill: '#FFD700' }}>
                  <TrophyFilled16 />
                </span>
              </StructuredListCell>
              <StructuredListCell>
                Participant Team: Magnum |{' '}
                <Link href="https://slideslive.com/38942505" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:28 – 14:30 EST</StructuredListCell>
              <StructuredListCell>
                Jaron Maene{' '}
                <span style={{ fill: '#FFD700' }}>
                  <TrophyFilled16 />
                </span>
              </StructuredListCell>
              <StructuredListCell>
                Participant Team: Hubris |{' '}
                <Link href="https://slideslive.com/38942508" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:30 – 14:32 EST</StructuredListCell>
              <StructuredListCell>Denis Litvinov</StructuredListCell>
              <StructuredListCell>
                Participant Team: Jb |{' '}
                <Link href="https://slideslive.com/38942509" target="_blank">
                  View
                </Link>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:32 – 14:45 EST</StructuredListCell>
              <StructuredListCell>Kartik Talamadupula</StructuredListCell>
              <StructuredListCell>
                NLC2CMD Competition: Results <Tag type="green">live</Tag>
              </StructuredListCell>
            </StructuredListRow>
            <StructuredListRow>
              <StructuredListCell>14:45 – 16:00 EST</StructuredListCell>
              <StructuredListCell>Open Forum</StructuredListCell>
              <StructuredListCell>
                We will use this time to call for open participation, ways to
                improve going forward, and discuss next steps in the life of the
                competition. <Tag type="green">live</Tag>
              </StructuredListCell>
            </StructuredListRow>
          </StructuredListBody>
        </StructuredListWrapper>

        <Link
          href="https://neurips.cc/virtual/2020/protected/e_competitions.html"
          target="_blank">
          <Button kind="primary" size="field">
            Join us Live!
          </Button>
        </Link>
        <br />
        <br />
        <br />
        <br />
      </div>

      <InfoAreaCompetition />
    </div>
  );
};

export default LandingPage;
