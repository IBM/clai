import React from 'react';
import { LinkList } from '../../components/Info';

import {
  StructuredListWrapper,
  StructuredListHead,
  StructuredListRow,
  StructuredListCell,
  StructuredListBody,
  Tag,
} from 'carbon-components-react';

const ExtendedLinkList = ({ primaryUrl, secondaryUrl }) => {
  return (
    <LinkList
      primaryUrlName={'Home'}
      primaryUrl={primaryUrl}
      secondaryUrlName={'Twitter'}
      secondaryUrl={secondaryUrl}
    />
  );
};

const RenderBio = bio => {
  return <span dangerouslySetInnerHTML={{ __html: bio }} />;
};

const OrgInfo = [
  {
    id: 0,
    name: 'Mayank Agarwal',
    affiliation: 'IBM Research',
    role: 'Sudo',
    roleColor: 'green',
    roleUrl: '',
    imageUrl: 'mayank',
    bio: RenderBio(
      'Mayank is a research engineer at IBM Research,\n' +
        'and he holds a Masters degree in Computer\n' +
        'Science from the University of Massachusetts\n' +
        "Amherst. At IBM Research, he's worked on\n" +
        'federated learning, contextual bandits, and\n' +
        'semi-supervised learning, with publications at\n' +
        'NeurIPS, ICML, ICLR, and AAAI. For Project CLAI,\n' +
        'he has been responsible for designing key APIs\n' +
        'for AI agent integration into the project.'
    ),
    home:
      'https://researcher.watson.ibm.com/researcher/view.php?person=ibm-Mayank.Agarwal',
    twitter: 'https://twitter.com/mayankagarwal__',
  },
  {
    id: 1,
    name: 'Tathagata Chakraborti',
    affiliation: 'IBM Research',
    role: 'Contact',
    roleColor: 'blue',
    roleUrl: 'mailto:nlc2cmd@gmail.com',
    imageUrl: 'tathagata',
    bio: RenderBio(
      'Tathagata works on human-AI collaboration and\n' +
        'sequential decision-making. Before joining IBM,\n' +
        'he received back to back IBM Ph.D. Fellowships,\n' +
        'an honorable mention for the ICAPS Best\n' +
        'Dissertation Award, and was invited to draft the\n' +
        'landscaping primer for the Partnership of AI\n' +
        'Pillar on Collaborations Between People and AI\n' +
        'Systems in recognition of his work. He has a\n' +
        'track record for taking research ideas into\n' +
        'prototypes, having received multiple ICAPS demo\n' +
        'awards and been invited to serve as the\n' +
        'ICAPS-2021 Demo Chair as a result. He is the\n' +
        'project lead of\n' +
        "<a href='https://github.com/IBM/clai' class='no-decoration-link'>CLAI</a>,\n" +
        'an effort aimed to bring the power of AI to\n' +
        'the command line interface.'
    ),
    home: 'http://tchakra2.com',
    twitter: 'https://twitter.com/tchakra2',
  },
  {
    id: 2,
    name: 'Kartik Talamadupula',
    affiliation: 'IBM Research',
    imageUrl: 'kartik',
    bio: RenderBio(
      'Kartik’s background is in sequential\n' +
        'decision-making and its application to various\n' +
        'AI, ML, and NLP problems. IBM, he has worked on\n' +
        'applying AI techniques to dialog systems,\n' +
        'human-agent collaboration mechanisms, and\n' +
        'natural language inference. He has won multiple\n' +
        'awards for demonstrating the applicability of AI\n' +
        'systems to real world problems, including the\n' +
        'AAAI 2018 Best Demonstration award. He has\n' +
        'organized several workshops at AI venues such as\n' +
        'AAAI, IJCAI, and NeurIPS; most recently, KR2ML\n' +
        '2019 at NeurIPS and RCQA 2020 at AAAI. He served\n' +
        'on the AAAI 2020 organizing committee as the\n' +
        'Systems Demonstrations co-chair, and will be\n' +
        'serving as the ICAPS 2021 Program Chair for\n' +
        "applications. He is currently leading IBM's\n" +
        '"AI4Code" effort for modernizing the developer\n' +
        'experience.'
    ),
    home:
      'https://researcher.watson.ibm.com/researcher/view.php?person=us-krtalamad',
    twitter: 'https://twitter.com/kr_t',
  },
  {
    id: 3,
    name: 'Oren Etzioni',
    affiliation: 'Allen Institute for AI (AI2)',
    imageUrl: 'oren',
    role: 'Advisor',
    roleColor: 'purple',
    roleUrl: '',
    bio: RenderBio(
      'Oren is the CEO of the Allen Institute for AI\n' +
        '(AI2). He has been a Professor at the University\n' +
        "of Washington's Computer Science department\n" +
        'since 1991, and a Venture Partner at the Madrona\n' +
        'Venture Group since 2000. He has garnered\n' +
        "several awards including Seattle's Geek of the\n" +
        'Year (2013), the Robert Engelmore Memorial Award\n' +
        '(2007), the IJCAI Distinguished Paper Award\n' +
        '(2005), AAAI Fellow (2003), and a National Young\n' +
        'Investigator Award (1993). He has been the\n' +
        'founder or co-founder of several companies,\n' +
        'including Farecast (sold to Microsoft) and\n' +
        'Decide (sold to eBay). He also led the\n' +
        'pioneering work on AI Softbots on the CLI during\n' +
        'the 90s.'
    ),
    home: 'https://allenai.org/team/orene/',
    twitter: 'https://twitter.com/etzioni',
  },
  {
    id: 4,
    name: 'Jorge Barroso',
    affiliation: 'IBM Research',
    imageUrl: 'jorge',
    bio: RenderBio(
      'Jorge Barroso is the co-founder and developer of\n' +
        'Karumi. Before Karumi, he worked at Tuenti, the\n' +
        'leading Spanish social network, and MVNO. Jorge\n' +
        'developed a wide variety of strategic products\n' +
        'covering J2ME, Blackberry and especially\n' +
        'Android. With over 10 years of software\n' +
        'engineering experience, he also works on\n' +
        'developing videogames and boardgames. He is the lead developer of\n' +
        "<a href='https://github.com/IBM/clai' class='no-decoration-link'>Project CLAI</a>."
    ),
    home: 'https://www.karumi.com/',
    twitter: 'https://twitter.com/flipper83',
  },
  {
    id: 5,
    name: 'Borja Godoy',
    affiliation: 'IBM Research',
    imageUrl: 'borja',
    bio: RenderBio(
      'Borja is a front-end developer at IBM Research\n' +
        'specializing in voice assistants, web components\n' +
        'and generation of tooling. He is also currently\n' +
        'an Organizer at Google Developer Group Spain,\n' +
        'participating in the organization of events such\n' +
        'as ExFest de Cáceres. He led the front-end\n' +
        'development of the Santander Bank project, a\n' +
        'large university-entrepreneurship initiative.'
    ),
    home: 'https://es.linkedin.com/in/borja-godoy',
    twitter: 'https://twitter.com/gody11',
  },
  {
    id: 6,
    name: 'Victoria Xi Lin',
    affiliation: 'Salesforce Research',
    role: 'Baseline',
    roleColor: 'red',
    roleUrl: '',
    imageUrl: 'victoria',
    bio: RenderBio(
      'Victoria is a research scientist at Salesforce\n' +
        'Research. She develops novel machine learning\n' +
        'solutions for natural language understanding\n' +
        'tasks such as semantic parsing and question\n' +
        'answering. She led the original\n' +
        "<a href='https://github.com/TellinaTool/nl2bash/' class='no-decoration-link'>NL2Bash</a>\n" +
        'work on an end-user scripting assistant on the\n' +
        'Bash that can be queried in natural language.\n' +
        'She will be providing the baseline for the\n' +
        'competition based on NL2Bash.'
    ),
    home: 'http://victorialin.net/',
    twitter: 'https://twitter.com/victorialinml',
  },
  {
    id: 7,
    name: 'Eli M Dow',
    affiliation: 'IBM Research',
    imageUrl: 'eli',
    bio: RenderBio(
      'Eli is the Senior Technical Staff Member in the\n' +
        'IBM Research Emerging Technology Accelerator and\n' +
        'is the growth initiative software engineering\n' +
        'and developer enablement lead for IBM Research.\n' +
        'Professionally, he is Research software\n' +
        'developer, author, and prolific inventor based\n' +
        'in Yorktown NY. He is designated as a "Master\n' +
        'Inventor" and is a member of the IBM Academy of\n' +
        'Technology. He has decades of experience leading\n' +
        'research teams for proof-of-concept or\n' +
        'exploratory research software development from\n' +
        'concept to production.'
    ),
    home:
      'https://researcher.watson.ibm.com/researcher/view.php?person=us-emdow',
  },
];

