

import React from 'react';
import ReactDOM from 'react-dom';
import MapContainer from './screens/MapScreen/MapScreen';
 

ReactDOM.render(
  <React.StrictMode>
    <div style={{ backgroundColor: '#eee' }}>
      <MapContainer apiKey='AIzaSyCqCO4OFri0-do9lW15udLNC_Bh-KbkW0I' center={{ lat: 28.4595, lng: 77.0266 }} zoom={10} />
    </div>
  </React.StrictMode>,
  document.getElementById('root')
);
  