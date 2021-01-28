import React from 'react';
import AppSwitcher20 from '@carbon/icons-react/lib/app-switcher/20';
import { Link } from 'react-router-dom';

import HeaderContainer from 'carbon-components-react/lib/components/UIShell/HeaderContainer';
import {
  Header,
  HeaderMenuButton,
  HeaderName,
  HeaderNavigation,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
  HeaderSideNavItems,
  SkipToContent,
  SideNav,
  SideNavItems,
} from 'carbon-components-react/lib/components/UIShell';

const toCLAI = () => {
  window.location.href = 'https://clai-home.mybluemix.net/';
  return null;
};

const PageHeader = (isSideNavExpanded, onClickSideNavExpand) => (
  <HeaderContainer
    render={({ isSideNavExpanded, onClickSideNavExpand }) => (
      <>
        <Header aria-label="Carbon Tutorial">
          <SkipToContent />
          <HeaderMenuButton
            aria-label="Open menu"
            onClick={onClickSideNavExpand}
            isActive={isSideNavExpanded}
          />
          <HeaderName element={Link} to="/" prefix="NeurIPS 2020">
            nlc2cmd
          </HeaderName>
          <HeaderNavigation aria-label="nlc2cmd links">
            <HeaderMenuItem element={Link} to="/participate">
              Compete
            </HeaderMenuItem>
            <HeaderMenuItem element={Link} to="/challenge">
              Challenge
            </HeaderMenuItem>
            <HeaderMenuItem element={Link} to="/publications">
              Publications
            </HeaderMenuItem>
            <HeaderMenuItem element={Link} to="/evalai">
              EvalAI
            </HeaderMenuItem>
          </HeaderNavigation>
          <HeaderGlobalBar>
            <HeaderMenuItem element={Link} to="/clai">
              Project CLAI
            </HeaderMenuItem>
            <HeaderGlobalAction aria-label="App Switcher" onClick={toCLAI}>
              <AppSwitcher20 />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
          <SideNav
            aria-label="Side navigation"
            expanded={isSideNavExpanded}
            isPersistent={false}>
            <SideNavItems>
              <HeaderSideNavItems>
                <HeaderMenuItem element={Link} to="/participate">
                  Participate
                </HeaderMenuItem>
                <HeaderMenuItem element={Link} to="/leaderboard">
                  Leaderboard
                </HeaderMenuItem>
                <HeaderMenuItem element={Link} to="/publications">
                  Publications
                </HeaderMenuItem>
                <HeaderMenuItem element={Link} to="/evalai">
                  EvalAI
                </HeaderMenuItem>
              </HeaderSideNavItems>
            </SideNavItems>
          </SideNav>
        </Header>
      </>
    )}
  />
);

export default PageHeader;
