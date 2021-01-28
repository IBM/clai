import React from 'react';
import TeamTable from './TeamTable';
import { Link } from 'carbon-components-react';
import { LinkList } from '../../components/Info';

const tellina_description = () => {
  return (
    <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
      <div className="bx--col-lg-16">
        We will be using the original{' '}
        <Link href={'https://www.aclweb.org/anthology/L18-1491.pdf'}>
          NL2Bash
        </Link>{' '}
        paper as the baseline. The translator is based on{' '}
        <Link href={'https://arxiv.org/abs/1409.0473'}>Seq2Seq</Link> and{' '}
        <Link href={'https://arxiv.org/abs/1603.06393'}>CopyNet</Link> models.
        We will help you set up the code once the competitiion begins.
      </div>
    </div>
  );
};

const dummy_description = () => {
  return (
    <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
      <div className="bx--col-lg-16">
        The competitiion begins in June. Read more about the timeline{' '}
        <Link href={'/#/participate'}>here</Link>.
      </div>
    </div>
  );
};

const headers = [
  {
    key: 'name',
    header: 'Team Name',
  },
  {
    key: 'joinedOn',
    header: 'Joined',
  },
  {
    key: 'updatedAt',
    header: 'Updated',
  },
  {
    key: 't1',
    header: 'Accuracy',
  },
  {
    key: 't2',
    header: 'Latency',
  },
  {
    key: 'links',
    header: '',
  },
];

const data = [
  {
    id: '1',
    name: 'Tellina/NL2Bash',
    joinedOn: '2018-05-07',
    updatedAt: '2020-02-17',
    t1: '--',
    t2: '--',
    url: 'https://github.com/TellinaTool/nl2bash',
    homepageUrl: 'http://tellina.rocks/',
    description: tellina_description(),
  },
  {
    id: '2',
    name: '--',
    joinedOn: '--',
    updatedAt: '--',
    t1: '--',
    t2: '--',
    description: dummy_description(),
  },
];

const getRowItems = rows =>
  rows.map(row => ({
    ...row,
    key: row.id,
    name: row.name,
    joinedOn: row.joinedOn,
    updatedAt: row.updatedAt,
    t1: row.t1,
    t2: row.t2,
    links: (
      <LinkList
        primaryUrlName="GitHub"
        primaryUrl={row.url}
        secondaryUrlName="Homepage"
        secondaryUrl={row.homepageUrl}
      />
    ),
    description: row.description,
  }));

const rows = getRowItems(data);

const LeaderboardPage = () => {
  return (
    <div className="bx--grid bx--grid--full-width bx--grid--no-gutter no-edges">
      <TeamTable headers={headers} rows={rows} />
    </div>
  );
};

export default LeaderboardPage;
