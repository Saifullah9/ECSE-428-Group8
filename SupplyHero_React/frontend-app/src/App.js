import React from 'react';

import './App.css';

import ImageUpload from './ImageUpload/ImageUpload'
import MenuNavbar from './MenuNavbar/Navbar'

function App() {

  /**
   * IMPORTANT - Try your best keep your components in separate files!
   *             It will abstract the details of implementation
   *             that may not be required to add features.
   */
  return (
    <div className="App">
      {/* Sample taken from https://material-ui.com/components/app-bar/ 
          Feel free to change to support what's needed */}
      <MenuNavbar />
      <ImageUpload /> 

    </div>
  );
}


export default App;