import React from 'react';
import CheckmarkFilled32 from '@carbon/icons-react/lib/checkmark--filled/32';
import { Tag } from 'carbon-components-react';

const DonePage = props => {
  return (
    <div className="bx--grid bx--grid--full-width landing-page">
      <br />
      <div className="bx--row">
        <div className="bx--row">
          <div className="bx--col-2" style={{ paddingLeft: '30px' }}>
            <CheckmarkFilled32 style={{ fill: '#24a148' }} />
          </div>
          <div className="bx--col-14" style={{ paddingLeft: '10px' }}>
            <p>
              Your data has been submitted. Your new submission key is{' '}
              <Tag type="purple" title="Clear Filter">
                {' '}
                {props.location.state.key}{' '}
              </Tag>
              . Please save this for future submissions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DonePage;
