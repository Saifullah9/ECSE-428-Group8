import React, { Component } from 'react';
import axios from 'axios';

export default class Login extends Component{
    constructor(props){
        super(props);

        this.onChangeUsername = this.onChangeUsername.bind(this);
        this.onChangePassword = this.onChangePassword.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        
        this.state = {
            username: '',
            password: '',
        }
    }

    onChangeUsername(e){
        this.setState({
            username: e.target.value
        });
    }

    onChangePassword(e){
        this.setState({
            password: e.target.value
        });
    }

    onSubmit(e){
        e.preventDefault();

        const user = {
            username:this.state.username,
            password:this.state.password,
        }

        console.log(user);

        axios.post('http://localhost:8000/login')
        .then(res => console.log(res.data));

        this.setState({
            username:'',
            password:'',
        })
        //window.location = '/' // reroutes to home page after submitting
        
    }



    render(){
        return(
            <div>
              <h3>Login</h3>
              <form onSubmit={this.onSubmit}>
                <div className="form-group">
                    <label>Username: </label>
                    <input
                        type="text"
                        required
                        value={this.state.username}
                        placeholder="Enter your email"
                        className="form-control"
                        onChange={this.onChangeUsername}
                    />
                    <label>Password: </label>
                    <input
                        type="text"
                        required
                        value={this.state.password}
                        placeholder="Enter your password"
                        className="form-control"
                        onChange={this.onChangePassword}
                    />
                    </div>
                    <div className="form-group">
                <input type="submit" value="Login" className="btn btn-primary" />
                </div>
              </form>
            </div>
        )
    }
}