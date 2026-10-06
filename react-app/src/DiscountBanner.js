import React from 'react';
import { useTreatments, SplitContext } from '@splitsoftware/splitio-react';
import { useContext } from 'react';

const FLAG_NAME = 'show-discount-banner';

function DiscountBanner() {
  const { isReady } = useContext(SplitContext);
  const treatments = useTreatments([FLAG_NAME]);
  const treatment = treatments[FLAG_NAME]?.treatment;

  if (!isReady) {
    return null; // SDK still loading
  }

  if (treatment === 'on') {
    return (
      <div style={{
        background: '#4CAF50',
        color: 'white',
        padding: '16px',
        borderRadius: '8px',
        textAlign: 'center',
        fontSize: '18px',
        fontWeight: 'bold',
        margin: '16px 0'
      }}>
        🎉 10% off today! Use code <strong>HARNESS10</strong> at checkout.
      </div>
    );
  }

  // treatment === 'off' or control — no banner
  return null;
}

export default DiscountBanner;
