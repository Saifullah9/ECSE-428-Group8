import React, { Component } from 'react';

export default class Login extends Component{
    render(){
        return(
            <div>
                <p>Your are now on the Login component</p>
                <h1>Login</h1>
                <input
                name="email"
                type="text"
                placeholder="Enter your email"
                className="textbox"
                />
                <input
                name="password"
                type="password"
                placeholder="Enter your password"
                className="textbox"
                />
            </div>
        )
    }
}