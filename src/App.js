import React, { Component } from 'react';
import './app.scss';
import { Content } from 'carbon-components-react/lib/components/UIShell';
import PageHeader from './components/PageHeader';
import { Route, Switch } from 'react-router-dom';
import LandingPage from './content/LandingPage';
import ParticipatePage from './content/ParticipatePage';
import ChallengePage from './content/ChallengePage';
import LeaderboardPage from './content/LeaderboardPage';
import PublicationsPage from './content/PublicationsPage';
import DonePage from './content/DonePage';

class App extends Component {
  render() {
    return (
      <>
        <PageHeader />
        <Content>
          <Switch>
            <Route exact path="/" component={LandingPage} />
            <Route path="/participate" component={ParticipatePage} />
            <Route path="/challenge" component={ChallengePage} />
            <Route path="/leaderboard" component={LeaderboardPage} />
            <Route path="/publications" component={PublicationsPage} />
            <Route path="/done" component={DonePage} />
            <Route
              path="/clai"
              component={() => {
                window.location.href = 'https://github.com/IBM/clai';
                return null;
              }}
            />
            <Route
              path="/evalai"
              component={() => {
                window.location.href =
                  'https://evalai.cloudcv.org/web/challenges/challenge-page/674/overview';
                return null;
              }}
            />
          </Switch>
        </Content>
      </>
    );
  }
}

export default App;
