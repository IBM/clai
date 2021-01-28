import React from 'react';
import {
  StructuredListWrapper,
  StructuredListHead,
  StructuredListRow,
  StructuredListCell,
  StructuredListBody,
  StructuredListInput,
} from 'carbon-components-react';
import DocumentPdf16 from '@carbon/icons-react/lib/document--pdf/16';

const PublicationsList = [
  {
    id: 0,
    title: 'Language Models are Few-Shot Learners',
    authors:
      'Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei',
    venue: 'arXiv',
    link: 'https://arxiv.org/abs/2005.14165',
  },
  {
    id: 7,
    title: 'Project CLAI -- Bringing AI to the Command Line Interface',
    authors:
      'Mayank Agarwal, Jorge Barroso Carmona, Tathagata Chakraborti,\n' +
      'Eli M. Dow, Kshitij P. Fadnis, Borja Godoy, and Kartik Talamadupula',
    venue: 'NeurIPS 2019 Demonstration Track',
    link: 'https://arxiv.org/abs/2002.00762',
  },
  {
    id: 10,
    title:
      'SmartShell: Automated Shell Scripts Synthesis from Natural Language',
    authors: 'Hao Li, Yu Ping Wang, Jie Yin, and Gang Tan',
    venue:
      'International Journal of Software Engineering and Knowledge Engineering',
    link: 'https://www.worldscientific.com/doi/abs/10.1142/S0218194019500098',
  },
  {
    id: 11,
    title:
      'AInix: An Open Platform for Natural Language Interfaces to Shell Commands',
    authors: 'David Gros, Advised by Raymond Mooney',
    venue: 'Honors Theses, University of Texas Austin',
    link: 'https://apps.cs.utexas.edu/apps/tech-reports/177982',
  },
  {
    id: 12,
    title:
      'NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System',
    authors:
      'Xi Victoria Lin and Chenglong Wang and Luke Zettlemoyer and Michael D. Ernst',
    venue: 'LREC 2018',
    link: 'https://www.aclweb.org/anthology/L18-1491/',
  },
  {
    id: 13,
    title:
      'Program Synthesis from Natural LanguageUsing Recurrent Neural Networks',
    authors:
      'Xi Victoria Lin, Chenglong Wang, Deric Pang, Kevin Vu, Luke Zettlemoyer, and Michael D. Ernst',
    venue: 'Technical Report (2017) UW-CSE-17-03-01',
    link:
      'https://homes.cs.washington.edu/~mernst/pubs/nl-command-tr170301-abstract.html',
  },
  {
    id: 14,
    title:
      'UbuntuWorld 1.0 LTS - A Platform for Automated Problem Solving & Troubleshooting in the Ubuntu OS',
    authors:
      'Tathagata Chakraborti, Kartik Talamadupula, Kshitij P. Fadnis, Murray Campbell, and Subbarao Kambhampati',
    venue: 'AAAI / IAAI, 2017',
    link: 'https://aaai.org/ocs/index.php/IAAI/IAAI17/paper/view/14206',
  },
  {
    id: 15,
    title: 'Reinforcement Learning for Mapping Instructions to Actions',
    authors:
      'S.R.K. Branavan, Harr Chen, Luke Zettlemoyer, and Regina Barzilay',
    venue: 'ACL / Natural Language Processing of the AFNLP',
    link: 'https://www.aclweb.org/anthology/P09-1010/',
  },
  {
    id: 16,
    title: 'The Linux Plan Corpus',
    authors: 'Nate Blaylock',
    venue: 'Technical Report',
    link: 'https://www.cs.rochester.edu/research/cisd/resources/linux-plan/',
  },
  {
    id: 17,
    title: 'A Softbot-Based Interface to the Internet',
    authors: 'Oren Etzioni and Daniel Weld',
    venue: 'AAAI',
    link: 'https://www.aaai.org/Papers/ARPI/1996/ARPI96-020.pdf',
  },
];

const Publication = props => {
  const rowName = id => {
    return `row-${id}`;
  };

  return (
    <StructuredListRow tabIndex={props.PublicationInfo.id}>
      <StructuredListCell>
        <strong>{props.PublicationInfo.title}. </strong>
        {props.PublicationInfo.authors}. {props.PublicationInfo.venue}.
      </StructuredListCell>
      <StructuredListInput
        id={rowName(props.PublicationInfo.id)}
        value={rowName(props.PublicationInfo.id)}
        title={rowName(props.PublicationInfo.id)}
        name={rowName(props.PublicationInfo.id)}
        defaultChecked
      />
      <StructuredListCell>
        <a
          href={props.PublicationInfo.link}
          target="_blank"
          rel="noopener noreferrer">
          <DocumentPdf16
            className="bx--structured-list-svg"
            aria-label="View PDF">
            <title>View PDF</title>
          </DocumentPdf16>
        </a>
      </StructuredListCell>
    </StructuredListRow>
  );
};

const PublicationsPage = () => {
  return (
    <div className="bx--grid bx--grid--full-width landing-page">
      <div className="bx--row publications-page__tab-content">
        <StructuredListWrapper selection ariaLabel="Structured list">
          <StructuredListHead>
            <StructuredListRow head tabIndex={0}>
              <StructuredListCell
                head
                className="publications-page__publications-list-header">
                The following is a list of publications relevant to the
                competition (youngest first). We will continue to update this
                list as the competition progresses.
              </StructuredListCell>
              <StructuredListCell head />
            </StructuredListRow>
          </StructuredListHead>
          <StructuredListBody>
            {PublicationsList.map(publication => (
              <React.Fragment key={publication.id}>
                <Publication PublicationInfo={publication} />
              </React.Fragment>
            ))}
          </StructuredListBody>
        </StructuredListWrapper>
      </div>
    </div>
  );
};

export default PublicationsPage;
