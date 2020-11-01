import React, { Component } from 'react';
import axios from 'axios';
import ls from 'local-storage'

export default class Logout extends Component{

    constructor(props){
        super(props);
        this.onSubmit = this.onSubmit.bind(this);
     
    /*
        this.state = {
            username: '',
            password: '',
        }
        */
    }

   
    onSubmit(e){
        e.preventDefault();

    /*    
        const user = {
            username:this.state.username,
            password:this.state.password,
        }

        console.log(user);
        const dataForm = new FormData();
        dataForm.append('username', this.state.username);
        dataForm.append('password', this.state.password);
    */    

        /*
        this is commented out till the post request is completed in the backend
        need to know the parameters needed for the request from the backend
        */
      
      //  axios.post('http://localhost:8000/logout') 
      //  .then(res => {console.log(res.data)
      //  localStorage.removeItem('Login_token')});

       /* this.setState({
            username:'',
            password:'',
        }) */

       // window.location = '/login' // reroutes to login page after submitting
        
    }



    render(){
        return(
            <div>
              <h3>Logout</h3>
              <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                <input type="submit" value="Confirm Logout" className="btn btn-primary" />
                </div>
              </form>
            </div>
        )
    }
}