const MemberCard = props => {
  const generateImageUrl = imageUrl => {
    return `${process.env.PUBLIC_URL}/images/team/${imageUrl}.png`;
  };

  return (
    <StructuredListWrapper
      selection
      ariaLabel="Structured list"
      className="social-distancing">
      <StructuredListHead>
        <StructuredListRow head tabIndex={0}>
          <StructuredListCell head>
            {props.MemberInfo.name}
            <span className="company ibm-color">
              {' '}
              | {props.MemberInfo.affiliation}
            </span>
            &nbsp;
            {props.MemberInfo.role && props.MemberInfo.roleUrl && (
              <Tag title={'Contact'} type={props.MemberInfo.roleColor}>
                <a
                  href={props.MemberInfo.roleUrl}
                  className="no-decoration-link">
                  {props.MemberInfo.role}
                </a>
              </Tag>
            )}
            {props.MemberInfo.role && !props.MemberInfo.roleUrl && (
              <Tag title={'Contact'} type={props.MemberInfo.roleColor}>
                {props.MemberInfo.role}
              </Tag>
            )}
          </StructuredListCell>
          <StructuredListCell head />
        </StructuredListRow>
      </StructuredListHead>
      <StructuredListBody>
        <StructuredListRow tabIndex={0}>
          <StructuredListCell>
            <div className="bx--row">
              <div className="bx--col-md-12 bx--col-lg-2">
                <div className="image-frame">
                  <img
                    className="image-circle"
                    src={generateImageUrl(props.MemberInfo.imageUrl)}
                    alt="Carbon illustration"
                    width="100px"
                    height="auto"
                  />
                </div>
              </div>

              <div className="bx--col-md-12 bx--col-lg-14">
                <p> {props.MemberInfo.bio} </p>
                <div className="info-links">
                  <ExtendedLinkList
                    primaryUrl={props.MemberInfo.home}
                    secondaryUrl={props.MemberInfo.twitter}
                  />
                </div>
              </div>
            </div>
          </StructuredListCell>
        </StructuredListRow>
      </StructuredListBody>
    </StructuredListWrapper>
  );
};

export { MemberCard, OrgInfo };
