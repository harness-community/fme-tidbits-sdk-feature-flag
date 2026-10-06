import React from 'react';
import { SplitFactory } from '@splitsoftware/splitio-react';
import DiscountBanner from './DiscountBanner';

// Replace with your Harness FME Browser/Client-side SDK key
const SDK_KEY = 'YOUR_CLIENT_SIDE_SDK_KEY';

const sdkConfig = {
  core: {
    authorizationKey: SDK_KEY,
    key: 'user_anonymous',
  },
};

function App() {
  return (
    <SplitFactory config={sdkConfig}>
      <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
        <div style={{ display: 'inline-block', background: '#61DAFB', color: '#000', padding: '4px 12px', borderRadius: '12px', fontSize: '13px', fontWeight: 'bold', marginBottom: '8px' }}>
          ⚛️ React SDK — port 3000
        </div>
        <h1>🛍️ Harness E-Commerce Store</h1>
        <p>Welcome to our store! Check out our latest products.</p>

        {/* Feature flag controls the banner */}
        <DiscountBanner />

        <div style={{ marginTop: '20px', padding: '20px', background: '#f5f5f5', borderRadius: '8px' }}>
          <h2>Featured Products</h2>
          <p>Product 1 — $49.99</p>
          <p>Product 2 — $29.99</p>
          <p>Product 3 — $99.99</p>
        </div>
      </div>
    </SplitFactory>
  );
}

export default App;
