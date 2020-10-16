import React from 'react';

import './App.css';

import "bootstrap/dist/css/bootstrap.min.css"// installed and imported bootstrap -Saifullah
import { BrowserRouter as Router, Route } from "react-router-dom"; // installed react routers to make it easier to add urls to components -Saifullah
import Navbar from "./components/navbar.component";
import SupplyList from "./components/supply-list.component";
import Register from "./components/register.component";
import Login from "./components/login.component";
import Logout from "./components/logout.component";
import Upload from "./components/upload.component";
import ImageUpload from './ImageUpload/ImageUpload'
import MenuNavbar from './MenuNavbar/Navbar'

function App() {

  /**
   * IMPORTANT - Try your best keep your components in separate files!
   *             It will abstract the details of implementation
   *             that may not be required to add features.
   */
  return (
    <Router>
   {/* <div className="App">

    
       Sample taken from https://material-ui.com/components/app-bar/ 
          Feel free to change to support what's needed 
     
      I currently removed the sections below to make it easier to route and develop the modules first then enhance in another sprint -Saifullah
      <MenuNavbar />
      <ImageUpload /> 
      
    </div>*/}
    <Navbar />
      <br/>
      <Route path = "/" exact component={SupplyList} />
      <Route path = "/register"  component={Register} />
      <Route path = "/login"  component={Login} />
      <Route path = "/logout"  component={Logout} />
      <Route path = "/upload/:id"  component={Upload} />
    </Router>
  );
}


export default App;