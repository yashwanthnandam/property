import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import PropertyMap from './components/maps/maps';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div style={{ backgroundColor: '#eee' }}>
      {/* <PropertyMap apiKey='AIzaSyCqCO4OFri0-do9lW15udLNC_Bh-KbkW0I' center={{ lat: 28.4595, lng: 77.0266 }} zoom={10} /> */}
      <PropertyMap/>
    </div>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
reportWebVitals();

