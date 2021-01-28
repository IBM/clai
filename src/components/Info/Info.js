import React from 'react';

import Globe32 from '@carbon/icons-react/lib/globe/32';
import PersonFavorite32 from '@carbon/icons-react/lib/person--favorite/32';
import Application32 from '@carbon/icons-react/lib/application/32';

import { Link } from 'carbon-components-react';

// Take in a phrase and separate the third word in an array
function createArrayFromPhrase(phrase) {
  const splitPhrase = phrase.split(' ');
  const thirdWord = splitPhrase.pop();
  return [splitPhrase.join(' '), thirdWord];
}

const InfoSection = props => (
  <section className={`bx--row ${props.className} info-section`}>
    <div className="bx--col-md-8 bx--col-lg-4 bx--col-xlg-3">
      <h3 className="info-section__heading">{props.heading}</h3>
      <h6 className="info-section__secondary_heading">{props.subheading}</h6>
    </div>
    {props.children}
  </section>
);

const InfoCard = props => {
  const splitHeading = createArrayFromPhrase(props.heading);

  return (
    <div className="info-card bx--col-md-4 bx--col-lg-4 bx--col-xlg-3 bx--offset-xlg-1">
      <h4 className="info-card__heading">
        {`${splitHeading[0]} `}
        <strong>{splitHeading[1]}</strong>
      </h4>
      <p className="info-card__body">{props.body}</p>
      {props.icon}
    </div>
  );
};

const InfoAreaCompetition = props => (
  <InfoSection
    heading="Competition Timeline"
    subheading="NuerIPS 2020, Dec 11"
    className="landing-page__r3">
    <InfoCard
      heading="Stage-1 July"
      body="The Competition is live! You will be able to access starter code, sample data, and evaluate your algorithms on public data. We are hosted on EvalAI."
      icon={<PersonFavorite32 />}
    />
    <InfoCard
      heading="Stage-2 October"
      body={
        <>
          The validator against the held out data is out in October. You can
          evaluate your approach against the held out validation set.{' '}
          <span style={{ color: 'red' }}>
            Deadline for new sign-ups is Oct 31, 2020 AoE.
          </span>
        </>
      }
      icon={<Application32 />}
    />
    <InfoCard
      heading="Stage-3 November"
      body="You can try your approach against the held out test data start of November. This will be allowed only a limited number of times. The Competition ends on November 21."
      icon={<Globe32 />}
    />
  </InfoSection>
);

const InfoAreaChallenge = props => (
  <InfoSection
    heading="Challenge Timeline"
    subheading="NuerIPS 2020, Dec 11"
    className="landing-page__r3">
    <InfoCard
      heading="Stage-1 Now"
      body="The Challenge is live! You will be able to submit data as many times as you want."
      icon={<PersonFavorite32 />}
    />
    <InfoCard
      heading="Stage-2 October"
      body="The Challenge ends on Oct 30, just before the testing phase of The Competition. Your data will be validated and added to the test set at this point."
      icon={<Application32 />}
    />
    <InfoCard
      heading="Stage-3 December"
      body="The results of The Competition as well as The Challenge will be out in December."
      icon={<Globe32 />}
    />
  </InfoSection>
);

const LinkList = ({
  primaryUrlName,
  primaryUrl,
  secondaryUrlName,
  secondaryUrl,
}) => (
  <ul style={{ display: 'flex' }}>
    <li>
      <Link href={primaryUrl} target="_blank">
        {primaryUrlName}
      </Link>
    </li>
    {secondaryUrl && (
      <li>
        <span>&nbsp;|&nbsp;</span>
        <Link href={secondaryUrl} target="_blank">
          {secondaryUrlName}
        </Link>
      </li>
    )}
  </ul>
);

function generateTermsURL(key) {
  return `${process.env.PUBLIC_URL}/files/${key}-terms.pdf`;
}

export { InfoAreaCompetition, InfoAreaChallenge, LinkList, generateTermsURL };
