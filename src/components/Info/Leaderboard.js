import React from 'react';
import { LinkList } from './Info.js';
import { winners } from './results.js';
import {
  Tag,
  Link,
  DataTable,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  Button,
} from 'carbon-components-react';

import { TrophyFilled16 } from '@carbon/icons-react';

const headerData = [
  {
    header: 'Team Name',
    key: 'name',
  },
  {
    header: 'Accuracy',
    key: 'accuracy',
  },
  {
    header: 'Power (mW)',
    key: 'power',
  },
  {
    header: 'Latency (sec)',
    key: 'latency',
  },
  {
    header: '',
    key: 'links',
  },
];

class Leaderboard extends React.Component {
  constructor() {
    super();
    this.state = {};
  }

  componentDidMount() {
    var newData = [];
    var template = {
      id: null,
      name: null,
      accuracy: null,
      power: null,
      latency: null,
      links: null,
      disqualified: false,
      baseline: false,
    };

    winners.map((item, key) => {
      var newTemplate = JSON.parse(JSON.stringify(template));
      newTemplate['id'] = key;
      newTemplate['name'] = item['name'];

      newTemplate['accuracy'] = (
        <>
          {item['accuracy'][0]}{' '}
          {item['accuracy'][1] && (
            <span style={{ fill: '#FFD700' }}>
              <TrophyFilled16 />
            </span>
          )}
        </>
      );
      newTemplate['power'] = (
        <>
          {item['power'][0]}{' '}
          {item['power'][1] && (
            <span style={{ fill: '#FFD700' }}>
              <TrophyFilled16 />
            </span>
          )}
        </>
      );
      newTemplate['latency'] = item['latency'][0];

      if (item.baseline)
        newTemplate['name'] = (
          <>
            {item['name']}{' '}
            <Tag type="purple" title="Clear Filter">
              baseline
            </Tag>
          </>
        );

      if (item.disqualified) {
        newTemplate['name'] = (
          <>
            <span style={{ color: 'silver' }}>{item['name']}</span>{' '}
            <Tag type="gray" title="Clear Filter">
              disqualified
            </Tag>
          </>
        );

        newTemplate['accuracy'] = (
          <>
            <span style={{ color: 'silver' }}>{item['accuracy'][0]}</span>{' '}
            {item['accuracy'][1] && (
              <span style={{ fill: '#FFD700' }}>
                <TrophyFilled16 />
              </span>
            )}
          </>
        );
        newTemplate['power'] = (
          <>
            <span style={{ color: 'silver' }}>{item['power'][0]}</span>{' '}
            {item['power'][1] && (
              <span style={{ fill: '#FFD700' }}>
                <TrophyFilled16 />
              </span>
            )}
          </>
        );
        newTemplate['latency'] = (
          <>
            <span style={{ color: 'silver' }}>{item['latency'][0]}</span>
          </>
        );
      }

      if (item.links)
        newTemplate['links'] = (
          <>
            <LinkList
              primaryUrlName="GitHub"
              primaryUrl={item.links[0]}
              secondaryUrlName="Report"
              secondaryUrl={item.links[1]}
            />
          </>
        );

      newData.push(newTemplate);
    });

    this.setState({
      ...this.state,
      data: newData,
    });
  }

  render() {
    return (
      <section className="bx--row landing-page__r3 info-section">
        {this.state.data && (
          <DataTable
            rows={this.state.data}
            headers={headerData}
            render={({ rows, headers, getHeaderProps, getTableProps }) => (
              <div className="bx--col-lg-14 bx--offset-lg-1">
                <TableContainer
                  style={{ width: '100%' }}
                  title={
                    <>
                      <span style={{ marginRight: '20px' }}>
                        NLC2CMD Leaderboard
                      </span>
                      <Link
                        href="https://www.ibm.com/blogs/research/2020/12/ai-natural-language-competition/"
                        target="_blank">
                        <Button size="small" kind="secondary">
                          Read the Blog
                        </Button>
                      </Link>
                    </>
                  }>
                  <Table size="normal" {...getTableProps()}>
                    <TableHead>
                      <TableRow>
                        {headers.map(header => (
                          <TableHeader
                            key={header.key}
                            {...getHeaderProps({ header })}>
                            {header.header}
                          </TableHeader>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {rows.map(row => (
                        <TableRow key={row.id}>
                          {row.cells.map(cell => (
                            <TableCell key={cell.id}>
                              {cell.value && cell.value}
                            </TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
                <p className="disclaimer" style={{ marginTop: '10px' }}>
                  DISCLAIMER: GPT-3 was run with off-the-shelf settings with two
                  temperature settings of 0.3 and 0.7 and the same prompt as the
                  OpenAI demo. This result is NOT meant to be taken as the
                  definitive result on the effectiveness of GPT-3 in the NLC2CMD
                  task but is instead meant to illustrate the difficulty of the
                  task for off-the-shelf language models not optimized for
                  downstream tasks. Many many thanks to the OpenAI team for
                  helping us set up.
                </p>
                <p className="disclaimer" style={{ marginTop: '10px' }}>
                  Teams tagged "disqualified" did not conform to the T&C and
                  open source their code. Overall, 16 teams signed up for the
                  competition, with 204 submissions over the course of the three
                  stages (38 in dev, 119 in val, and 47 in test). A massive
                  thank you to everyone who took part! Special mention to{' '}
                  <Link
                    href="https://github.com/Shikhar-S/Neural-Machine-Translation/tree/cmd_sq2sq"
                    target="_blank"
                    style={{ color: 'dimgray', fontSize: 'smaller' }}>
                    Shikhar Bharadwaj
                  </Link>{' '}
                  who did not compete in the final phase but still shared his
                  code in the spirit of the open competition, and our best
                  wishes to Reshinth Adithyan who has been an active participant
                  throughout but could not complete the final phase due to
                  cyclones in India. Finally, congratulations to our winners
                  Quchen, Jaron, and Kangwook; and thank you to Kangwook, Jaron,
                  David, and Quchen for the many discussions and shaping the
                  NLC2CMD task over the duration of the competition.
                </p>
              </div>
            )}
          />
        )}
      </section>
    );
  }
}

export { Leaderboard };
