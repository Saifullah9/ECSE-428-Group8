import React, { Component } from 'react';

export default class Register extends Component{
    render(){
        return(
            <div>
              <p>Your are now on the Register component</p>
              <form>
                <h1>Register</h1>
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
                <button className="btn" type="submit">
                Register
                </button>
              </form>
            </div>
        )
    }
}