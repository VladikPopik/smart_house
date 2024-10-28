
import '../fullscreen.css';
import '../logout.css';
import Home from '../components/Home';
// import Logout from '../Logout';
// import * as React from 'react';

import CardHome from '../components/CardHome';
import AppBarComponent from '../components/AppBarComponent';

function HomePage () {
  return (
    <body>
      <Home />
      <AppBarComponent />
      <div style={{position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '75%', height: '75%' }}>
        <CardHome/>
      </div>
    </body>
  );
}
export default HomePage;
